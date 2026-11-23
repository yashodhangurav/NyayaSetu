"""Comprehensive test suite for Legal AI Assistant (RAG) and Admin Ingestion."""

import pytest
from httpx import AsyncClient, Request, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.modules.admin.models import AuditLog
from app.modules.legal_assistant.citation_validator import CitationValidator
from app.modules.legal_assistant.llm_provider import GroqLLMProvider
from app.modules.legal_knowledge.ingestion import LegalIngestionService
from app.modules.users.models import User


async def create_user_and_token(
    async_client: AsyncClient,
    db_session: AsyncSession,
    role: str = "CITIZEN",
    email: str = "rag.test@example.com",
) -> tuple[str, str]:
    """Helper to register and login user with specified role."""
    password = "SecurePassword2026"
    user = User(
        full_name="Test User",
        email=email,
        phone="+919876543999" if role == "ADMIN" else "+919876543998",
        password_hash=hash_password(password),
        role=role,
        is_verified=True,
        is_active=True,
    )
    db_session.add(user)
    await db_session.commit()

    login_res = await async_client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert login_res.status_code == 200
    return str(user.id), login_res.json()["access_token"]


@pytest.mark.asyncio
async def test_legal_ask_cheque_bounce_retrieval(async_client: AsyncClient, db_session: AsyncSession):
    """Verify inquiry regarding cheque bounce retrieves Section 138 NI Act with verified citation and next steps."""
    # Ensure corpus seeded
    await LegalIngestionService.seed_curated_corpus(db_session)

    payload = {
        "query": "My business client gave me a cheque of Rs 5 Lakhs which bounced due to insufficient funds. What is the procedure under Section 138?",
        "preferred_language": "en",
        "max_sources": 3,
    }

    res = await async_client.post("/api/v1/legal/ask", json=payload)
    assert res.status_code == 200
    data = res.json()

    assert data["query"] == payload["query"]
    assert data["detected_language"] == "en"
    assert data["sources_found"] is True
    assert "Section 138" in data["answer"]
    assert "Negotiable Instruments Act" in data["answer"]
    assert data["retrieved_chunks_count"] >= 1

    # Verify Citations
    citations = data["citations"]
    assert len(citations) >= 1
    c0 = citations[0]
    assert "Negotiable Instruments Act" in c0["source_title"]
    assert "Section 138" in c0["section_or_paragraph"]
    assert c0["is_verified_in_corpus"] is True
    assert c0["official_source_url"] is not None
    assert "indiacode.nic.in" in c0["official_source_url"]
    assert c0["jurisdiction"] == "Union of India"
    assert c0["document_version"] and len(c0["relevant_text"]) > 20
    assert c0["content_checksum"] is not None

    # Verify Actionable Next Steps
    next_steps = " ".join(data["suggested_next_steps"])
    assert "notice" in next_steps.lower()
    assert "30 days" in next_steps.lower() or "15 days" in next_steps.lower()

    # Verify Mandatory Disclaimer
    assert "does not constitute formal legal advice" in data["disclaimer"]


@pytest.mark.asyncio
async def test_legal_ask_insufficient_sources_returns_safe_fallback(async_client: AsyncClient):
    """Ensure out-of-scope inquiry returns safe fallback without hallucinating or making speculative assertions."""
    payload = {
        "query": "What is the maritime salvage protocol for an extraterrestrial spacecraft in international waters under Neptune Treaty?",
        "preferred_language": "en",
    }

    res = await async_client.post("/api/v1/legal/ask", json=payload)
    assert res.status_code == 200
    data = res.json()

    assert data["sources_found"] is False
    assert len(data["citations"]) == 0
    assert "No verified legal sources found" in data["answer"]
    assert "before I can explain which rule applies" in data["answer"]
    assert data["confidence_level"] == "LOW"
    assert data["facts_to_confirm"] and not data["legal_points"]
    assert any("Consult an empanelled advocate" in step for step in data["suggested_next_steps"])


@pytest.mark.asyncio
async def test_citation_validator_prunes_hallucinations():
    """Verify CitationValidator excludes cited sections that were never part of the retrieved chunks."""
    retrieved_chunks = [
        {
            "section_number": "Section 138",
            "source_title": "The Negotiable Instruments Act, 1881",
            "source_type": "BARE_ACT",
            "act_or_judgment_identifier": "Act No. 26 of 1881",
            "clause_heading": "Dishonour of cheque",
            "official_source_url": "https://indiacode.nic.in",
            "content_checksum": "abc123hash",
        }
    ]

    # LLM claimed both Section 138 (valid) and Section 420 IPC (hallucinated / not retrieved)
    claimed_references = [
        {
            "section_or_paragraph": "Section 138",
            "source_title": "The Negotiable Instruments Act, 1881",
        },
        {
            "section_or_paragraph": "Section 420",
            "source_title": "Indian Penal Code",
        },
    ]

    answer_text = "Under Section 138 of NI Act and also Section 420 of IPC, offences are punishable."

    verified, unverified = CitationValidator.validate_and_filter_citations(
        answer_text=answer_text,
        claimed_references=claimed_references,
        retrieved_chunks=retrieved_chunks,
    )

    # Section 138 is verified
    assert len(verified) == 1
    assert verified[0].section_or_paragraph == "Section 138"
    assert verified[0].is_verified_in_corpus is True

    # Section 420 IPC is flagged and pruned
    assert len(unverified) >= 1
    unverified_text = " ".join(unverified)
    assert "420" in unverified_text


@pytest.mark.asyncio
async def test_language_detection_and_multi_language_support(async_client: AsyncClient, db_session: AsyncSession):
    """Verify Hindi and Kannada queries are detected and answered with correct language metadata."""
    await LegalIngestionService.seed_curated_corpus(db_session)

    # 1. Hindi Query in Devanagari Script
    hindi_res = await async_client.post(
        "/api/v1/legal/ask",
        json={"query": "चेक बाउंस होने पर क्या कानूनी प्रक्रिया है?"},
    )
    assert hindi_res.status_code == 200
    hindi_data = hindi_res.json()
    assert hindi_data["detected_language"] == "hi"
    assert "हिंदी" in hindi_data["answer"]

    # 2. Kannada Query in Kannada Script
    kannada_res = await async_client.post(
        "/api/v1/legal/ask",
        json={"query": "ಗ್ರಾಹಕರ ರಕ್ಷಣಾ ಕಾಯ್ದೆಯಡಿ ದೂರು ದಾಖಲಿಸುವುದು ಹೇಗೆ?"},
    )
    assert kannada_res.status_code == 200
    kannada_data = kannada_res.json()
    assert kannada_data["detected_language"] == "kn"
    assert "ಕನ್ನಡ" in kannada_data["answer"]


@pytest.mark.asyncio
async def test_admin_source_ingestion_workflow(async_client: AsyncClient, db_session: AsyncSession):
    """Verify admin registers legal source, ingests statutory chunk, and lists verified sources."""
    admin_id, admin_token = await create_user_and_token(
        async_client,
        db_session,
        role="ADMIN",
        email="superadmin.rag@nyayasetu.in",
    )

    # 1. Admin creates new legal source
    source_payload = {
        "title": "The Arbitration and Conciliation Act, 1996",
        "source_type": "BARE_ACT",
        "short_code": "ACA_1996",
        "citation": "Act No. 26 of 1996",
        "act_or_judgment_identifier": "Act No. 26 of 1996",
        "jurisdiction": "Union of India",
        "document_version": "2026.1",
        "official_source_url": "https://www.indiacode.nic.in/handle/123456789/1978",
    }

    create_res = await async_client.post(
        "/api/v1/legal/admin/sources",
        json=source_payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert create_res.status_code == 201
    source_id = create_res.json()["id"]

    # 2. Admin ingests chunk
    chunk_payload = {
        "section_number": "Section 9",
        "clause_heading": "Interim measures, etc., by Court",
        "chunk_text": "A party may, before or during arbitral proceedings or at any time after the making of the arbitral award, apply to a court for interim measures of protection.",
    }

    chunk_res = await async_client.post(
        f"/api/v1/legal/admin/sources/{source_id}/chunks",
        json=chunk_payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert chunk_res.status_code == 201
    chunk_data = chunk_res.json()
    assert chunk_data["status"] == "embedded_and_stored"
    assert chunk_data["content_checksum"] is not None

    # 3. Admin lists sources
    list_res = await async_client.get(
        "/api/v1/legal/admin/sources",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert list_res.status_code == 200
    sources_list = list_res.json()
    assert any(s["id"] == source_id for s in sources_list)


@pytest.mark.asyncio
async def test_admin_ingestion_access_control(async_client: AsyncClient, db_session: AsyncSession):
    """Ensure citizens and unauthenticated users cannot access admin knowledge ingestion routes."""
    citizen_id, citizen_token = await create_user_and_token(
        async_client,
        db_session,
        role="CITIZEN",
        email="unauthorized.citizen@example.com",
    )

    # Citizen receives 403 Forbidden
    res_citizen = await async_client.post(
        "/api/v1/legal/admin/sources",
        json={"title": "Test Act", "source_type": "BARE_ACT", "jurisdiction": "Delhi"},
        headers={"Authorization": f"Bearer {citizen_token}"},
    )
    assert res_citizen.status_code == 403

    # Unauthenticated receives 401 Unauthorized
    res_unauth = await async_client.post(
        "/api/v1/legal/admin/sources",
        json={"title": "Test Act", "source_type": "BARE_ACT", "jurisdiction": "Delhi"},
    )
    assert res_unauth.status_code == 401


@pytest.mark.asyncio
async def test_audit_log_recorded_for_legal_ai_queries(async_client: AsyncClient, db_session: AsyncSession):
    """Verify that asking a legal question creates an immutable audit trail entry."""
    await LegalIngestionService.seed_curated_corpus(db_session)

    res = await async_client.post(
        "/api/v1/legal/ask",
        json={"query": "What are the rights of an undertrial prisoner regarding bail?"},
    )
    assert res.status_code == 200

    audit_res = await db_session.execute(
        select(AuditLog).where(
            AuditLog.entity_type == "legal_assistant_rag",
            AuditLog.action == "LEGAL_AI_QUERY_ANSWERED",
        )
    )
    audit = audit_res.scalar_one_or_none()
    assert audit is not None
    assert "undertrial" in audit.payload_snapshot["query"].lower()
    assert audit.payload_snapshot["sources_found"] is True


@pytest.mark.asyncio
async def test_groq_receives_bundled_statute_and_returns_its_citation(async_client, monkeypatch):
    monkeypatch.setattr(
        "app.modules.legal_assistant.service.get_llm_provider",
        lambda: GroqLLMProvider(api_key="test-key"),
    )

    def complete(url, *, headers, json, timeout):
        prompt = json["messages"][1]["content"]
        assert "Section 138" in prompt
        assert "dishonour" in prompt.lower() and len(prompt) > 300
        return Response(
            200,
            request=Request("POST", url),
            json={"choices": [{"finish_reason": "stop", "message": {"content": (
                '{"answer":"Section 138 concerns cheque dishonour.",'
                '"legal_points":[{"explanation":"Check the bank return memo.","source_number":1}],'
                '"documents_to_gather":["Bank return memo"],"facts_to_confirm":["When did you receive the memo?"],'
                '"decision_badge":"ADVOCATE_ADVISED","next_steps":[],'
                '"cited_source_numbers":[1],"confidence_level":"HIGH","follow_ups":[]}'
            )}}]},
        )

    monkeypatch.setattr("app.modules.legal_assistant.llm_provider.httpx.post", complete)
    response = await async_client.post(
        "/api/v1/legal/ask", json={"query": "What is cheque bounce under Section 138?"}
    )
    assert response.status_code == 200
    result = response.json()
    assert result["answer"].startswith("Section 138 concerns cheque dishonour.")
    assert result["decision_badge"] == "Advocate advised"
    assert result["legal_points"][0]["source_checksum"] == result["citations"][0]["content_checksum"]
    assert result["documents_to_gather"] == ["Bank return memo"]
    assert result["facts_to_confirm"] == ["When did you receive the memo?"]
    assert len(result["citations"]) == 1
    assert result["citations"][0]["section_or_paragraph"] == "Section 138"
    assert result["citations"][0]["relevant_text"]


@pytest.mark.asyncio
async def test_chat_greeting_does_not_require_retrieval(async_client, monkeypatch):
    async def unexpected_retrieval(*args, **kwargs):
        pytest.fail("A greeting should be answered before statutory retrieval")

    monkeypatch.setattr(
        "app.modules.legal_assistant.service.LegalRetrievalEngine.retrieve",
        unexpected_retrieval,
    )
    response = await async_client.post("/api/v1/legal/ask", json={"query": "  Hi!  "})

    assert response.status_code == 200
    result = response.json()
    assert result["kind"] == "greeting"
    assert result["answer"].startswith("Hello!")
    assert result["citations"] == []
