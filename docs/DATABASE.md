# Database and migrations

## Local development (SQLite default)

`backend/.env.example` ships with `DATABASE_URL=sqlite+aiosqlite:///./nyayasetu.db`. The API creates `backend/nyayasetu.db` and all tables from ORM metadata on startup (see `initialize_database` in [database.py](../backend/app/core/database.py)), so no database server or migration step is required for local development. Relative SQLite paths are anchored to the `backend/` directory regardless of where the server is launched.

PostgreSQL is still the production database. To switch back, set `DATABASE_URL`/`DATABASE_URL_SYNC` to `postgresql+psycopg://…` and run `alembic upgrade head`; the SQLite `create_all` path is skipped automatically.

## PostgreSQL 16 (production)

PostgreSQL 16 stores application state. The first migration enables `uuid-ossp`, `postgis` and `vector`. Provision the extensions or use a database role with permission to create them before upgrading. Psycopg 3 connects the async SQLAlchemy engine. Configure connection settings in the backend environment.

## Model ownership

| Module | Tables |
| --- | --- |
| [admin](../backend/app/modules/admin/models.py) | `audit_logs` |
| [advocates](../backend/app/modules/advocates/models.py) | `advocate_profiles`, `advocate_verification_applications`, `advocate_verifications` |
| [appointments](../backend/app/modules/appointments/models.py) | `appointments` |
| [auth](../backend/app/modules/auth/models.py) | `refresh_tokens` |
| [cases](../backend/app/modules/cases/models.py) | `legal_cases`, `case_messages` |
| [communication](../backend/app/modules/communication/models.py) | `conversations`, `messages` |
| [deadlines](../backend/app/modules/deadlines/models.py) | `deadlines` |
| [documents](../backend/app/modules/documents/models.py) | `documents` |
| [legal_knowledge](../backend/app/modules/legal_knowledge/models.py) | `legal_sources`, `legal_chunks`, `legal_ingestion_jobs`, `legal_source_registry`, `legal_document_versions`, `legal_sync_jobs`, `legal_review_items`, `legal_relationships` |
| [reviews](../backend/app/modules/reviews/models.py) | `reviews` |
| [triage](../backend/app/modules/triage/models.py) | `consultation_requests` |
| [users](../backend/app/modules/users/models.py) | `users`, `user_consents` |

## Changing the schema

With the SQLite development default, edited ORM models are applied automatically on the next server start (`create_all`). Alembic migrations remain the mechanism for PostgreSQL only.

From `backend/` with the virtual environment activated and a PostgreSQL `DATABASE_URL`, use `alembic current` and `alembic heads` to inspect revision state. Use `alembic upgrade head` to apply pending migrations to the configured database.

Register new models in [the metadata registry](../backend/app/core/models.py). Generate a new revision with `alembic revision --autogenerate -m "describe the change"`. Review the generated operations, especially geospatial and vector indexes. Committed revisions in [the version history](../backend/migrations/versions/) are immutable. Revision `0016_legal_source_registry_and_versions` is the current head; it adds the active registry, immutable document versions, sync jobs, review items, and relationship tables additively.

The [session dependency](../backend/app/core/database.py) handles normal commit and exception rollback. The [test fixtures](../backend/tests/conftest.py) create an isolated SQLite schema for application tests.
