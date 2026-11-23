# Development and operations

Follow the [setup guide](CROSS_PLATFORM_SETUP.md) for Windows, macOS or Linux. The backend and frontend have independent dependencies. The root virtual environment is local to the operating system.

## Verify a change

| Working directory | Command | What it checks |
| --- | --- | --- |
| `backend/` with the root virtual environment active | `python -m pytest -v` | API, domain, storage and isolation tests using the test fixtures |
| `backend/` | `python scripts/verify_health.py` | FastAPI health endpoint on port 8000. Inspect the nested database status separately |
| `frontend/` | `npm run lint` | ESLint |
| `frontend/` | `npm run build:webpack` | Production compilation, type checking and prerendering |
| `frontend/` | `node scripts/test-services.mjs` | Checks the current process environment for two prohibited public secret names |

For a narrow change, target the relevant pytest file. For example, `python -m pytest tests/test_legal_ai_assistant.py` exercises legal search and answer generation. Database migrations and PostgreSQL extensions require a PostgreSQL instance. SQLite tests cannot validate those extensions.

## Operational entry points

- [Database changes](DATABASE.md) covers the model registry and forward migrations.
- [Vault operations](SECURITY_STORAGE_AND_COMPLIANCE.md) covers private storage, cloud migration and rollback.
- [Legal knowledge](AI_AND_RAG.md) covers corpus ingestion and evaluation.
- [Frontend integration](FRONTEND.md) covers API rewrites and the dev server lifecycle.
