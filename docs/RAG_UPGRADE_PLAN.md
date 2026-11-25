# RAG Upgrade Plan

## Scope and constraints

- Preserve the existing FastAPI API, SQLite development default, PostgreSQL + pgvector production target, provider abstractions, document vault, scanning, and authentication.
- Add capability incrementally; every increment must keep the existing backend test suite green.
- External legal content is untrusted data. Official URLs are provenance, not instructions.
- No source, section, judgment, URL, or amendment is invented. A registry row is a discovery candidate until a real fetch/verification succeeds.
- No user identity, private document, or unnecessary personal data is sent to an external retrieval provider.
- No human legal ground truth is fabricated. Generated evaluation items are regression signals only.

## Dependency map

1. **Schema and source registry** — persistent registry, document versions, sync jobs, review queue.
2. **Secure acquisition** — robots-aware HTTP client, SSRF/redirect/content validation, discovery adapters.
3. **Sync orchestration and admin/CLI operations** — bootstrap, incremental sync, retries/checkpoints, promotion of reviewed documents through the existing ingestion pipeline.
4. **Unified retrieval** — one interface used by assistant and search; query understanding, temporal validity, authority-aware reranking, RRF, sufficiency/abstention.
5. **Embeddings and migration discipline** — configurable open-source neural embeddings, explicit mock fallback, dimension/version checks.
6. **Grounded generation** — claim-level verification, controlled abstention, response structure compatible with the current schema.
7. **Evaluation and observability** — baseline capture, deterministic metrics, content-free event counters, honest reporting.

## Phases

| Phase | Deliverable | Status | Evidence / limitation |
|---|---|---|---|
| 1 | Active source registry and secure fetch/discovery/sync pipeline | Implemented / Tested | `source_registry.py`, `fetcher.py`, `discovery.py`, `sync_service.py`; one source (`SRC_PROC_KAVERI_001`) live fetch-verified and synced to a `PENDING_REVIEW` version. Other candidates remain unverified. |
| 2 | Rich metadata, versioning, structure-aware ingestion expansion | Implemented / Tested | `0016_legal_source_registry_and_versions.py`, immutable `LegalDocumentVersion`, XML/DOCX parser support; promotion remains explicit. PostgreSQL migration was not executed against a live PostgreSQL instance. |
| 3 | Unified hybrid retrieval and evidence sufficiency | Implemented / Tested | `unified_retriever.py`, RRF of semantic and lexical ranks, authority bonus, explicit-section boost, sufficiency gate; `tests/test_unified_retriever.py` passed. |
| 4 | Temporal retrieval and amendment/review queue | Implemented / Tested | Validity-window filtering and `LegalReviewItem` queue; changed checksums and ambiguous commencement states require human legal review. |
| 5 | Generation prompt/repair and claim verification | Implemented / Tested | `CitationValidator.verify_claim_support()`, confidence downgrade and controlled abstention in `service.py`; response schema remains backward compatible. |
| 6 | Controlled official-source fallback via the acquisition pipeline | Implemented / Tested | Opt-in `RAG_OFFICIAL_FALLBACK_ENABLED`; fallback queues reviewed documents only and never injects raw web text into generation. Explicit fallback forces its own sync despite the default fetch flag. No live fallback execution. |
| 7 | Evaluation, tests, monitoring, documentation | Implemented / Tested | `run_upgrade_eval.py` executed and regenerated after corpus expansion; content-free observability endpoint and JSONL sink added; full backend suite `183 passed`. Quality gate remains blocked without human-verified ground truth. |

## Verification history

- Baseline before implementation: `& ..\venv\Scripts\python.exe -m pytest -q` from `backend/` — **154 passed in 64.72s**.
- Focused acquisition/sync tests: **12 passed in 2.68s**.
- Retrieval/generation regression tests: **20 passed in 6.70s**.
- Grounding/observability tests: **14 passed in 4.43s**.
- Full suite after upgrade: `& ..\venv\Scripts\python.exe -m pytest -q` from `backend/` — **183 passed in 79.94s**.
- Live registry bootstrap loaded 161 candidates; one source was fetch-verified and synced to a `PENDING_REVIEW` version without indexing.
- Live health probe: `& ..\venv\Scripts\python.exe scripts\verify_health.py` → `200 OK`, `status: healthy`, SQLite connected.
- Alembic head inspection: `alembic heads` → `0016_legal_source_registry_and_versions (head)`.
