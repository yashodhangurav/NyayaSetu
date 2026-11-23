# System architecture

NyayaSetu runs a Next.js App Router client and one Python FastAPI service. Client-side requests use relative paths under `/api/v1`. The Next.js rewrite forwards them to the configured FastAPI origin. Domain state belongs to PostgreSQL. Private document bytes are stored separately from the public web assets.

| Boundary | Responsibility | Starting point |
| --- | --- | --- |
| Web UI | Pages, dashboard interactions, server rendering, public content and offline development data | [App routes](../frontend/src/app/), [dashboard clients](../frontend/src/services/dashboard/) |
| API | Startup validation, CORS, error handling and versioned routes | [ASGI factory](../backend/app/main.py), [router registry](../backend/app/api/v1/router.py) |
| Business logic | Route handlers, typed payloads, services, role and ownership checks | [Domain modules](../backend/app/modules/) |
| Persistence | Async database sessions, models and schema changes | [Database reference](DATABASE.md) |
| Private documents | Storage adapters, upload, authorized download and scanning | [Storage and security](SECURITY_STORAGE_AND_COMPLIANCE.md) |
| Legal assistant | Retrieval, provider selection, source validation and structured answers | [AI and RAG](AI_AND_RAG.md) |

The public content and parts of the dashboard include demonstrations. Trace a feature from its page to the service method and registered route before treating its displayed state as persisted. Keep the existing development fallback until the live path has been verified.

The [superseded backend decision](adr/0001-backend-stack.md) records the earlier stack selection. The active runtime is FastAPI.
