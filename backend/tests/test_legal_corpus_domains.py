"""Multi-Domain Statutory Corpus Retrieval & Grounding Integration Tests.

Validates that NyayaSetu's legal knowledge base accurately indexes, retrieves,
and grounds inquiries across all 10 priority Indian legal practice domains:
1. Family Law (PWDVA, HMA, HSA)
2. Criminal Law (BNS, BNSS, BSA)
3. Commercial & Contracts (ICA, NI Act)
4. Consumer Protection (CPA 2019)
5. Cyber Law & Data Privacy (IT Act, DPDP Act)
6. Motor Vehicle Law (MV Act - MACT)
7. Property & Civil Law (TPA, Limitation Act, RERA)
8. Legal Aid & Access (NALSA)
9. Employment & Labour (IDA, PGA)
10. Intellectual Property (Copyright Act, Trade Marks Act)
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.legal_assistant.retrieval import LegalRetrievalEngine
from app.modules.legal_knowledge.ingestion import LegalIngestionService


pytestmark = pytest.mark.usefixtures("isolated_embedding_provider")


# ──────────────────────────────────────────────────────────────
# 1. Family Law Domain Tests
# ──────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_family_law_domestic_violence_retrieval(async_client: AsyncClient, db_session: AsyncSession):
    """Verify domestic violence and protection order query retrieves PWDVA 2005."""
    await LegalIngestionService.seed_curated_corpus(db_session)

    res = await async_client.post(
        "/api/v1/legal/ask",
        json={
            "query": "My husband and in-laws are subjecting me to severe domestic violence and threatening to throw me out of the shared household. What protection orders can I get?",
            "preferred_language": "en",
            "max_sources": 3,
        },
    )
    assert res.status_code == 200
    data = res.json()

    assert data["sources_found"] is True
    assert "Domestic Violence" in data["answer"]
    assert any("PWDVA" in c["source_title"] or "Domestic Violence" in c["source_title"] for c in data["citations"])
    assert any(c["is_verified_in_corpus"] for c in data["citations"])

    # Actionable next steps check
    next_steps = " ".join(data["suggested_next_steps"]).lower()
    assert "protection officer" in next_steps or "section 12" in next_steps or "magistrate" in next_steps


@pytest.mark.asyncio
async def test_family_law_hindu_marriage_mutual_divorce(async_client: AsyncClient, db_session: AsyncSession):
    """Verify mutual consent divorce inquiry retrieves Hindu Marriage Act Section 13B."""
    await LegalIngestionService.seed_curated_corpus(db_session)

    res = await async_client.post(
        "/api/v1/legal/ask",
        json={
            "query": "We have been living separately for over a year and want to file for mutual consent divorce. What is the procedure under Hindu Marriage Act?",
            "preferred_language": "en",
            "max_sources": 3,
        },
    )
    assert res.status_code == 200
    data = res.json()

    assert data["sources_found"] is True
    assert any("Hindu Marriage" in c["source_title"] for c in data["citations"])
    assert any("13B" in c["section_or_paragraph"] or "13" in c["section_or_paragraph"] for c in data["citations"])


@pytest.mark.asyncio
async def test_family_law_coparcenary_daughter_succession(async_client: AsyncClient, db_session: AsyncSession):
    """Verify coparcenary property succession query retrieves Hindu Succession Act Section 6."""
    await LegalIngestionService.seed_curated_corpus(db_session)

    chunks = await LegalRetrievalEngine.retrieve(
        db=db_session,
        query="Do married daughters have equal rights as coparceners in ancestral property under Hindu Succession Act?",
        jurisdiction="Union of India",
        max_sources=3,
    )
    assert len(chunks) >= 1
    top_chunk = chunks[0]
    assert "Hindu Succession" in top_chunk["source_title"]
    assert "Section 6" in top_chunk["section_number"]


# ──────────────────────────────────────────────────────────────
# 2. Criminal Law & Evidence Domain Tests
# ──────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_criminal_law_anticipatory_bail_retrieval(async_client: AsyncClient, db_session: AsyncSession):
    """Verify anticipatory bail inquiry retrieves Section 482 BNSS."""
    await LegalIngestionService.seed_curated_corpus(db_session)

    res = await async_client.post(
        "/api/v1/legal/ask",
        json={
            "query": "I apprehend that a false criminal FIR will be registered against me. How can I seek anticipatory bail under BNSS?",
            "preferred_language": "en",
            "max_sources": 3,
        },
    )
    assert res.status_code == 200
    data = res.json()

    assert data["sources_found"] is True
    assert any("BNSS" in c["source_title"] or "Bharatiya Nagarik Suraksha" in c["source_title"] for c in data["citations"])
    assert any("482" in c["section_or_paragraph"] for c in data["citations"])


@pytest.mark.asyncio
async def test_criminal_law_cheating_bns_retrieval(async_client: AsyncClient, db_session: AsyncSession):
    """Verify cheating and fraudulent inducement inquiry retrieves Section 318 BNS."""
    await LegalIngestionService.seed_curated_corpus(db_session)

    chunks = await LegalRetrievalEngine.retrieve(
        db=db_session,
        query="A contractor dishonestly induced me to pay money with false promises and cheated me. What section of Bharatiya Nyaya Sanhita applies?",
        jurisdiction="Union of India",
        max_sources=3,
    )
    assert len(chunks) >= 1
    matched_titles = [c["source_title"] for c in chunks]
    assert any("Bharatiya Nyaya Sanhita" in t for t in matched_titles)


@pytest.mark.asyncio
async def test_criminal_evidence_electronic_records_bsa(async_client: AsyncClient, db_session: AsyncSession):
    """Verify electronic records admissibility inquiry retrieves BSA 2023 Section 63."""
    await LegalIngestionService.seed_curated_corpus(db_session)

    chunks = await LegalRetrievalEngine.retrieve(
        db=db_session,
        query="What certificate is required to submit electronic WhatsApp and computer evidence in court under Bharatiya Sakshya Adhiniyam?",
        jurisdiction="Union of India",
        max_sources=3,
    )
    assert len(chunks) >= 1
    assert any("Bharatiya Sakshya" in c["source_title"] for c in chunks)


# ──────────────────────────────────────────────────────────────
# 3. Commercial & Contract Law Tests
# ──────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_commercial_contract_breach_and_damages(async_client: AsyncClient, db_session: AsyncSession):
    """Verify breach of contract compensation inquiry retrieves Section 73 Indian Contract Act."""
    await LegalIngestionService.seed_curated_corpus(db_session)

    res = await async_client.post(
        "/api/v1/legal/ask",
        json={
            "query": "A vendor committed a fundamental breach of contract causing severe business financial loss. What compensation is payable under Indian Contract Act?",
            "preferred_language": "en",
            "max_sources": 3,
        },
    )
    assert res.status_code == 200
    data = res.json()

    assert data["sources_found"] is True
    assert any("Indian Contract Act" in c["source_title"] for c in data["citations"])
    assert any("73" in c["section_or_paragraph"] or "10" in c["section_or_paragraph"] for c in data["citations"])


# ──────────────────────────────────────────────────────────────
# 4. Cyber Law & Data Privacy Tests
# ──────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_cyber_law_identity_theft_and_personation(async_client: AsyncClient, db_session: AsyncSession):
    """Verify cyber phishing and identity theft inquiry retrieves Section 66C/66D IT Act."""
    await LegalIngestionService.seed_curated_corpus(db_session)

    res = await async_client.post(
        "/api/v1/legal/ask",
        json={
            "query": "A fraudster stolen my password and electronic identity to cheat people online. What are the provisions under Information Technology Act for identity theft?",
            "preferred_language": "en",
            "max_sources": 3,
        },
    )
    assert res.status_code == 200
    data = res.json()

    assert data["sources_found"] is True
    assert any("Information Technology Act" in c["source_title"] for c in data["citations"])
    assert any("66C" in c["section_or_paragraph"] or "66D" in c["section_or_paragraph"] or "43" in c["section_or_paragraph"] for c in data["citations"])

    # Check actionable cyber steps
    next_steps = " ".join(data["suggested_next_steps"]).lower()
    assert "cyber" in next_steps or "police" in next_steps


@pytest.mark.asyncio
async def test_data_privacy_dpdp_consent_rights(async_client: AsyncClient, db_session: AsyncSession):
    """Verify digital personal data consent inquiry retrieves Section 6 DPDPA 2023."""
    await LegalIngestionService.seed_curated_corpus(db_session)

    chunks = await LegalRetrievalEngine.retrieve(
        db=db_session,
        query="What are the requirements for free and informed consent of Data Principal under Digital Personal Data Protection Act?",
        jurisdiction="Union of India",
        max_sources=3,
    )
    assert len(chunks) >= 1
    assert any("Digital Personal Data" in c["source_title"] for c in chunks)


# ──────────────────────────────────────────────────────────────
# 5. Motor Vehicle Law Tests
# ──────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_motor_vehicle_accident_mact_compensation(async_client: AsyncClient, db_session: AsyncSession):
    """Verify road accident compensation inquiry retrieves Motor Vehicles Act MACT provisions."""
    await LegalIngestionService.seed_curated_corpus(db_session)

    res = await async_client.post(
        "/api/v1/legal/ask",
        json={
            "query": "My family member suffered grievous hurt in a road accident. What is the time limit to file a compensation claim before MACT under Motor Vehicles Act?",
            "preferred_language": "en",
            "max_sources": 3,
        },
    )
    assert res.status_code == 200
    data = res.json()

    assert data["sources_found"] is True
    assert any("Motor Vehicles Act" in c["source_title"] for c in data["citations"])
    assert any("166" in c["section_or_paragraph"] or "164" in c["section_or_paragraph"] for c in data["citations"])

    next_steps = " ".join(data["suggested_next_steps"]).lower()
    assert "mact" in next_steps or "accident" in next_steps


# ──────────────────────────────────────────────────────────────
# 6. Employment & Labour Law Tests
# ──────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_labour_law_workman_retrenchment(async_client: AsyncClient, db_session: AsyncSession):
    """Verify sudden workman termination inquiry retrieves Section 25F Industrial Disputes Act."""
    await LegalIngestionService.seed_curated_corpus(db_session)

    res = await async_client.post(
        "/api/v1/legal/ask",
        json={
            "query": "A factory abruptly terminated a workman with 3 years continuous service without notice or compensation. What are retrenchment conditions under Industrial Disputes Act?",
            "preferred_language": "en",
            "max_sources": 3,
        },
    )
    assert res.status_code == 200
    data = res.json()

    assert data["sources_found"] is True
    assert any("Industrial Disputes Act" in c["source_title"] for c in data["citations"])
    assert any("25F" in c["section_or_paragraph"] for c in data["citations"])


@pytest.mark.asyncio
async def test_labour_law_gratuity_continuous_service(async_client: AsyncClient, db_session: AsyncSession):
    """Verify 5-year gratuity eligibility inquiry retrieves Section 4 Payment of Gratuity Act."""
    await LegalIngestionService.seed_curated_corpus(db_session)

    chunks = await LegalRetrievalEngine.retrieve(
        db=db_session,
        query="Is an employee who resigned after 5 years of continuous service entitled to payment of gratuity?",
        jurisdiction="Union of India",
        max_sources=3,
    )
    assert len(chunks) >= 1
    assert any("Payment of Gratuity" in c["source_title"] for c in chunks)
    assert any("Section 4" in c["section_number"] for c in chunks)


# ──────────────────────────────────────────────────────────────
# 7. Property & Civil Law Tests
# ──────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_property_lease_termination_notice(async_client: AsyncClient, db_session: AsyncSession):
    """Verify tenancy lease termination notice inquiry retrieves Section 106 Transfer of Property Act."""
    await LegalIngestionService.seed_curated_corpus(db_session)

    res = await async_client.post(
        "/api/v1/legal/ask",
        json={
            "query": "How many days notice is required to terminate a month to month lease of immovable property under Transfer of Property Act?",
            "preferred_language": "en",
            "max_sources": 3,
        },
    )
    assert res.status_code == 200
    data = res.json()

    assert data["sources_found"] is True
    assert any("Transfer of Property Act" in c["source_title"] for c in data["citations"])
    assert any("106" in c["section_or_paragraph"] for c in data["citations"])


@pytest.mark.asyncio
async def test_limitation_condonation_of_delay(async_client: AsyncClient, db_session: AsyncSession):
    """Verify appeal delay condonation inquiry retrieves Section 5 Limitation Act."""
    await LegalIngestionService.seed_curated_corpus(db_session)

    chunks = await LegalRetrievalEngine.retrieve(
        db=db_session,
        query="Can a court condone delay in filing an appeal if there was sufficient cause under Limitation Act Section 5?",
        jurisdiction="Union of India",
        max_sources=3,
    )
    assert len(chunks) >= 1
    assert any("Limitation Act" in c["source_title"] for c in chunks)
    assert any("Section 5" in c["section_number"] for c in chunks)


# ──────────────────────────────────────────────────────────────
# 8. Intellectual Property Law Tests
# ──────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_copyright_fair_dealing_exceptions(async_client: AsyncClient, db_session: AsyncSession):
    """Verify fair dealing research exception inquiry retrieves Section 52 Copyright Act."""
    await LegalIngestionService.seed_curated_corpus(db_session)

    res = await async_client.post(
        "/api/v1/legal/ask",
        json={
            "query": "Does using an excerpt of a book for private study and fair dealing criticism constitute copyright infringement under Copyright Act?",
            "preferred_language": "en",
            "max_sources": 3,
        },
    )
    assert res.status_code == 200
    data = res.json()

    assert data["sources_found"] is True
    assert any("Copyright Act" in c["source_title"] for c in data["citations"])
    assert any("52" in c["section_or_paragraph"] for c in data["citations"])


@pytest.mark.asyncio
async def test_trademark_infringement_deceptively_similar(async_client: AsyncClient, db_session: AsyncSession):
    """Verify trademark infringement inquiry retrieves Section 29 Trade Marks Act."""
    await LegalIngestionService.seed_curated_corpus(db_session)

    chunks = await LegalRetrievalEngine.retrieve(
        db=db_session,
        query="What constitutes infringement of a registered trade mark by a deceptively similar mark in trade under Trade Marks Act?",
        jurisdiction="Union of India",
        max_sources=3,
    )
    assert len(chunks) >= 1
    assert any("Trade Marks Act" in c["source_title"] for c in chunks)
    assert any("Section 29" in c["section_number"] for c in chunks)


# ──────────────────────────────────────────────────────────────
# 9. Legal Aid & Lok Adalat Finality Tests
# ──────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_lok_adalat_award_finality_and_court_fee_refund(async_client: AsyncClient, db_session: AsyncSession):
    """Verify Lok Adalat settlement finality inquiry retrieves Section 21 Legal Services Authorities Act."""
    await LegalIngestionService.seed_curated_corpus(db_session)

    chunks = await LegalRetrievalEngine.retrieve(
        db=db_session,
        query="Is an award passed by Lok Adalat appealable and is court fee refunded under Legal Services Authorities Act?",
        jurisdiction="Union of India",
        max_sources=3,
    )
    assert len(chunks) >= 1
    assert any("Legal Services Authorities" in c["source_title"] for c in chunks)
    assert any("21" in c["section_number"] for c in chunks)
