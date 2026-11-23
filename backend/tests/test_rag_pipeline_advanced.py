"""Source selection, disambiguation and fallback behavior for legal retrieval."""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.legal_assistant.retrieval import LegalRetrievalEngine
from app.modules.legal_knowledge.ingestion import LegalIngestionService
from app.modules.legal_knowledge.models import LegalSource


pytestmark = pytest.mark.usefixtures("isolated_embedding_provider")


@pytest.mark.asyncio
async def test_disambiguation_section_12_domestic_violence_vs_legal_aid(db_session: AsyncSession):
    """When user asks for 'Section 12' in a domestic violence context, retrieve PWDVA, NOT NALSA."""
    await LegalIngestionService.seed_curated_corpus(db_session)

    # 1. Domestic violence query mentioning Section 12
    dv_chunks = await LegalRetrievalEngine.retrieve(
        db=db_session,
        query="What reliefs can an aggrieved woman claim by presenting an application under Section 12 for domestic violence?",
        jurisdiction="Union of India",
        max_sources=3,
    )
    assert len(dv_chunks) >= 1
    top_dv = dv_chunks[0]
    assert "Domestic Violence" in top_dv["source_title"]
    assert "Section 12" in top_dv["section_number"]

    # 2. Legal aid query mentioning Section 12
    aid_chunks = await LegalRetrievalEngine.retrieve(
        db=db_session,
        query="What are the criteria for free legal aid and who is entitled under Section 12 of Legal Services Authorities Act?",
        jurisdiction="Union of India",
        max_sources=3,
    )
    assert len(aid_chunks) >= 1
    top_aid = aid_chunks[0]
    assert "Legal Services Authorities" in top_aid["source_title"]
    assert "Section 12" in top_aid["section_number"]


@pytest.mark.asyncio
async def test_multi_statute_retrieval_contract_and_limitation(db_session: AsyncSession):
    """A commercial contract dispute involving delay and limitation should retrieve both ICA and Limitation Act."""
    await LegalIngestionService.seed_curated_corpus(db_session)

    chunks = await LegalRetrievalEngine.retrieve(
        db=db_session,
        query="The supplier breached our contract causing severe financial loss, but 2 years have passed. Can I sue for breach and what is the limitation period under Article 54?",
        jurisdiction="Union of India",
        max_sources=4,
    )
    assert len(chunks) >= 2
    titles = [c["source_title"] for c in chunks]
    assert any("Indian Contract Act" in t for t in titles)
    assert any("Limitation Act" in t for t in titles)


@pytest.mark.asyncio
async def test_no_corpus_coverage_safe_fallback(async_client: AsyncClient, db_session: AsyncSession):
    """Uncovered queries (e.g. quantum physics, outer space salvage) must return safe fallback without hallucination."""
    await LegalIngestionService.seed_curated_corpus(db_session)

    res = await async_client.post(
        "/api/v1/legal/ask",
        json={
            "query": "What are the salvage regulations for capturing deep space asteroids in orbital outer space under galactic space law?",
            "preferred_language": "en",
        },
    )
    assert res.status_code == 200
    data = res.json()

    assert data["sources_found"] is False
    assert len(data["citations"]) == 0
    assert "does not contain sufficient" in data["answer"].lower() or "no verified legal sources" in data["answer"].lower()
    # Check that it asks for missing facts or advises advocate consultation
    assert any("advocate" in step.lower() for step in data["suggested_next_steps"])


@pytest.mark.asyncio
async def test_fabricated_or_invalid_section_numbers(async_client: AsyncClient, db_session: AsyncSession):
    """Querying a non-existent section (e.g. Section 9999 of NI Act) should not retrieve fake sections."""
    await LegalIngestionService.seed_curated_corpus(db_session)

    res = await async_client.post(
        "/api/v1/legal/ask",
        json={
            "query": "What is the penalty for dishonour under Section 9999 of the Negotiable Instruments Act?",
            "preferred_language": "en",
        },
    )
    assert res.status_code == 200
    data = res.json()

    # Section 9999 must NOT be in verified citations
    for cit in data["citations"]:
        assert "9999" not in (cit["section_or_paragraph"] or "")


@pytest.mark.asyncio
async def test_rejected_source_filtered_from_retrieval(db_session: AsyncSession):
    """Sources marked as REJECTED in verification_status must be excluded from retrieval."""
    await LegalIngestionService.seed_curated_corpus(db_session)

    # Ingest a rejected source
    rejected_source = LegalSource(
        source_type="BARE_ACT",
        title="Repealed Bogus Act",
        short_code="BOGUS_ACT",
        jurisdiction="Union of India",
        verification_status="REJECTED",
        ingestion_status="COMPLETED",
    )
    db_session.add(rejected_source)
    await db_session.flush()

    chunks = await LegalRetrievalEngine.retrieve(
        db=db_session,
        query="What are the provisions under Repealed Bogus Act?",
        jurisdiction="Union of India",
    )
    assert not any(c["source_title"] == "Repealed Bogus Act" for c in chunks)


@pytest.mark.asyncio
async def test_relevance_threshold_filters_out_poor_matches(db_session: AsyncSession):
    """When relevance_threshold is set strictly high, low-similarity noise chunks are discarded."""
    await LegalIngestionService.seed_curated_corpus(db_session)

    # Completely unrelated query with standard threshold vs strict threshold
    standard_chunks = await LegalRetrievalEngine.retrieve(
        db=db_session,
        query="astrophysics dark matter galaxy rotation curves",
        relevance_threshold=0.45,
    )
    # Should be empty because composite score is too low
    assert len(standard_chunks) == 0
