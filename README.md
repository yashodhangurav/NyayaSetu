# NyayaSetu (न्यायसेतु)

**Legal Help Should Be Clear. Justice Should Be Accessible.**

NyayaSetu is an India-focused legal technology platform bridging citizens and verified advocates, established in 2026. The platform combines an editorial-grade client application with a resilient Python FastAPI modular monolith, providing deterministic legal triage, geospatial advocate matching under Bar Council of India (BCI) Rule 36, secure evidence vaults, statutory limitation tracking, and grounded retrieval-augmented generation (RAG) over verified Indian Bare Acts.

> [!IMPORTANT]
> **Mandatory Statutory Disclosure:** NyayaSetu provides an AI-assisted preliminary legal assessment and advocate-discovery platform. It is **not** a law firm and does not provide legal advice under the Advocates Act, 1961. Submitting an intake request does **not** create an advocate-client relationship. Advocates listed on the platform do not solicit work or advertise fee schedules, in compliance with Rule 36, Chapter II, Part VI of the Bar Council of India Rules.


## Run locally

Start the Python 3.12 FastAPI service from `backend/` and the Next.js client from `frontend/`. PostgreSQL 16 with PostGIS and pgvector backs the API. The browser sends API requests through the Next.js server on port 3000 to FastAPI on port 8000.

From the repository root, run `python backend/scripts/bootstrap_env.py` to prepare the Python environment. Follow the [platform setup guide](docs/CROSS_PLATFORM_SETUP.md) to configure PostgreSQL, apply migrations and start both services.

## Find your way around

| Location | Contents |
| --- | --- |
| [frontend/src](frontend/src/) | App Router pages, shared components and API clients |
| [backend/app](backend/app/) | API entry point, configuration and domain modules |
| [backend/rag](backend/rag/) | Bundled legal corpus, search and evaluation |
| [backend/tests](backend/tests/) | Automated backend regression tests |
| [Documentation](docs/README.md) | Contracts, architecture, setup and operations |
| [Contributor guide](AGENTS.md) | Repository rules and verification commands |
