# FastAPI contract

The registered [versioned router](../backend/app/api/v1/router.py), endpoint decorators and Pydantic schemas define paths, authentication, accepted fields and responses. With `DEBUG=true`, inspect [Swagger UI](http://localhost:8000/docs), [ReDoc](http://localhost:8000/redoc) or the [OpenAPI JSON](http://localhost:8000/api/v1/openapi.json).

## Calling the API

The default prefix is `/api/v1`. The browser uses the [shared API client](../frontend/src/lib/api-client.ts) for bearer tokens, JSON, multipart uploads and typed errors. Domain routes enforce their own roles and resource ownership.

Application errors expose `error.code`, `error.message` and `error.details`. Validation errors return HTTP 422. See the [exception handlers](../backend/app/core/errors.py) for the precise envelope.

## Legal chat

`POST /api/v1/legal/ask` accepts `query` and optional `preferred_language`, `jurisdiction` and `max_sources`. A greeting returns `kind="greeting"`. A legal answer includes a summary and explanations in `answer`, citation records, ordered next steps, optional deadline information and confidence metadata. Each item in `legal_points` carries a `source_checksum` identifying its citation. `documents_to_gather` and `facts_to_confirm` are lists. Read the [request and response schemas](../backend/app/modules/legal_assistant/schemas.py) for constraints and defaults.

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
