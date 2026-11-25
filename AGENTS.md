# AGENTS.md — NyayaSetu Repository Guide

This file is the single source of truth and entry point for any developer or AI coding agent working in this repository.
Read it completely before inspecting or modifying code.

---

## 1. Project Overview & Architecture

NyayaSetu (न्यायसेतु) is an India-focused legal technology platform designed to bridge citizens and verified advocates, established in 2026. The platform comprises two independent applications:

* **`frontend/`** — Next.js 16 (App Router), React 19, TypeScript, and Tailwind CSS 4 client application featuring an editorial design language, public legal information directories, citizen matter intake, case tracking dockets, evidence vault, and advocate discovery.
* **`backend/`** — Python 3.12 + FastAPI 0.115 Modular Monolith API with SQLAlchemy 2.0 (Asyncio) over PostgreSQL 16 (powered by PostGIS geospatial indexing and pgvector semantic embeddings). It manages authentication, advocate credentials, case dossiers, deterministic triage, limitation deadlines, secure document vault, and grounded statutory RAG assistance.

> [!CRITICAL]
> **Single Backend Rule:** The Python FastAPI backend in `backend/` is the sole authoritative server application. Do **not** introduce a second backend framework (e.g., Express, Fastify, NestJS) or duplicate database ORM layer (e.g., Prisma, Drizzle). All server features, migrations, and database entities must remain in `backend/`.

---

## 2. Repository Map

```text
NyayaSetu/
├── frontend/                   Next.js 16 client application
│   ├── src/app/                App Router routes & layouts
│   ├── src/components/         Editorial UI primitives, layout, 3D Canvas
│   ├── src/services/dashboard/ API integration clients & typed service layer
│   ├── src/lib/                AuthContext, unified API client, design tokens
│   ├── src/types/              TypeScript domain definitions
│   └── scripts/predev.js       Port 3000 lifecycle hygiene
├── backend/                    Python 3.12 FastAPI Modular Monolith API
│   ├── app/
│   │   ├── main.py             ASGI factory, CORS, exception handlers
│   │   ├── core/               Config, SQLAlchemy async engine, Argon2/JWT security
│   │   ├── api/v1/             Central API router & health diagnostics
│   │   ├── modules/            Domain packages (routes, services, models)
│   │   ├── integrations/       AI providers, SMS gateways, external adapters
│   │   └── shared/             Shared pagination models & response schemas
│   ├── migrations/             Alembic migration revisions (`versions/`) & env.py
│   ├── scripts/                Operational scripts (`run_dev.sh`, `verify_health.py`)
│   ├── tests/                  Pytest async integration test suites
│   ├── rag/                    Bundled legal corpus, search, ingestion and evaluation
│   ├── requirements.txt        Pinned Python dependencies
│   ├── alembic.ini             Alembic configuration
│   └── run.py                  Uvicorn development server launcher
├── docs/                       Architecture, API contract, database schema, roadmaps
└── .gitignore                  Git tracking rules
```

There is **no root package manager workspace**. Run frontend commands from `frontend/` and backend commands from `backend/`.

---

## 3. Technology Stack & Verification Commands

### 3.1 Backend (`backend/`)

* **Runtime:** Python 3.12
* **Framework:** FastAPI 0.115 + Pydantic v2
* **ORM:** SQLAlchemy 2.0 (Asyncio)
* **Driver:** Psycopg 3 (`psycopg[binary]>=3.2.0`) for PostgreSQL; `aiosqlite` for the SQLite development default
* **Database:** PostgreSQL 16 with PostGIS (`geoalchemy2`) and pgvector (`pgvector.sqlalchemy`) in production; local development defaults to SQLite (`sqlite+aiosqlite:///./nyayasetu.db`, schema auto-created on startup)
* **Migrations:** Alembic (PostgreSQL only)
* **Password Hashing:** Argon2id (`argon2-cffi`)
* **Tokens:** PyJWT (HS256) with database-tracked refresh rotation
* **Testing:** Pytest 8.2 + pytest-asyncio + HTTPX (uses SQLite `:memory:` via `aiosqlite`)

#### Backend Commands

The root `venv/` is generated per operating system and git-ignored; never
commit it. See [`docs/CROSS_PLATFORM_SETUP.md`](docs/CROSS_PLATFORM_SETUP.md)
for the one-command bootstrap (`python backend/scripts/bootstrap_env.py`) and
full Windows commands.

```bash
cd backend

# Setup Python 3.12 Virtual Environment — macOS / Linux
python3.12 -m venv ../venv
source ../venv/bin/activate

# Setup Python 3.12 Virtual Environment — Windows PowerShell
# py -3.12 -m venv ..\venv
# ..\venv\Scripts\Activate.ps1

# Install dependencies (either OS)
python -m pip install -r requirements.txt

# Environment configuration
cp .env.example .env
# Windows PowerShell: Copy-Item .env.example .env

# Database Migrations (PostgreSQL)
alembic upgrade head

# Generate new migration after editing SQLAlchemy models
alembic revision --autogenerate -m "describe_change"

# Launch Development Server (Port 8000)
python run.py
# Or directly via Uvicorn:
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Operational Verification & Diagnostics
python scripts/verify_health.py

# Run Integration Test Suite
pytest -v
```

* **Interactive OpenAPI Swagger Docs:** <http://localhost:8000/docs>
* **Alternative ReDoc UI:** <http://localhost:8000/redoc>
* **System Health Probe:** <http://localhost:8000/api/v1/health>

---

### 3.2 Frontend (`frontend/`)

* **Framework:** Next.js 16.4.5 (App Router)
* **UI Runtime:** React 19.3.0
* **Language:** TypeScript 5
* **Styling:** Tailwind CSS 4 + custom warm editorial CSS tokens in `src/app/globals.css`
* **Motion & 3D:** Framer Motion 14, Three.js, `@react-three/fiber`, `@react-three/drei`
* **Icons:** `lucide-react`
* **API Proxy:** Next.js rewrites in `next.config.ts` route `/api/v1/:path*` to `http://localhost:8000`

#### Frontend Commands

```bash
cd frontend

# Install Node dependencies
npm install

# Start Development Server (Port 3000)
npm run dev

# Code Quality & Type Checks
npm run lint

# Production Webpack Build
npm run build:webpack
# Or standard build:
npm run build

# Start Production Server
npm run start
```

---

## 4. Non-Negotiable Architecture & Coding Conventions

### 4.1 Backend Code Conventions

1. **Modular Monolith Boundaries:**
   * Business domains reside in `backend/app/modules/<module_name>/`.
   * Each module encapsulates its own:
     * `router.py` (FastAPI route declarations)
     * `schemas.py` (Pydantic v2 request/response models)
     * `models.py` (SQLAlchemy 2 mapped entities)
     * `service.py` (business logic, queries, and transactions)
     * `dependencies.py` (role guards, query parameters)
   * Cross-module interaction must occur through exported service methods, never via raw cross-table SQL joins across domain boundaries.
2. **Thin Route Handlers:**
   * Route handlers must only validate request payloads, inject dependencies (`db: AsyncSession = Depends(get_db)`, `current_user = Depends(get_current_active_user)`), and delegate to the domain `Service`.
3. **Database Access & Transactions:**
   * Always inject `AsyncSession` via `Depends(get_db)`.
   * `get_db()` automatically commits transactions upon normal completion and triggers an automatic rollback if an unhandled exception or `SQLAlchemyError` occurs.
4. **Standardized Error Handling:**
   * Throw typed exceptions from `backend/app/core/errors.py`:
     * `NotFoundException` (HTTP 404)
     * `BadRequestException` (HTTP 400)
     * `ConflictException` (HTTP 409)
     * `UnauthorizedException` (HTTP 401)
     * `ForbiddenException` (HTTP 403)
   * Never hand-roll inconsistent JSON error bodies. Centralized handlers in `app/main.py` format all exceptions into:
     `{"error": {"code": "...", "message": "...", "details": {...}}, "request_id": "..."}`.
5. **Alembic Migrations:**
   * All entity models must inherit from `app.core.database.Base` and be imported into `app.core.models` so Alembic can discover metadata.
   * Never modify existing, committed migration scripts in `backend/migrations/versions/`. Always create a new forward migration with `alembic revision --autogenerate -m "..."`.

---

### 4.2 Authentication & Security Conventions

1. **Password Security:**
   * Plaintext passwords must be hashed using Argon2id (`app.core.security.hash_password`) before storage. Plain passwords are never logged or stored.
2. **JWT Sessions:**
   * Access tokens expire in 60 minutes (`ACCESS_TOKEN_EXPIRE_MINUTES`).
   * Refresh tokens expire in 7 days and must be tracked in the `refresh_tokens` database table with their SHA-256 fingerprint (`hash_token`). Tokens are rotated upon each refresh; reuse invalidates all related sessions.
3. **Role-Based Access Control (RBAC):**
   * Three distinct system roles exist: `CITIZEN`, `ADVOCATE`, `ADMIN`.
   * Protect sensitive routes using FastAPI dependencies:
     * `require_roles("CITIZEN")`
     * `require_roles("ADVOCATE")`
     * `require_roles("ADMIN")`
   * Self-assignment of the `ADMIN` role is strictly rejected at the route and service level.
4. **Document Vault Security:**
   * Private client evidence files must be stored outside public frontend directories.
   * File downloads must be authenticated via Bearer JWT or short-lived, signed download tokens (15-minute expiry). Public static URLs for vault files are strictly prohibited.

---

### 4.3 Frontend Code Conventions

1. **Next.js 16 & React 19 Compliance:**
   * Follow Next.js 16 App Router patterns. Keep data fetches on the server where appropriate.
   * In React 19, avoid `setState` calls directly inside top-level `useEffect` hooks for prop synchronization; prefer render-phase state adjustment.
2. **Visual Design Integrity (The Homepage Reference):**
   * The visual standard is defined by the homepage (`frontend/src/app/page.tsx`):
     * Backgrounds: Warm ivory (`#f4efe6`) and card paper (`#fffaf2`).
     * Typography: Gambetta editorial serif (`font-serif`) for headings; clean sans-serif for body text; monospace for dockets.
     * Accents: Antique bronze (`#9a6a35`) and warm gold (`#d1a46a`).
     * Geometry: Classical rectangular borders (`rounded-[2px]`).
     * **Prohibited:** Never introduce modern SaaS neon hues (`bg-blue-600`, `bg-purple-600`) or pill-shaped buttons (`rounded-full`, `rounded-2xl`).
3. **API Integration Standards:**
   * Use the centralized client `api` in `frontend/src/lib/api-client.ts`.
   * Automatically injects Bearer JWT from `localStorage` and unwraps FastAPI standardized errors into typed `ApiError` instances.
   * Preserve offline fallback data while developing until endpoints are fully verified.

---

### 4.4 Indian Legal Compliance Standards

1. **Bar Council of India (BCI) Rule 36:**
   * Advocates are prohibited from soliciting clients or advertising fee structures.
   * Maintain the prominent non-advertising notice on all public pages.
   * Advocate directory matching must remain transparent, objective, and merit-based (scoring by practice fit, court proximity, language, and verified bar roll). Never introduce paid priority placements.
2. **Statutory Legal Disclaimer:**
   * Never weaken or remove the mandatory disclosure:
     *"NyayaSetu provides an AI-assisted preliminary legal assessment and advocate-discovery platform. It is not a law firm and does not provide legal advice. Submitting an intake does not create an advocate-client relationship."*
3. **Limitation Act, 1963 Disclaimers:**
   * Statutory limitation calculations must indicate their statutory basis (e.g., Section 138 NI Act 30-day notice, Consumer Protection Act 2-year filing) and state that they require review by an empanelled advocate.
4. **Digital Personal Data Protection Act, 2023 (DPDP):**
   * Maintain transparent purpose limitation, consent logging, and data privacy disclosures across citizen intake and document sharing.

---

## 5. Verification Gates Before Reporting Complete

For a focused backend edit, run the pytest file or cases covering the changed behavior from `backend/`. For example, chat greeting and Groq response mapping are covered by `python -m pytest -q tests/test_legal_ai_assistant.py -k "greeting or groq"`. Run the whole file for changes to other chat behavior. Use the full backend checks below before merging or when changing shared fixtures, authentication dependencies, or database infrastructure. Probe the live server when verifying runtime configuration or connectivity.

### Backend Checks
```bash
cd backend
source ../venv/bin/activate      # macOS / Linux
pytest -v
python scripts/verify_health.py
```

```powershell
cd backend
..\venv\Scripts\Activate.ps1     # Windows PowerShell
pytest -v
python scripts\verify_health.py
```

### Frontend Checks
```bash
cd frontend
npm run lint
npm run build:webpack
```

### Documentation Checks
* Verify that command snippets and paths correspond to active files on disk.
* Verify links use the `file://` scheme or accurate relative markdown references.

---

## 6. Documentation Directory Index

When changing behavior, update the matching specification:
* **API Endpoints & Contracts:** [`docs/API.md`](docs/API.md)
* **Database Models & Alembic Schema:** [`docs/DATABASE.md`](docs/DATABASE.md)
* **System Architecture:** [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
* **Frontend Specifications:** [`docs/FRONTEND.md`](docs/FRONTEND.md)
* **Development, Setup & Operations:** [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md)
* **Cross-Platform Commands:** [`docs/CROSS_PLATFORM_SETUP.md`](docs/CROSS_PLATFORM_SETUP.md)
* **Legal RAG & AI Chatbot Specification:** [`RAG.md`](RAG.md)
* **AI/RAG Engineering:** [`docs/AI_AND_RAG.md`](docs/AI_AND_RAG.md)
* **Security, Storage & Compliance:** [`docs/SECURITY_STORAGE_AND_COMPLIANCE.md`](docs/SECURITY_STORAGE_AND_COMPLIANCE.md)
* **Delivery History/Audits:** [`docs/DELIVERY_RECORD.md`](docs/DELIVERY_RECORD.md)
* **Roadmap:** [`docs/ROADMAP.md`](docs/ROADMAP.md)
