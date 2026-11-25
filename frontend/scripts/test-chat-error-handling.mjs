import test from "node:test";
import assert from "node:assert/strict";

import {
  getAssistantFailure,
  getAssistantFailureFromResponse,
  RATE_LIMIT_MESSAGE,
} from "../src/services/dashboard/chat-error-handling.ts";

test("rate-limited backend response maps to the exact user message and retry", () => {
  const failure = getAssistantFailureFromResponse({
    kind: "answer",
    answer: RATE_LIMIT_MESSAGE,
    generation_status: "rate_limited",
    generation_error: RATE_LIMIT_MESSAGE,
    retry_after_seconds: 15,
    is_retryable: true,
  });

  assert.equal(failure?.message, RATE_LIMIT_MESSAGE);
  assert.equal(failure?.retryable, true);
  assert.equal(failure?.status, "rate_limited");
  assert.equal(failure?.retryAfterSeconds, 15);
});

test("HTTP 429 maps to the rate-limit message and retry", () => {
  const failure = getAssistantFailure({ status: 429, message: "Too Many Requests" });

  assert.equal(failure?.message, RATE_LIMIT_MESSAGE);
  assert.equal(failure?.retryable, true);
  assert.equal(failure?.status, "rate_limited");
});

test("DOMException timeout maps to a distinct timeout message", () => {
  const failure = getAssistantFailure(Object.assign(new DOMException("timeout", "TimeoutError")));

  assert.equal(failure?.status, "timeout");
  assert.equal(failure?.retryable, true);
  assert.match(failure?.message ?? "", /took too long/);
});

test("provider unavailable backend response is retryable but distinct from rate limit", () => {
  const failure = getAssistantFailureFromResponse({
    kind: "answer",
    answer: "The AI service is temporarily unavailable. Please try again shortly.",
    generation_status: "provider_unavailable",
    generation_error: "The AI service is temporarily unavailable. Please try again shortly.",
    is_retryable: true,
  });

  assert.equal(failure?.status, "provider_unavailable");
  assert.notEqual(failure?.message, RATE_LIMIT_MESSAGE);
  assert.equal(failure?.retryable, true);
});

test("insufficient evidence is not presented as a retryable generation failure", () => {
  const failure = getAssistantFailureFromResponse({
    kind: "answer",
    answer: "No verified legal sources found.",
    generation_status: "insufficient_evidence",
    sources_found: false,
  });

  assert.equal(failure, null);
});

test("successful responses have no failure", () => {
  const failure = getAssistantFailureFromResponse({
    kind: "answer",
    answer: "Section 138 concerns cheque dishonour.",
    generation_status: "ok",
    sources_found: true,
  });

  assert.equal(failure, null);
});
