"""Tests for the unified retrieval facade and evidence gates."""

from datetime import date
from types import SimpleNamespace
from uuid import uuid4

import pytest
from sqlalchemy import select

from app.core.config import settings
from app.modules.legal_assistant.unified_retriever import UnifiedLegalRetriever
from app.modules.legal_knowledge.models import LegalDocumentVersion, LegalSourceRegistry
from app.modules.legal_knowledge.source_registry import SourceCandidate, upsert_source_registry


@pytest.mark.asyncio
async def test_out_of_scope_query_is_rejected_before_retrieval(db_session, monkeypatch):
    async def unexpected(*args, **kwargs):
        pytest.fail("Out-of-scope queries must not invoke statutory retrieval")

    monkeypatch.setattr(
        "app.modules.legal_assistant.unified_retriever.LegalRetrievalEngine.retrieve",
        unexpected,
    )
    bundle = await UnifiedLegalRetriever.retrieve(
        db_session,
        "What is the recipe for an extraterrestrial cricket cake?",
        max_sources=3,
    )
    assert bundle.chunks == []
    assert bundle.source == "OUT_OF_SCOPE"
    assert bundle.diagnostics["out_of_scope"] is True


@pytest.mark.asyncio
async def test_temporal_validity_excludes_expired_versions(db_session):
    candidate = SourceCandidate(
        registry_key="SRC_TEMPORAL_TEST",
        name="Temporal Test Act",
        official_domain="www.indiacode.nic.in",
        base_url="https://www.indiacode.nic.in/handle/temporal",
        source_category="CENTRAL_ACT",
        jurisdiction="Union of India",
        legal_domains=[],
        document_types=["CENTRAL_ACT"],
        fetch_strategy="STATIC_DOCUMENT",
        parser_strategy="TXT",
        authority_level="TIER 1",
        supported_languages=["English"],
        update_frequency_hours=168,
        source_config={},
    )
    await upsert_source_registry(db_session, [candidate])
    registry = (
        await db_session.execute(
            select(LegalSourceRegistry).where(LegalSourceRegistry.registry_key == candidate.registry_key)
        )
    ).scalar_one()
    source_id = uuid4()
    db_session.add(
        LegalDocumentVersion(
            registry_key=candidate.registry_key,
            document_key="https://www.indiacode.nic.in/handle/temporal",
            title="Temporal Test Act",
            source_url="https://www.indiacode.nic.in/handle/temporal",
            content_checksum="a" * 64,
            status="INDEXED",
            legal_source_id=source_id,
            valid_from=date(2020, 1, 1),
            valid_until=date(2024, 12, 31),
        )
    )
    await db_session.commit()

    chunks = [
        {"source_id": str(source_id), "score": 0.9, "chunk_text": "current"},
        {"source_id": str(uuid4()), "score": 0.8, "chunk_text": "legacy-without-version"},
    ]
    filtered = await UnifiedLegalRetriever.apply_temporal_validity(
        db_session, chunks, date(2026, 1, 1)
    )
    assert [c["chunk_text"] for c in filtered] == ["legacy-without-version"]


def test_rrf_merges_rank_lists_and_deduplicates_chunks():
    first = {"chunk_id": "a", "chunk_text": "alpha", "section_number": "1"}
    second = {"chunk_id": "b", "chunk_text": "beta", "section_number": "2"}
    fused = UnifiedLegalRetriever.reciprocal_rank_fusion([[first, second], [second, first]])
    assert len(fused) == 2
    assert all(chunk["rrf_score"] > 0 for chunk in fused)
    assert {chunk["chunk_id"] for chunk in fused} == {"a", "b"}


def test_authority_ranking_is_transparent_and_sufficient_gate_is_configurable(monkeypatch):
    chunks = [
        {"score": 0.5, "chunk_text": "lower", "metadata_json": {"authority_level": "TIER 2"}},
        {"score": 0.49, "chunk_text": "higher", "metadata_json": {"authority_level": "TIER 1"}},
    ]
    ranked = UnifiedLegalRetriever.apply_authority_ranking(chunks)
    assert ranked[0]["chunk_text"] == "higher"
    assert ranked[0]["ranked_score"] == 0.53

    monkeypatch.setattr(settings, "RAG_EVIDENCE_MIN_SCORE", 0.6)
    assert UnifiedLegalRetriever.is_sufficient(ranked) is False
    monkeypatch.setattr(settings, "RAG_EVIDENCE_MIN_SCORE", 0.45)
    assert UnifiedLegalRetriever.is_sufficient(ranked) is True


@pytest.mark.asyncio
async def test_official_fallback_force_overrides_disabled_fetch_flag(db_session, monkeypatch):
    candidate = SourceCandidate(
        registry_key="SRC_FALLBACK_TEST",
        name="Temporal Test Act",
        official_domain="www.indiacode.nic.in",
        base_url="https://www.indiacode.nic.in/handle/fallback",
        source_category="CENTRAL_ACT",
        jurisdiction="Union of India",
        legal_domains=["Civil Procedure"],
        document_types=["CENTRAL_ACT"],
        fetch_strategy="STATIC_DOCUMENT",
        parser_strategy="TXT",
        authority_level="TIER 1",
        supported_languages=["English"],
        update_frequency_hours=168,
        source_config={},
    )
    await upsert_source_registry(db_session, [candidate])
    registry = (
        await db_session.execute(
            select(LegalSourceRegistry).where(LegalSourceRegistry.registry_key == candidate.registry_key)
        )
    ).scalar_one()
    registry.enabled = True
    registry.verification_status = "VERIFIED"
    await db_session.commit()

    captured = {}

    class DummyFetcher:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return None

    async def fake_sync_source(db, *, source_key, **kwargs):
        captured["source_key"] = source_key
        captured["force"] = kwargs.get("force")
        return SimpleNamespace(id=uuid4())

    monkeypatch.setattr(settings, "RAG_OFFICIAL_FALLBACK_ENABLED", True)
    monkeypatch.setattr(settings, "RAG_SOURCE_FETCH_ENABLED", False)
    monkeypatch.setattr("app.modules.legal_knowledge.fetcher.SecureFetcher", DummyFetcher)
    monkeypatch.setattr("app.modules.legal_knowledge.sync_service.sync_source", fake_sync_source)

    queued = await UnifiedLegalRetriever.queue_official_fallback(
        db_session, "Temporal procedure question", max_sources=1
    )

    assert queued == ["SRC_FALLBACK_TEST"]
    assert captured == {"source_key": "SRC_FALLBACK_TEST", "force": True}


@pytest.mark.asyncio
async def test_explicit_section_reference_outranks_expansion_noise():
    class FakeSearchEngine:
        def search(self, **kwargs):
            return {
                "confidence_level": "HIGH",
                "results": [
                    {
                        "chunk_id": "rti-7",
                        "act": "Right to Information Act",
                        "section": "Section 7",
                        "chunk_text": "Public information officer duties.",
                    },
                    {
                        "chunk_id": "ni-138",
                        "act": "Negotiable Instruments Act",
                        "section": "Section 138",
                        "chunk_text": "Dishonour of cheque for insufficiency of funds.",
                    },
                ],
            }

    bundle = await UnifiedLegalRetriever.retrieve_offline(
        "cheque bounce Kaveri portal encumbrance certificate form 15",
        hybrid_engine=FakeSearchEngine(),
        original_query="What is cheque bounce under Section 138?",
        max_sources=2,
    )

    assert bundle.chunks[0]["chunk_id"] == "ni-138"
    assert bundle.chunks[0]["explicit_reference_bonus"] == 0.25
