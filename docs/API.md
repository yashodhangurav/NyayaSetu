# FastAPI contract

The registered [versioned router](../backend/app/api/v1/router.py), endpoint decorators and Pydantic schemas define paths, authentication, accepted fields and responses. With `DEBUG=true`, inspect [Swagger UI](http://localhost:8000/docs), [ReDoc](http://localhost:8000/redoc) or the [OpenAPI JSON](http://localhost:8000/api/v1/openapi.json).

## Calling the API

The default prefix is `/api/v1`. The browser uses the [shared API client](../frontend/src/lib/api-client.ts) for bearer tokens, JSON, multipart uploads and typed errors. Domain routes enforce their own roles and resource ownership.

Application errors expose `error.code`, `error.message` and `error.details`. Validation errors return HTTP 422. See the [exception handlers](../backend/app/core/errors.py) for the precise envelope.

## Legal chat

`POST /api/v1/legal/ask` accepts `query` and optional `preferred_language`, `jurisdiction` and `max_sources`. A greeting returns `kind="greeting"`. A legal answer includes a summary and explanations in `answer`, citation records, ordered next steps, optional deadline information and confidence metadata. Each item in `legal_points` carries a `source_checksum` identifying its citation. `documents_to_gather` and `facts_to_confirm` are lists.

The response also carries additive diagnostics: `retrieval_source` (`VERIFIED_DATABASE`, `BUNDLED_CORPUS`, `BUNDLED_NO_MATCH`, `OUT_OF_SCOPE`, or `NONE`), `evidence_sufficient`, and `claim_support` (sentence-level lexical support statistics). When retrieved evidence is insufficient and citations cannot be grounded, the service may return a controlled abstention with `confidence_level="LOW"`; unsupported statements otherwise downgrade confidence to `MEDIUM` with a note. Existing clients can ignore these fields.

Generation outcomes are reported separately in `generation_status`: `ok`, `rate_limited`, `timeout`, `provider_unavailable`, `insufficient_evidence`, or `generation_error`. Provider-transport failures return HTTP 200 with `answer` set to a safe message, `generation_error` mirroring it, `is_retryable`, and optional `retry_after_seconds`; they never substitute a deterministic legal answer. For rate limits the exact user-facing message is `"The AI service is temporarily rate-limited. Please try again shortly."`. The chat UI maps these states to a retry action without dropping the original question or preceding turns.

`GET /api/v1/legal/admin/observability` is ADMIN-only and returns content-free RAG counters plus bounded recent events (hashes and counts only).

Read the [request and response schemas](../backend/app/modules/legal_assistant/schemas.py) for constraints and defaults.

## Official-source registry

All routes below are ADMIN-only and are mounted by [`legal_knowledge/router.py`](../backend/app/modules/legal_knowledge/router.py):

- `POST /api/v1/legal-knowledge/admin/registry/bootstrap` — load declarative CSV candidates. All new rows are `PENDING` and disabled.
- `GET /api/v1/legal-knowledge/admin/registry/sources` — list active registry rows.
- `POST /api/v1/legal-knowledge/admin/registry/verify` — live-check declared document URLs. Requires `source_keys` or `verify_all=true`; `force=true` overrides the disabled-by-default fetch flag for an explicit operator action.
- `POST /api/v1/legal-knowledge/admin/registry/sync` — discover, fetch, checksum, and queue documents for legal review.
- `GET /api/v1/legal-knowledge/admin/registry/jobs` — persistent sync-job checkpoints.
- `GET /api/v1/legal-knowledge/admin/registry/versions` — immutable fetched versions.
- `GET /api/v1/legal-knowledge/admin/registry/review` — review queue.
- `POST /api/v1/legal-knowledge/admin/registry/versions/ingest` — explicitly promote an approved version through the existing ingestion pipeline.

Automated fetching is disabled by default (`RAG_SOURCE_FETCH_ENABLED=false`). Fetched content is never injected directly into generation; it must be reviewed and promoted first.

## Domain routes

- [admin](../backend/app/modules/admin/router.py)
- [advocates](../backend/app/modules/advocates/router.py)
- [appointments](../backend/app/modules/appointments/router.py)
- [auth](../backend/app/modules/auth/router.py)
- [cases](../backend/app/modules/cases/router.py)
- [communication](../backend/app/modules/communication/router.py)
- [dashboard](../backend/app/modules/dashboard/router.py)
- [deadlines](../backend/app/modules/deadlines/router.py)
- [documents](../backend/app/modules/documents/router.py)
- [legal_assistant](../backend/app/modules/legal_assistant/router.py)
- [legal_knowledge](../backend/app/modules/legal_knowledge/router.py)
- [matching](../backend/app/modules/matching/router.py)
- [reviews](../backend/app/modules/reviews/router.py)
- [triage](../backend/app/modules/triage/router.py)
- [users](../backend/app/modules/users/router.py)
