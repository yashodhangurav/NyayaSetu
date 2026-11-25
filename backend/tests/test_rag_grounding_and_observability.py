"""Tests for claim support, abstention, and content-free RAG observability."""

import pytest

from app.core.config import settings
from app.core.security import hash_password
from app.modules.legal_assistant.citation_validator import CitationValidator
from app.modules.legal_assistant.observability import RagObservability
from app.modules.users.models import User


CHUNKS = [
    {
        "source_title": "The Negotiable Instruments Act, 1881",
        "section_number": "Section 138",
        "clause_heading": "Dishonour of cheque",
        "chunk_text": (
            "Where any cheque drawn by a person on an account maintained by him is returned by the bank "
            "unpaid due to insufficiency of funds, the drawer shall pay the amount to the payee within "
            "thirty days of receiving notice in writing."
        ),
    }
]


def test_claim_support_flags_only_unsupported_substantive_claims():
    answer = (
        "Under the Negotiable Instruments Act, Section 138 applies when a cheque is returned unpaid "
        "due to insufficiency of funds. The drawer may pay within thirty days of receiving notice. "
        "The leading judgment in Smith v Jones (2020) established a different test."
    )
    supported, unsupported, diagnostics = CitationValidator.verify_claim_support(answer, CHUNKS)

    assert len(supported) == 2
    assert len(unsupported) == 1
    assert "Smith v Jones" in unsupported[0]
    assert diagnostics["support_ratio"] == pytest.approx(2 / 3, abs=0.01)


def test_claim_support_ignores_disclaimer_and_short_citation_fragments():
    answer = (
        "Section 138 concerns cheque dishonour. "
        "This information does not constitute formal legal advice."
    )
    supported, unsupported, diagnostics = CitationValidator.verify_claim_support(answer, CHUNKS)
    assert unsupported == []
    assert diagnostics["claim_count"] <= 1


def test_observability_events_do_not_contain_user_content():
    observer = RagObservability()
    observer.record(
        {
            "request_id": "req-1",
            "query": "My private question with Aadhaar 1234",
            "answer": "Private answer",
            "user_id": "secret-user",
            "retrieval_source": "BUNDLED_CORPUS",
            "sources_found": True,
            "retrieval_sufficient": True,
            "unsupported_claims": 1,
        }
    )
    summary = observer.summary()
    event = summary["recent_events"][0]
    assert "query" not in event and "answer" not in event and "user_id" not in event
    assert event["query_fingerprint"]
    assert summary["counts"]["responses_with_unsupported_claims"] == 1
    assert summary["by_retrieval_source"]["BUNDLED_CORPUS"]["with_sources"] == 1


@pytest.mark.asyncio
async def test_abstention_when_no_citations_and_weak_claim_support(async_client, monkeypatch):
    from app.modules.legal_assistant import service as service_module

    class UnsupportedProvider:
        provider_name = "UnsupportedTestProvider"

        def generate_legal_answer(self, **kwargs):
            return {
                "answer": (
                    "The planets align to create an unlisted planetary tribunal with exclusive "
                    "jurisdiction over all imagined maritime treaties."
                ),
                "sources_found": True,
                "cited_references": [],
                "suggested_next_steps": [],
            }

    monkeypatch.setattr(service_module, "get_llm_provider", lambda: UnsupportedProvider())
    monkeypatch.setattr(settings, "RAG_ABSTAIN_WITHOUT_CITATIONS", True)

    res = await async_client.post(
        "/api/v1/legal/ask",
        json={"query": "What is the procedure under the Neptune Treaty?"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["sources_found"] is False
    assert "will not speculate" in data["answer"]
    assert data["claim_support"]["abstained"] is True
    assert data["confidence_level"] == "LOW"


@pytest.mark.asyncio
async def test_observability_endpoint_is_admin_only(async_client, db_session):
    def make_user(email, role):
        user = User(
            full_name="Observer",
            email=email,
            phone="+919876543000" if role == "ADMIN" else "+919876543001",
            password_hash=hash_password("SecurePassword2026"),
            role=role,
            is_verified=True,
            is_active=True,
        )
        db_session.add(user)
        return user

    admin = make_user("observer.admin@example.com", "ADMIN")
    citizen = make_user("observer.citizen@example.com", "CITIZEN")
    await db_session.commit()

    citizen_token = await _login(async_client, "observer.citizen@example.com")
    admin_token = await _login(async_client, "observer.admin@example.com")

    citizen_res = await async_client.get(
        "/api/v1/legal/admin/observability",
        headers={"Authorization": f"Bearer {citizen_token}"},
    )
    assert citizen_res.status_code == 403

    admin_res = await async_client.get(
        "/api/v1/legal/admin/observability",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert admin_res.status_code == 200
    assert "counts" in admin_res.json()
    assert "recent_events" in admin_res.json()
    assert admin and citizen


async def _login(async_client, email):
    res = await async_client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "SecurePassword2026"},
    )
    assert res.status_code == 200
    return res.json()["access_token"]
