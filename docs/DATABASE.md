# Database and migrations

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
| [legal_knowledge](../backend/app/modules/legal_knowledge/models.py) | `legal_sources`, `legal_chunks`, `legal_ingestion_jobs` |
| [reviews](../backend/app/modules/reviews/models.py) | `reviews` |
| [triage](../backend/app/modules/triage/models.py) | `consultation_requests` |
| [users](../backend/app/modules/users/models.py) | `users`, `user_consents` |

## Changing the schema

From `backend/` with the virtual environment activated, use `alembic current` and `alembic heads` to inspect revision state. Use `alembic upgrade head` to apply pending migrations to the configured database.

Register new models in [the metadata registry](../backend/app/core/models.py). Generate a new revision with `alembic revision --autogenerate -m "describe the change"`. Review the generated operations, especially geospatial and vector indexes. Committed revisions in [the version history](../backend/migrations/versions/) are immutable.

The [session dependency](../backend/app/core/database.py) handles normal commit and exception rollback. The [test fixtures](../backend/tests/conftest.py) create an isolated SQLite schema for application tests.
