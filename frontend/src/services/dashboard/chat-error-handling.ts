export const RATE_LIMIT_MESSAGE = "The AI service is temporarily rate-limited. Please try again shortly.";
export const PROVIDER_UNAVAILABLE_MESSAGE = "The AI service is temporarily unavailable. Please try again shortly.";
export const TIMEOUT_MESSAGE = "The assistant took too long to respond. Please retry.";

export type AssistantFailureStatus =
  | "rate_limited"
  | "timeout"
  | "provider_unavailable"
  | "generation_error";

export interface AssistantFailure {
  message: string;
  status: AssistantFailureStatus;
  retryable: boolean;
  retryAfterSeconds?: number;
}

export class AssistantServiceError extends Error {
  readonly failure: AssistantFailure;

  constructor(failure: AssistantFailure) {
    super(failure.message);
    this.name = "AssistantServiceError";
    this.failure = failure;
  }
}

function asRecord(value: unknown): Record<string, unknown> | null {
  return value !== null && typeof value === "object" ? (value as Record<string, unknown>) : null;
}

function statusFromValue(value: unknown): AssistantFailureStatus | null {
  if (value === "rate_limited" || value === "timeout" || value === "provider_unavailable" || value === "generation_error") {
    return value;
  }
  return null;
}

export function getAssistantFailureFromResponse(response: unknown): AssistantFailure | null {
  const data = asRecord(response);
  if (!data) return null;

  const status = statusFromValue(data.generation_status);
  const answer = typeof data.answer === "string" ? data.answer : "";
  const generationError = typeof data.generation_error === "string" ? data.generation_error : "";
  const retryAfter = typeof data.retry_after_seconds === "number" ? data.retry_after_seconds : undefined;
  const retryable = typeof data.is_retryable === "boolean" ? data.is_retryable : true;

  if (status === "rate_limited" || answer === RATE_LIMIT_MESSAGE || generationError === RATE_LIMIT_MESSAGE) {
    return {
      message: RATE_LIMIT_MESSAGE,
      status: "rate_limited",
      retryable: true,
      retryAfterSeconds: retryAfter,
    };
  }

  if (status === "timeout") {
    return { message: generationError || TIMEOUT_MESSAGE, status: "timeout", retryable };
  }

  if (status === "provider_unavailable" || status === "generation_error") {
    return {
      message: generationError || answer || PROVIDER_UNAVAILABLE_MESSAGE,
      status,
      retryable,
    };
  }

  return null;
}

export function getAssistantFailure(error: unknown): AssistantFailure | null {
  if (error instanceof AssistantServiceError) return error.failure;

  const data = asRecord(error);
  if (!data) return null;

  const statusCode = typeof data.status === "number" ? data.status : undefined;
  const errorName = typeof data.name === "string" ? data.name : "";
  const message = typeof data.message === "string" ? data.message : "";

  if (statusCode === 429) {
    return { message: RATE_LIMIT_MESSAGE, status: "rate_limited", retryable: true };
  }

  if (statusCode === 408 || errorName === "TimeoutError" || /timed?\s*out|timeout/i.test(message)) {
    return { message: TIMEOUT_MESSAGE, status: "timeout", retryable: true };
  }

  if (statusCode !== undefined && statusCode >= 500) {
    return { message: PROVIDER_UNAVAILABLE_MESSAGE, status: "provider_unavailable", retryable: true };
  }

  return null;
}
