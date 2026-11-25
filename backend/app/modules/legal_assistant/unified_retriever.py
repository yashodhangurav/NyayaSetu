"""Single retrieval facade reused by the legal assistant and legal search APIs.

The facade keeps the existing database/pgvector path authoritative, falls back to
the bundled offline corpus, applies temporal and authority-aware checks, and
reports evidence sufficiency. Official-source fallback is opt-in and only queues
documents through the reviewed acquisition pipeline; raw web text is never fed
directly to generation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
import re
from typing import Any, Dict, Iterable, List, Optional, Set
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.concurrency import run_in_threadpool

from app.core.config import settings
from app.core.logging import logger
from app.modules.legal_assistant.retrieval import LegalRetrievalEngine
from app.modules.legal_knowledge.models import LegalDocumentVersion, LegalSourceRegistry
from rag.search.hybrid_search import LegalHybridSearchEngine
from rag.search.query_rewriter import LegalQueryRewriter


@dataclass
class RetrievalBundle:
    """Evidence returned by the unified retrieval layer."""

    chunks: List[Dict[str, Any]] = field(default_factory=list)
    source: str = "NONE"
    rewritten_query: str = ""
    sufficient: bool = False
    diagnostics: Dict[str, Any] = field(default_factory=dict)


class UnifiedLegalRetriever:
    """Unified retriever with query understanding, temporal checks, and sufficiency."""

    @classmethod
    async def retrieve(
        cls,
        db: AsyncSession,
        query: str,
        *,
        jurisdiction: Optional[str] = None,
        max_sources: int = 5,
        hybrid_engine: Optional[LegalHybridSearchEngine] = None,
        as_of_date: Optional[date] = None,
    ) -> RetrievalBundle:
        rewritten = LegalQueryRewriter.rewrite(query)
        diagnostics: Dict[str, Any] = {
            "detected_language": rewritten.detected_language,
            "legacy_concordance": rewritten.legacy_concordance_detected,
            "domain_tags": rewritten.domain_tags,
            "out_of_scope": rewritten.is_out_of_scope,
        }
        if rewritten.is_out_of_scope:
            return RetrievalBundle(
                source="OUT_OF_SCOPE",
                rewritten_query=rewritten.expanded_query,
                diagnostics=diagnostics,
            )

        # Primary evidence: verified database/pgvector corpus.
        db_chunks = await LegalRetrievalEngine.retrieve(
            db=db,
            query=rewritten.expanded_query,
            jurisdiction=jurisdiction,
            max_sources=max_sources,
        )
        diagnostics["database_chunks"] = len(db_chunks)
        if db_chunks:
            db_chunks = await cls.apply_temporal_validity(db, db_chunks, as_of_date or date.today())
            db_chunks = cls.apply_explicit_reference_boost(db_chunks, query)
            db_chunks = cls.apply_authority_ranking(db_chunks)
            diagnostics["temporally_valid_chunks"] = len(db_chunks)
            return RetrievalBundle(
                chunks=db_chunks[:max_sources],
                source="VERIFIED_DATABASE",
                rewritten_query=rewritten.expanded_query,
                sufficient=cls.is_sufficient(db_chunks[:max_sources]),
                diagnostics=diagnostics,
            )

        # Secondary evidence: immutable bundled corpus used for offline development.
        offline = await cls.retrieve_offline(
            rewritten.expanded_query,
            jurisdiction=jurisdiction,
            max_sources=max_sources,
            hybrid_engine=hybrid_engine,
            diagnostics=diagnostics,
            domain_tags=rewritten.domain_tags,
            original_query=query,
        )
        offline.rewritten_query = rewritten.expanded_query
        return offline

    @staticmethod
    async def retrieve_offline(
        query: str,
        *,
        jurisdiction: Optional[str] = None,
        max_sources: int = 5,
        hybrid_engine: Optional[LegalHybridSearchEngine] = None,
        diagnostics: Optional[Dict[str, Any]] = None,
        domain_tags: Optional[List[str]] = None,
        original_query: Optional[str] = None,
    ) -> RetrievalBundle:
        """Search only the immutable bundled corpus, without any database access."""
        diagnostics = diagnostics or {}
        engine = hybrid_engine or LegalHybridSearchEngine()
        search_result = await run_in_threadpool(
            lambda: engine.search(
                query=query,
                filter_in_force_only=True,
                jurisdiction=jurisdiction,
                top_k=max_sources,
            )
        )
        confidence = search_result.get("confidence_level")
        diagnostics["bundled_confidence"] = confidence
        results = search_result.get("results", [])
        if not results or confidence == "NO_MATCH":
            return RetrievalBundle(source="BUNDLED_NO_MATCH", diagnostics=diagnostics)

        bundled_chunks = [
            {
                "chunk_id": c.get("chunk_id") or c.get("source_id"),
                "source_title": c.get("act", "Indian Statute"),
                "source_type": c.get("doc_type", "BARE_ACT"),
                "act_or_judgment_identifier": c.get("source_id"),
                "section_number": c.get("section", ""),
                "section_or_paragraph": c.get("section", ""),
                "clause_heading": c.get("clause_heading", ""),
                "chunk_text": c["chunk_text"],
                "relevant_text": c["chunk_text"][:280],
                "jurisdiction": c.get("jurisdiction", "Union of India"),
                "document_version": c.get("document_version", "1.0"),
                "official_source_url": c.get("source_url"),
                "content_checksum": c.get("content_checksum") or c.get("chunk_id"),
                "score": c.get("score"),
                "detected_domain": (domain_tags or [None])[0],
            }
            for c in search_result.get("results", [])
        ]
        # Reciprocal rank fusion of the semantic ranking and a transparent lexical
        # overlap ranking. Both signals come only from the immutable bundled corpus.
        lexical_ranking = sorted(
            bundled_chunks,
            key=lambda c: UnifiedLegalRetriever._lexical_overlap(query, c),
            reverse=True,
        )
        bundled_chunks = UnifiedLegalRetriever.reciprocal_rank_fusion(
            [bundled_chunks, lexical_ranking]
        )
        bundled_chunks = UnifiedLegalRetriever.apply_explicit_reference_boost(
            bundled_chunks, original_query or query
        )
        bundled_chunks = UnifiedLegalRetriever.apply_authority_ranking(bundled_chunks)
        return RetrievalBundle(
            chunks=bundled_chunks[:max_sources],
            source="BUNDLED_CORPUS",
            sufficient=UnifiedLegalRetriever.is_sufficient(bundled_chunks[:max_sources]),
            diagnostics=diagnostics,
        )

    @staticmethod
    async def apply_temporal_validity(
        db: AsyncSession,
        chunks: List[Dict[str, Any]],
        as_of: date,
    ) -> List[Dict[str, Any]]:
        """Filter chunks linked to immutable versions whose validity excludes ``as_of``.

        Legacy curated chunks without a linked document version are retained; they
        predate version tracking and are not silently discarded.
        """
        source_ids: Set[UUID] = set()
        for chunk in chunks:
            raw_id = chunk.get("source_id")
            if raw_id:
                try:
                    source_ids.add(UUID(str(raw_id)))
                except ValueError:
                    continue
        if not source_ids:
            return chunks

        versions = (
            await db.execute(
                select(LegalDocumentVersion).where(
                    LegalDocumentVersion.legal_source_id.in_(source_ids)
                )
            )
        ).scalars().all()
        if not versions:
            return chunks

        by_source: Dict[UUID, List[LegalDocumentVersion]] = {}
        for version in versions:
            if version.legal_source_id:
                by_source.setdefault(version.legal_source_id, []).append(version)

        result: List[Dict[str, Any]] = []
        for chunk in chunks:
            try:
                source_id = UUID(str(chunk.get("source_id")))
            except (ValueError, TypeError):
                result.append(chunk)
                continue
            linked = by_source.get(source_id, [])
            if not linked:
                result.append(chunk)
                continue
            valid = any(
                (v.valid_from is None or v.valid_from <= as_of)
                and (v.valid_until is None or v.valid_until >= as_of)
                for v in linked
            )
            if valid:
                chunk["temporal_valid_as_of"] = as_of.isoformat()
                result.append(chunk)
        return result

    @staticmethod
    def _referenced_sections(query: str) -> Set[str]:
        """Extract explicitly named section numbers from the user's own query."""
        return {
            match.group(1).casefold()
            for match in re.finditer(
                r"\b(?:section|sec\.?)\s*(\d+[a-z]?)", query.casefold()
            )
        }

    @classmethod
    def apply_explicit_reference_boost(
        cls, chunks: List[Dict[str, Any]], query: str
    ) -> List[Dict[str, Any]]:
        """Keep an explicitly cited section ahead of synonym-expansion noise.

        Query expansion may legitimately add related topics, but it must not
        displace the statute section the user actually named. Only the chunk's
        section metadata is boosted; retrieved text is never altered.
        """
        sections = cls._referenced_sections(query)
        for chunk in chunks:
            haystack = " ".join(
                str(chunk.get(key) or "")
                for key in ("section_number", "section_or_paragraph")
            ).casefold()
            matched = [
                section
                for section in sections
                if re.search(rf"\b{re.escape(section)}\b", haystack)
            ]
            chunk["explicit_reference_bonus"] = round(0.25 * len(matched), 6)
        return chunks

    @staticmethod
    def _lexical_overlap(query: str, chunk: Dict[str, Any]) -> float:
        query_tokens = {t for t in re.findall(r"\w+", query.casefold()) if len(t) > 2}
        if not query_tokens:
            return 0.0
        body = " ".join(
            str(chunk.get(key) or "")
            for key in ("source_title", "section_number", "clause_heading", "chunk_text")
        )
        body_tokens = set(re.findall(r"\w+", body.casefold()))
        return len(query_tokens & body_tokens) / len(query_tokens)

    @staticmethod
    def reciprocal_rank_fusion(
        rankings: List[List[Dict[str, Any]]],
        *,
        k: int = 60,
    ) -> List[Dict[str, Any]]:
        """Merge ranked result lists using RRF and preserve a representative chunk."""
        scores: Dict[tuple, float] = {}
        representatives: Dict[tuple, Dict[str, Any]] = {}
        for ranking in rankings:
            for rank, chunk in enumerate(ranking, start=1):
                key = (
                    str(chunk.get("official_source_url") or ""),
                    str(chunk.get("section_number") or ""),
                    str(chunk.get("chunk_id") or ""),
                    (chunk.get("chunk_text") or "")[:120],
                )
                scores[key] = scores.get(key, 0.0) + 1.0 / (k + rank)
                representatives.setdefault(key, chunk)
        fused = [dict(representatives[key]) for key in scores]
        for chunk in fused:
            key = (
                str(chunk.get("official_source_url") or ""),
                str(chunk.get("section_number") or ""),
                str(chunk.get("chunk_id") or ""),
                (chunk.get("chunk_text") or "")[:120],
            )
            chunk["rrf_score"] = round(scores[key], 6)
        return sorted(fused, key=lambda c: c["rrf_score"], reverse=True)

    @staticmethod
    def apply_authority_ranking(chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Apply a small, transparent authority bonus without altering source text."""
        for chunk in chunks:
            meta = chunk.get("metadata_json") or {}
            authority = str(meta.get("authority_level") or chunk.get("authority_level") or "").upper()
            bonus = 0.04 if "TIER 1" in authority or "SUPREME" in authority else 0.0
            explicit_bonus = float(chunk.get("explicit_reference_bonus") or 0.0)
            chunk["authority_bonus"] = bonus
            score = chunk.get("score")
            if isinstance(score, (int, float)):
                chunk["ranked_score"] = round(float(score) + bonus + explicit_bonus, 4)
            else:
                chunk["ranked_score"] = round(
                    float(chunk.get("rrf_score") or 0.0) + bonus + explicit_bonus, 6
                )
        return sorted(
            chunks,
            key=lambda c: c.get("ranked_score", c.get("score") or 0.0),
            reverse=True,
        )

    @staticmethod
    def is_sufficient(chunks: List[Dict[str, Any]]) -> bool:
        if len(chunks) < settings.RAG_EVIDENCE_MIN_CHUNKS:
            return False
        scores = [c.get("score") for c in chunks if isinstance(c.get("score"), (int, float))]
        if not scores:
            return True
        return max(scores) >= settings.RAG_EVIDENCE_MIN_SCORE

    @classmethod
    async def queue_official_fallback(
        cls,
        db: AsyncSession,
        query: str,
        *,
        max_sources: int = 1,
    ) -> List[str]:
        """Opt-in fallback that queues candidate official documents for review only."""
        if not settings.RAG_OFFICIAL_FALLBACK_ENABLED:
            return []
        from app.modules.legal_knowledge.fetcher import SecureFetcher
        from app.modules.legal_knowledge.sync_service import sync_source

        terms = {term.lower() for term in query.split() if len(term) > 4}
        candidates = (
            await db.execute(
                select(LegalSourceRegistry).where(
                    LegalSourceRegistry.enabled.is_(True),
                    LegalSourceRegistry.verification_status == "VERIFIED",
                )
            )
        ).scalars().all()

        queued: List[str] = []
        async with SecureFetcher() as fetcher:
            for source in candidates:
                haystack = f"{source.name} {' '.join(source.legal_domains or [])}".lower()
                if not any(term in haystack for term in terms):
                    continue
                try:
                    job = await sync_source(
                        db,
                        source_key=source.registry_key,
                        fetcher=fetcher,
                        mode="INCREMENTAL",
                        # The fallback flag is itself the explicit operator opt-in.
                        force=True,
                        requested_by="automatic-official-fallback",
                    )
                    queued.append(source.registry_key)
                    logger.info(
                        "Queued official fallback source %s in job %s", source.registry_key, job.id
                    )
                except Exception as exc:
                    logger.warning(
                        "Official fallback sync failed for %s: %s", source.registry_key, exc
                    )
                if len(queued) >= max_sources:
                    break
        return queued
