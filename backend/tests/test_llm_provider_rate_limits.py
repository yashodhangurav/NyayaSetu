"""Rate-limit, token-budget, and fallback-quality regression tests for LLM providers."""

import pytest
import httpx

from app.core.config import settings
from app.modules.legal_assistant import llm_provider
from app.modules.legal_assistant.llm_provider import (
    DeterministicGroundedLLMProvider,
    GroqLLMProvider,
)
from app.modules.legal_assistant.schemas import LegalAskResponse


RATE_LIMIT_MESSAGE = "The AI service is temporarily rate-limited. Please try again shortly."


def _chunk(number: int = 1) -> dict:
    return {
        "chunk_id": f"chk_ni_{number}",
        "act": "Negotiable Instruments Act, 1881",
        "source_title": "Negotiable Instruments Act, 1881",
        "section": "Section 138",
        "section_number": "Section 138",
        "clause_heading": "Dishonour of cheque for insufficiency of funds",
        "chunk_text": (
            "Dishonour of cheque for insufficiency, etc., of funds in the account. "
            "Where any cheque drawn by a person on an account maintained by him is returned "
            "unpaid by the banker, that person shall be deemed to have committed an offence."
        ),
        "content_checksum": f"checksum-{number}",
        "official_source_url": "https://www.indiacode.nic.in/",
    }


def _success_payload() -> dict:
    return {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "content": (
                        '{"answer":"Section 138 concerns cheque dishonour.",'
                        '"legal_points":[{"explanation":"Check the bank return memo.",'
                        '"source_number":1}],"documents_to_gather":["Bank return memo"],'
                        '"facts_to_confirm":[],"decision_badge":"Advocate advised",'
                        '"next_steps":[],"cited_source_numbers":[1],'
                        '"confidence_level":"HIGH","follow_ups":[]}'
                    )
                },
            }
        ]
    }


def _response(status_code: int, payload: dict | None = None, headers: dict | None = None) -> httpx.Response:
    return httpx.Response(
        status_code,
        request=httpx.Request("POST", "https://api.groq.com/openai/v1/chat/completions"),
        json=payload or {},
        headers=headers,
    )


def _configure_provider(monkeypatch, **overrides):
    defaults = {
        "GROQ_MAX_COMPLETION_TOKENS": 800,
        "GROQ_MAX_RETRIES": 1,
        "GROQ_RETRY_BACKOFF_SECONDS": 15.0,
        "GROQ_RETRY_JITTER_SECONDS": 0.0,
        "GROQ_REQUEST_TIMEOUT_SECONDS": 20.0,
        "GROQ_OUTPUT_TOKEN_BUDGET_PER_MINUTE": 1000,
        "GROQ_MAX_CONTEXT_CHUNKS": 5,
        "GROQ_MAX_CONTEXT_CHARS": 8000,
        "GROQ_MAX_CHUNK_CHARS": 1400,
    }
    defaults.update(overrides)
    for key, value in defaults.items():
        monkeypatch.setattr(settings, key, value)
    return GroqLLMProvider(api_key="test-key")


def test_successful_generation_uses_configured_token_budget(monkeypatch):
    provider = _configure_provider(monkeypatch)
    captured: dict = {}

    def post(url, *, headers, json, timeout):
        captured.update(json)
        captured["timeout"] = timeout
        return _response(200, _success_payload())

    monkeypatch.setattr(llm_provider.httpx, "post", post)

    result = provider.generate_legal_answer("What is cheque bounce under Section 138?", [_chunk()])

    assert captured["max_completion_tokens"] == 800
    assert captured["timeout"] == 20.0
    assert result["generation_status"] == "ok"
    assert result["answer"].startswith("Section 138 concerns cheque dishonour.")
    assert result["cited_references"][0]["content_checksum"] == "checksum-1"


def test_groq_429_with_retry_after_is_retried(monkeypatch):
    provider = _configure_provider(monkeypatch)
    sleeps: list[float] = []
    calls = 0

    def post(url, *, headers, json, timeout):
        nonlocal calls
        calls += 1
        if calls == 1:
            return _response(429, {"error": {"message": "Rate limited"}}, {"Retry-After": "2"})
        return _response(200, _success_payload())

    monkeypatch.setattr(llm_provider.httpx, "post", post)
    monkeypatch.setattr(llm_provider.time, "sleep", sleeps.append)

    result = provider.generate_legal_answer("cheque bounce", [_chunk()])

    assert calls == 2
    assert sleeps == [2.0]
    assert result["generation_status"] == "ok"


def test_groq_429_without_retry_after_uses_configured_backoff(monkeypatch):
    provider = _configure_provider(monkeypatch)
    sleeps: list[float] = []
    calls = 0

    def post(url, *, headers, json, timeout):
        nonlocal calls
        calls += 1
        if calls == 1:
            return _response(429, {"error": {"message": "Rate limit reached"}})
        return _response(200, _success_payload())

    monkeypatch.setattr(llm_provider.httpx, "post", post)
    monkeypatch.setattr(llm_provider.time, "sleep", sleeps.append)

    result = provider.generate_legal_answer("cheque bounce", [_chunk()])

    assert calls == 2
    assert sleeps == [15.0]
    assert result["generation_status"] == "ok"


def test_groq_429_retry_exhaustion_returns_structured_error_without_fallback(monkeypatch):
    provider = _configure_provider(monkeypatch)
    sleeps: list[float] = []
    calls = 0

    def post(url, *, headers, json, timeout):
        nonlocal calls
        calls += 1
        return _response(429, {"error": {"message": "Rate limit reached"}})

    monkeypatch.setattr(llm_provider.httpx, "post", post)
    monkeypatch.setattr(llm_provider.time, "sleep", sleeps.append)
    monkeypatch.setattr(
        provider._fallback,
        "generate_legal_answer",
        lambda *args, **kwargs: pytest.fail("Rate limits must not use deterministic fallback"),
    )

    result = provider.generate_legal_answer("cheque bounce", [_chunk()])

    assert calls == 2
    assert sleeps == [15.0]
    assert result["generation_status"] == "rate_limited"
    assert result["answer"] == RATE_LIMIT_MESSAGE
    assert result["generation_error"] == RATE_LIMIT_MESSAGE
    assert result["is_retryable"] is True
    assert result["retry_after_seconds"] is not None
    assert result["cited_references"] == []


def test_groq_429_with_long_retry_after_returns_immediately(monkeypatch):
    provider = _configure_provider(monkeypatch)
    calls = 0
    sleeps: list[float] = []

    def post(url, *, headers, json, timeout):
        nonlocal calls
        calls += 1
        return _response(429, {"error": {"message": "Rate limited"}}, {"Retry-After": "90"})

    monkeypatch.setattr(llm_provider.httpx, "post", post)
    monkeypatch.setattr(llm_provider.time, "sleep", sleeps.append)

    result = provider.generate_legal_answer("cheque bounce", [_chunk()])

    assert calls == 1
    assert sleeps == []
    assert result["generation_status"] == "rate_limited"
    assert result["retry_after_seconds"] == 90.0


def test_groq_timeout_returns_distinct_retryable_error(monkeypatch):
    provider = _configure_provider(monkeypatch)

    def post(url, *, headers, json, timeout):
        raise httpx.TimeoutException("request timed out")

    monkeypatch.setattr(llm_provider.httpx, "post", post)
    monkeypatch.setattr(
        provider._fallback,
        "generate_legal_answer",
        lambda *args, **kwargs: pytest.fail("Timeouts must not use deterministic fallback"),
    )

    result = provider.generate_legal_answer("cheque bounce", [_chunk()])

    assert result["generation_status"] == "timeout"
    assert result["is_retryable"] is True
    assert "took too long" in result["generation_error"]


def test_groq_provider_failure_returns_distinct_retryable_error(monkeypatch):
    provider = _configure_provider(monkeypatch)

    def post(url, *, headers, json, timeout):
        return _response(503, {"error": {"message": "upstream unavailable"}})

    monkeypatch.setattr(llm_provider.httpx, "post", post)
    monkeypatch.setattr(
        provider._fallback,
        "generate_legal_answer",
        lambda *args, **kwargs: pytest.fail("Provider failures must not use deterministic fallback"),
    )

    result = provider.generate_legal_answer("cheque bounce", [_chunk()])

    assert result["generation_status"] == "provider_unavailable"
    assert result["is_retryable"] is True
    assert "temporarily unavailable" in result["generation_error"]


def test_cumulative_output_budget_blocks_immediate_second_request(monkeypatch):
    provider = _configure_provider(monkeypatch, GROQ_OUTPUT_TOKEN_BUDGET_PER_MINUTE=900)
    calls = 0
    monkeypatch.setattr(llm_provider.time, "sleep", lambda _seconds: pytest.fail("No retry expected"))

    def post(url, *, headers, json, timeout):
        nonlocal calls
        calls += 1
        return _response(200, _success_payload())

    monkeypatch.setattr(llm_provider.httpx, "post", post)

    first = provider.generate_legal_answer("cheque bounce", [_chunk()])
    second = provider.generate_legal_answer("cheque bounce again", [_chunk()])

    assert first["generation_status"] == "ok"
    assert calls == 1
    assert second["generation_status"] == "rate_limited"
    assert second["answer"] == RATE_LIMIT_MESSAGE
    assert second["is_retryable"] is True


def test_context_is_bounded_to_configured_limit(monkeypatch):
    provider = _configure_provider(monkeypatch, GROQ_MAX_CONTEXT_CHUNKS=1)
    captured: dict = {}

    def post(url, *, headers, json, timeout):
        captured.update(json)
        return _response(200, _success_payload())

    monkeypatch.setattr(llm_provider.httpx, "post", post)

    provider.generate_legal_answer("cheque bounce", [_chunk(1), _chunk(2)])

    user_prompt = captured["messages"][1]["content"]
    assert "[1]" in user_prompt
    assert "checksum-2" not in user_prompt


def test_conversation_context_is_bounded_and_excludes_identifiers(monkeypatch):
    provider = _configure_provider(monkeypatch)
    captured: dict = {}

    def post(url, *, headers, json, timeout):
        captured.update(json)
        return _response(200, _success_payload())

    monkeypatch.setattr(llm_provider.httpx, "post", post)

    provider.generate_legal_answer(
        "cheque bounce",
        [_chunk()],
        conversation_context={
            "legal_domain": "CRIMINAL_LAW",
            "dispute_category": "cheque bounce",
            "jurisdiction": {"state": "Karnataka", "district": "Belagavi"},
            "confirmed_facts": {
                "amount": "50000",
                "full_name": "Aadhaar Number 123456789012",
                "phone": "+919999999999",
            },
        },
    )

    user_prompt = captured["messages"][1]["content"]
    assert "VERIFIED SESSION FACTS" in user_prompt
    assert "CRIMINAL_LAW" in user_prompt
    assert "amount=50000" in user_prompt
    assert "Aadhaar" not in user_prompt
    assert "+919999999999" not in user_prompt
    assert len(user_prompt) < 6000


def test_deterministic_fallback_is_clean_and_limited(monkeypatch):
    chunk = _chunk()
    chunk["chunk_text"] = "**Dishonour** of cheque. The bank returned the cheque unpaid."

    result = DeterministicGroundedLLMProvider().generate_legal_answer("cheque bounce", [chunk])

    assert "**" not in result["answer"]
    assert "the law provides that" not in result["answer"].lower()
    assert "Limited, non-AI-generated legal information" in result["answer"]
    assert "not a personalized legal conclusion" in result["answer"].lower()
    assert len(result["cited_references"]) == 1


@pytest.mark.asyncio
async def test_api_returns_structured_rate_limit_status(async_client, monkeypatch):
    class RateLimitedProvider:
        provider_name = "RateLimitedTestProvider"
        is_mock = False

        def generate_legal_answer(self, **kwargs):
            return {
                "answer": RATE_LIMIT_MESSAGE,
                "generation_status": "rate_limited",
                "generation_error": RATE_LIMIT_MESSAGE,
                "retry_after_seconds": 15.0,
                "is_retryable": True,
                "confidence_level": "LOW",
                "cited_references": [],
            }

        def explain_legal_document(self, **kwargs):
            return {}

    monkeypatch.setattr(
        "app.modules.legal_assistant.service.get_llm_provider",
        lambda: RateLimitedProvider(),
    )

    response = await async_client.post(
        "/api/v1/legal/ask", json={"query": "What is cheque bounce under Section 138?"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["generation_status"] == "rate_limited"
    assert data["answer"] == RATE_LIMIT_MESSAGE
    assert data["generation_error"] == RATE_LIMIT_MESSAGE
    assert data["retry_after_seconds"] == 15.0
    assert data["is_retryable"] is True
    assert data["citations"] == []
    LegalAskResponse.model_validate(data)
