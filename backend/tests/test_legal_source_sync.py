"""Tests for official-source sync checkpoints, review queue, and promotion."""

import pytest
import httpx
from sqlalchemy import select

from app.core.config import settings
from app.core.storage import LocalStorageProvider, set_storage_provider
from app.modules.legal_knowledge.fetcher import SecureFetcher
from app.modules.legal_knowledge.models import (
    LegalChunk,
    LegalDocumentVersion,
    LegalReviewItem,
    LegalSource,
    LegalSourceRegistry,
    LegalSyncJob,
)
from app.modules.legal_knowledge.sync_service import (
    SourceSyncError,
    _format_from_strategy,
    ingest_document_version,
    sync_source,
    verify_sources,
)

BASE = "https://www.indiacode.nic.in"
DOC_URL = f"{BASE}/bitstream/test-act.txt"
STATUTORY_TEXT = (
    "1. Short title.\nThis Act may be called the Test Procedure Act, 2026.\n\n"
    "2. Application.\nAny person may submit a written application to the competent authority "
    "for the procedure described in this Act.\n\n"
    "3. Records.\nThe authority shall preserve all written records received under this Act."
)


def _handler(request: httpx.Request) -> httpx.Response:
    if request.url.path == "/robots.txt":
        return httpx.Response(404)
    if request.url.path == "/bitstream/test-act.txt":
        return httpx.Response(
            200,
            text=STATUTORY_TEXT,
            headers={"content-type": "text/plain; charset=utf-8", "etag": '"test-act-v1"'},
        )
    return httpx.Response(404)


def _fetcher() -> SecureFetcher:
    return SecureFetcher(
        client=httpx.AsyncClient(transport=httpx.MockTransport(_handler), follow_redirects=True),
        verify_dns=False,
        enforce_robots=True,
        rate_limit_per_minute=600,
        max_retries=0,
    )


async def _registry_row(db_session) -> LegalSourceRegistry:
    row = LegalSourceRegistry(
        registry_key="SRC_TEST_ACT",
        name="Test Procedure Act, 2026",
        official_domain="www.indiacode.nic.in",
        base_url=BASE,
        source_category="CENTRAL_ACT",
        jurisdiction="Union of India",
        legal_domains=["Civil Procedure"],
        document_types=["CENTRAL_ACT"],
        fetch_strategy="STATIC_DOCUMENT",
        parser_strategy="TXT",
        authority_level="TIER 1",
        supported_languages=["English"],
        update_frequency_hours=168,
        enabled=False,
        verification_status="PENDING",
        source_config={
            "document_urls": [DOC_URL],
            "declared_checksum": "metadata-derived-not-a-content-hash",
            "declared_checksum_is_content_hash": False,
            "commencement_status": "COMMENCED",
            "act_number": "Act No. 1 of 2026",
        },
    )
    db_session.add(row)
    await db_session.commit()
    await db_session.refresh(row)
    return row


def test_format_detection_prefers_fetched_content_type_over_stale_strategy():
    assert _format_from_strategy("PDF", "text/html; charset=utf-8", "https://kaveri.karnataka.gov.in/") == "HTML"
    assert _format_from_strategy("TXT", "application/pdf", "https://www.indiacode.nic.in/act") == "PDF"
    assert _format_from_strategy("", "text/plain", "https://www.indiacode.nic.in/act.txt") == "TXT"


@pytest.mark.asyncio
async def test_fetch_disabled_by_default_and_explicit_force_allows_verification(
    db_session, monkeypatch
):
    row = await _registry_row(db_session)
    monkeypatch.setattr(settings, "RAG_SOURCE_FETCH_ENABLED", False)

    with pytest.raises(SourceSyncError, match="disabled"):
        async with _fetcher() as fetcher:
            await verify_sources(db_session, fetcher=fetcher, source_keys=[row.registry_key])

    async with _fetcher() as fetcher:
        result = await verify_sources(
            db_session, fetcher=fetcher, source_keys=[row.registry_key], force=True
        )
    assert result[0]["verified"] is True
    assert len(result[0]["content_checksums"][0]) == 64
    assert result[0]["declared_checksums_are_content_hashes"] is False


@pytest.mark.asyncio
async def test_verification_refuses_declared_checksum_mismatch(db_session):
    row = await _registry_row(db_session)
    row.source_config = {
        **row.source_config,
        "declared_checksum": "0" * 64,
        "declared_checksum_is_content_hash": True,
    }
    await db_session.commit()

    async with _fetcher() as fetcher:
        result = await verify_sources(
            db_session, fetcher=fetcher, source_keys=[row.registry_key], force=True
        )

    assert result[0]["verified"] is False
    assert result[0]["checksum_mismatches"] == [DOC_URL]
    assert result[0]["content_checksums"] == []
    await db_session.refresh(row)
    assert row.verification_status == "PENDING"
    assert row.failure_count == 1


@pytest.mark.asyncio
async def test_sync_queues_version_for_review_without_indexing(db_session, monkeypatch, tmp_path):
    row = await _registry_row(db_session)
    monkeypatch.setattr(settings, "RAG_SOURCE_FETCH_ENABLED", True)
    storage = LocalStorageProvider(tmp_path / "storage")
    set_storage_provider(storage)
    try:
        async with _fetcher() as fetcher:
            job = await sync_source(
                db_session,
                source_key=row.registry_key,
                fetcher=fetcher,
                enable_verified=True,
                requested_by="test-operator",
            )
    finally:
        set_storage_provider(None)

    assert job.status == "COMPLETED"
    assert job.documents_discovered == 1
    assert job.documents_ingested == 1
    assert job.checkpoint_json[DOC_URL]["status"] == "QUEUED_FOR_REVIEW"

    version = (await db_session.execute(select(LegalDocumentVersion))).scalar_one()
    assert version.status == "PENDING_REVIEW"
    assert version.content_checksum != "metadata-derived-not-a-content-hash"
    assert version.raw_storage_key and await storage.exists(version.raw_storage_key)

    reviews = (await db_session.execute(select(LegalReviewItem))).scalars().all()
    assert [item.reason for item in reviews] == ["NEW_DOCUMENT"]
    assert (await db_session.execute(select(LegalSource))).scalars().all() == []
    assert (await db_session.execute(select(LegalChunk))).scalars().all() == []

    await db_session.refresh(row)
    assert row.verification_status == "VERIFIED"
    assert row.enabled is True


@pytest.mark.asyncio
async def test_admin_promotion_indexes_reviewed_version(db_session, monkeypatch, tmp_path):
    row = await _registry_row(db_session)
    monkeypatch.setattr(settings, "RAG_SOURCE_FETCH_ENABLED", True)
    storage = LocalStorageProvider(tmp_path / "storage")
    set_storage_provider(storage)
    try:
        async with _fetcher() as fetcher:
            await sync_source(db_session, source_key=row.registry_key, fetcher=fetcher)
        version = (await db_session.execute(select(LegalDocumentVersion))).scalar_one()
        result = await ingest_document_version(
            db_session, version_id=version.id, actor="admin:test"
        )
    finally:
        set_storage_provider(None)

    assert result["status"] == "INDEXED"
    assert result["chunks_extracted"] >= 1
    await db_session.refresh(version)
    assert version.status == "INDEXED"
    assert version.legal_source_id is not None
    assert (await db_session.execute(select(LegalChunk))).scalars().all()

    review = (await db_session.execute(select(LegalReviewItem))).scalar_one()
    assert review.status == "RESOLVED"
    assert review.resolved_by == "admin:test"

    jobs = (await db_session.execute(select(LegalSyncJob))).scalars().all()
    assert len(jobs) == 1
    assert jobs[0].status == "COMPLETED"
