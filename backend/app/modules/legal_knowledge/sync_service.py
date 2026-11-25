"""Official-source verification, synchronization, and review queue orchestration.

This service turns the declarative CSV registry into operational state. It never
promotes fetched content into the searchable corpus automatically: every fetched
document becomes an immutable ``LegalDocumentVersion`` in ``PENDING_REVIEW`` and
requires an explicit administrative ingest action.
"""

from __future__ import annotations

from datetime import date
from typing import Any, Dict, Iterable, List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logging import logger
from app.core.storage import get_storage_provider
from app.modules.legal_knowledge.discovery import discover_documents
from app.modules.legal_knowledge.fetcher import FetchError, SecureFetcher, storage_key_for_document
from app.modules.legal_knowledge.ingestion_pipeline import LegalDocumentIngestionPipeline, compute_sha256
from app.modules.legal_knowledge.models import (
    LegalDocumentVersion,
    LegalReviewItem,
    LegalSourceRegistry,
    LegalSyncJob,
)
from app.modules.legal_knowledge.source_registry import utcnow

AMBIGUOUS_LEGAL_STATUSES = {
    "PARTIALLY_COMMENCED",
    "MODEL_LAW",
    "HISTORICAL",
    "REPEALED",
    "SUPERSEDED",
    "UNKNOWN",
}


class SourceSyncError(RuntimeError):
    """Raised for an invalid or forbidden source synchronization request."""


def _parse_date(value: Optional[str]) -> Optional[date]:
    if not value or not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value[:10])
    except ValueError:
        return None


def _format_from_strategy(strategy: str, content_type: str = "", url: str = "") -> str:
    """Infer format from fetched evidence first, then fall back to registry metadata.

    Registry parser strategies are declarative and may be stale. A source that
    declares PDF but serves HTML must be parsed as HTML, otherwise a valid fetch
    is lost to a parser mismatch.
    """
    path = url.lower().split("?", 1)[0]
    lower_type = (content_type or "").lower()
    if "pdf" in lower_type or path.endswith(".pdf"):
        return "PDF"
    if "xml" in lower_type or path.endswith(".xml"):
        return "XML"
    if "html" in lower_type or path.endswith((".html", ".htm")):
        return "HTML"
    if "wordprocessingml" in lower_type or path.endswith(".docx"):
        return "DOCX"
    if "json" in lower_type or path.endswith(".json"):
        return "JSON"
    if "plain" in lower_type or path.endswith(".txt"):
        return "TXT"
    fmt = (strategy or "").upper()
    if fmt in {"PDF", "HTML", "TXT", "XML", "DOCX", "JSON"}:
        return fmt
    return "TXT"


async def _get_source(db: AsyncSession, source_key: str) -> LegalSourceRegistry:
    result = await db.execute(
        select(LegalSourceRegistry).where(LegalSourceRegistry.registry_key == source_key)
    )
    source = result.scalar_one_or_none()
    if source is None:
        raise SourceSyncError(f"Unknown legal source registry key: {source_key}")
    return source


def _require_fetch_enabled(force: bool) -> None:
    if not settings.RAG_SOURCE_FETCH_ENABLED and not force:
        raise SourceSyncError(
            "Automated official-source fetching is disabled. "
            "Set RAG_SOURCE_FETCH_ENABLED=true or pass force=true for an explicit operator action."
        )


async def verify_sources(
    db: AsyncSession,
    *,
    fetcher: SecureFetcher,
    source_keys: Optional[Iterable[str]] = None,
    force: bool = False,
) -> List[Dict[str, Any]]:
    """Perform policy-compliant live verification of declared document URLs."""
    _require_fetch_enabled(force)
    query = select(LegalSourceRegistry)
    if source_keys:
        keys = list(source_keys)
        query = query.where(LegalSourceRegistry.registry_key.in_(keys))
    sources = (await db.execute(query.order_by(LegalSourceRegistry.registry_key))).scalars().all()

    results: List[Dict[str, Any]] = []
    for source in sources:
        source.last_attempted_fetch = utcnow()
        urls = list((source.source_config or {}).get("document_urls") or [])
        if not urls:
            source.failure_count += 1
            results.append(
                {
                    "registry_key": source.registry_key,
                    "verification_status": source.verification_status,
                    "verified": False,
                    "reason": "NO_DECLARED_DOCUMENT_URL",
                }
            )
            continue

        successes = 0
        failures: List[str] = []
        checksums: List[str] = []
        checksum_mismatches: List[str] = []
        config = source.source_config or {}
        declared_checksum = str(config.get("declared_checksum") or "").strip()
        checksum_is_content_hash = bool(config.get("declared_checksum_is_content_hash"))
        for url in urls:
            try:
                result = await fetcher.fetch(url)
                if result.not_modified:
                    successes += 1
                    continue
                checksum = compute_sha256(result.content)
                if (
                    checksum_is_content_hash
                    and declared_checksum
                    and declared_checksum.casefold() != checksum.casefold()
                ):
                    checksum_mismatches.append(url)
                    failures.append(f"DECLARED_CHECKSUM_MISMATCH: {url}")
                    continue
                checksums.append(checksum)
                successes += 1
            except FetchError as exc:
                failures.append(str(exc)[:300])

        if successes:
            source.last_successful_fetch = utcnow()
            source.failure_count = 0
            if source.verification_status != "REJECTED":
                source.verification_status = "VERIFIED"
        else:
            source.failure_count += 1

        results.append(
            {
                "registry_key": source.registry_key,
                "verification_status": source.verification_status,
                "verified": successes > 0,
                "documents_checked": len(urls),
                "documents_verified": successes,
                "content_checksums": checksums,
                "checksum_mismatches": checksum_mismatches,
                "failures": failures,
                "declared_checksums_are_content_hashes": checksum_is_content_hash,
            }
        )

    await db.commit()
    logger.info("Verified %s/%s declared legal sources", sum(1 for r in results if r["verified"]), len(results))
    return results


async def sync_source(
    db: AsyncSession,
    *,
    source_key: str,
    fetcher: SecureFetcher,
    mode: str = "INCREMENTAL",
    force: bool = False,
    enable_verified: bool = False,
    requested_by: Optional[str] = None,
    storage_provider: Optional[Any] = None,
) -> LegalSyncJob:
    """Discover, fetch, checksum, and queue official documents for review."""
    _require_fetch_enabled(force)
    source = await _get_source(db, source_key)
    storage = storage_provider or get_storage_provider()

    job = LegalSyncJob(
        source_key=source_key,
        mode=(mode or "INCREMENTAL").upper(),
        status="RUNNING",
        checkpoint_json={},
        started_at=utcnow(),
        requested_by=requested_by,
    )
    db.add(job)
    await db.flush()
    source.last_attempted_fetch = utcnow()

    checkpoint: Dict[str, Any] = {}
    try:
        discovered = await discover_documents(
            _source_as_candidate(source), fetcher, max_documents=settings.RAG_DISCOVERY_MAX_DOCUMENTS
        )
        job.documents_discovered = len(discovered)
        prior_versions = {
            row.document_key: row
            for row in (
                await db.execute(select(LegalDocumentVersion).where(LegalDocumentVersion.registry_key == source_key))
            ).scalars().all()
        }

        for document in discovered:
            document_key = document.url
            prior = prior_versions.get(document_key)
            checkpoint[document_key] = {"url": document.url, "status": "PENDING"}
            try:
                etag = (prior.metadata_json or {}).get("etag") if prior else None
                last_modified = (prior.metadata_json or {}).get("last_modified") if prior else None
                fetched = await fetcher.fetch(document.url, if_none_match=etag, if_modified_since=last_modified)
                if fetched.not_modified:
                    checkpoint[document_key]["status"] = "NOT_MODIFIED"
                    continue

                checksum = compute_sha256(fetched.content)
                if prior and prior.content_checksum == checksum:
                    checkpoint[document_key]["status"] = "DUPLICATE"
                    continue

                file_format = _format_from_strategy(document.parser_strategy, fetched.content_type, document.url)
                text = LegalDocumentIngestionPipeline._extract_text(
                    content=fetched.content, file_format=file_format, filename=document.url
                )
                if len(text.strip()) < 20:
                    raise FetchError("Extracted document text is empty or insufficient")

                suffix = {
                    "PDF": ".pdf", "HTML": ".html", "XML": ".xml", "DOCX": ".docx", "TXT": ".txt"
                }.get(file_format, ".bin")
                storage_key = await storage.upload(
                    storage_key_for_document(source_key, checksum, suffix),
                    fetched.content,
                    content_type=fetched.content_type or "application/octet-stream",
                    metadata={"source_key": source_key, "content_checksum": checksum},
                )

                config = source.source_config or {}
                legal_status = (config.get("commencement_status") or "").upper()
                version = LegalDocumentVersion(
                    registry_key=source_key,
                    document_key=document_key,
                    title=document.title[:255],
                    source_url=document.url,
                    version=f"1.{len(prior_versions)}" if prior_versions else "1.0",
                    content_checksum=checksum,
                    normalized_text_checksum=compute_sha256(text.strip()),
                    raw_storage_key=storage_key,
                    status="PENDING_REVIEW",
                    document_type=source.source_category or "BARE_ACT",
                    jurisdiction=source.jurisdiction or "Union of India",
                    authority_level=source.authority_level or "OFFICIAL",
                    publication_date=_parse_date(config.get("published_date") or config.get("effective_date")),
                    effective_date=_parse_date(config.get("effective_date")),
                    valid_from=_parse_date(config.get("effective_date")),
                    metadata_json={
                        "etag": fetched.etag,
                        "last_modified": fetched.last_modified,
                        "content_type": fetched.content_type,
                        "legal_domains": source.legal_domains or [],
                        "commencement_status": legal_status or None,
                        "declared_checksum": config.get("declared_checksum"),
                        "declared_checksum_is_content_hash": False,
                        "final_url": fetched.final_url,
                    },
                )
                db.add(version)
                await db.flush()

                reasons: List[str] = []
                if prior:
                    reasons.append("CHECKSUM_CHANGED")
                else:
                    reasons.append("NEW_DOCUMENT")
                if legal_status in AMBIGUOUS_LEGAL_STATUSES:
                    reasons.append("LEGAL_STATUS_REQUIRES_REVIEW")

                for reason in reasons:
                    db.add(
                        LegalReviewItem(
                            document_version_id=version.id,
                            source_key=source_key,
                            reason=reason,
                            status="PENDING",
                            details_json={
                                "title": version.title,
                                "source_url": document.url,
                                "content_checksum": checksum,
                                "commencement_status": legal_status or None,
                                "note": (
                                    "A changed checksum is not proof of a legally effective amendment. "
                                    "An advocate or legal reviewer must confirm validity before indexing."
                                ),
                            },
                        )
                    )

                prior_versions[document_key] = version
                job.documents_ingested += 1
                checkpoint[document_key] = {
                    "url": document.url,
                    "status": "QUEUED_FOR_REVIEW",
                    "content_checksum": checksum,
                    "version_id": str(version.id),
                }
            except (FetchError, ValueError) as exc:
                job.documents_failed += 1
                checkpoint[document_key] = {"url": document.url, "status": "FAILED", "error": str(exc)[:300]}
                logger.warning("Failed to sync %s: %s", document.url, exc)

        if job.documents_ingested:
            source.last_successful_fetch = utcnow()
            source.verification_status = "VERIFIED"
            if enable_verified:
                source.enabled = True
            source.failure_count = 0
        elif job.documents_failed:
            source.failure_count += 1

        job.checkpoint_json = checkpoint
        job.status = "COMPLETED"
        job.finished_at = utcnow()
        await db.commit()
        await db.refresh(job)
        return job

    except Exception as exc:
        job.status = "FAILED"
        job.error_message = str(exc)[:1000]
        job.finished_at = utcnow()
        job.checkpoint_json = checkpoint
        source.failure_count += 1
        await db.commit()
        await db.refresh(job)
        raise


def _source_as_candidate(source: LegalSourceRegistry) -> Any:
    """Adapt a persisted registry row to the discovery adapter interface."""
    from app.modules.legal_knowledge.source_registry import SourceCandidate

    return SourceCandidate(
        registry_key=source.registry_key,
        name=source.name,
        official_domain=source.official_domain,
        base_url=source.base_url,
        source_category=source.source_category,
        jurisdiction=source.jurisdiction,
        legal_domains=list(source.legal_domains or []),
        document_types=list(source.document_types or []),
        fetch_strategy=source.fetch_strategy,
        parser_strategy=source.parser_strategy,
        authority_level=source.authority_level,
        supported_languages=list(source.supported_languages or []),
        update_frequency_hours=source.update_frequency_hours or 168,
        source_config=dict(source.source_config or {}),
    )


async def ingest_document_version(
    db: AsyncSession,
    *,
    version_id: UUID,
    actor: Optional[str] = None,
    storage_provider: Optional[Any] = None,
) -> Dict[str, Any]:
    """Promote one reviewed document version into the existing ingestion pipeline."""
    result = await db.execute(
        select(LegalDocumentVersion).where(LegalDocumentVersion.id == version_id)
    )
    version = result.scalar_one_or_none()
    if version is None:
        raise SourceSyncError(f"Unknown legal document version: {version_id}")
    if version.status == "INDEXED":
        raise SourceSyncError("This document version has already been indexed")
    if not version.raw_storage_key:
        raise SourceSyncError("This document version has no stored raw source file")

    source_result = await db.execute(
        select(LegalSourceRegistry).where(LegalSourceRegistry.registry_key == version.registry_key)
    )
    registry = source_result.scalar_one_or_none()
    if registry is None:
        raise SourceSyncError("Registry source no longer exists for this document version")

    config = dict(registry.source_config or {})
    meta = dict(version.metadata_json or {})
    storage = storage_provider or get_storage_provider()
    raw_content = await storage.download(version.raw_storage_key)
    file_format = _format_from_strategy(registry.parser_strategy, meta.get("content_type", ""), version.source_url)

    source_metadata = {
        "title": version.title,
        "short_code": registry.registry_key[:64],
        "source_type": version.document_type,
        "citation": config.get("act_number"),
        "jurisdiction": version.jurisdiction,
        "court": None,
        "act_or_judgment_identifier": config.get("document_id") or config.get("act_number"),
        "publication_date": version.publication_date,
        "document_version": version.version,
        "official_source_url": version.source_url,
        "verification_status": "VERIFIED",
        "metadata_json": {
            "registry_key": registry.registry_key,
            "document_version_id": str(version.id),
            "content_checksum": version.content_checksum,
            "normalized_text_checksum": version.normalized_text_checksum,
            "legal_domains": version.metadata_json.get("legal_domains") if version.metadata_json else [],
            "commencement_status": meta.get("commencement_status"),
            "promoted_by": actor,
            "promoted_at": utcnow().isoformat(),
        },
    }

    legal_source, ingestion_job = await LegalDocumentIngestionPipeline.ingest_document(
        db=db,
        source_metadata=source_metadata,
        raw_content=raw_content,
        file_format=file_format,
        filename=version.source_url,
        require_verified_source=True,
    )

    version.legal_source_id = legal_source.id
    version.status = "INDEXED"
    reviews = (
        await db.execute(
            select(LegalReviewItem).where(
                LegalReviewItem.document_version_id == version.id,
                LegalReviewItem.status == "PENDING",
            )
        )
    ).scalars().all()
    for review in reviews:
        review.status = "RESOLVED"
        review.resolved_by = actor
        review.resolved_at = utcnow()
    await db.commit()

    return {
        "document_version_id": str(version.id),
        "legal_source_id": str(legal_source.id),
        "ingestion_job_id": str(ingestion_job.id),
        "chunks_extracted": ingestion_job.chunks_extracted,
        "status": "INDEXED",
    }
