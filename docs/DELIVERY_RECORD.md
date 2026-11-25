# Delivery record

The historical November 2026 reports cover the FastAPI migration, dashboard integration, advocate verification and matching, case intake, vault storage, communication and legal retrieval. The original audit narratives, dated results and implementation matrices are available from the repository root with:

```bash
git show 690d5bdc:docs/DELIVERY_RECORD.md
```

Those reports describe the checkout examined at the time. Run `python -m pytest --collect-only -q` from `backend/` to list the tests in your checkout.

For operating instructions use the [documentation index](README.md). The [architecture decision](adr/0001-backend-stack.md) preserves the earlier backend selection.

## 2026-11-25 — grounded RAG upgrade increment

- Added the active official-source registry, secure fetch/discovery/sync pipeline, immutable document versions, sync checkpoints, and legal review queue in `backend/app/modules/legal_knowledge/` and migration `0016_legal_source_registry_and_versions`.
- Added unified retrieval (DB-first with bundled fallback, temporal validity, authority ranking, RRF, sufficiency), claim-level support diagnostics with controlled abstention, opt-in neural embeddings, and content-free observability in `backend/app/modules/legal_assistant/`.
- Added `backend/scripts/rag_ops.py` and `backend/rag/eval/run_upgrade_eval.py`; executed the offline regression harness and recorded results in `backend/rag/eval/latest_upgrade_report.json` and [`RAG_EVALUATION_REPORT.md`](RAG_EVALUATION_REPORT.md).
- Final verification: `& ..\venv\Scripts\python.exe -m pytest -q` from `backend/` → **183 passed in 79.94s** (baseline 154 passed). Live health probe returned `200 OK` with SQLite connected.
- Completion pass: one source (`SRC_PROC_KAVERI_001`) was fetch-verified and synced to `PENDING_REVIEW` through the runtime CLI; format detection was corrected so an HTML response is not parsed as a declared PDF; explicit section references now outrank query-expansion noise.
- Limitations: only 1 of 161 sources is fetch-verified, no human-verified legal ground truth, no live PostgreSQL migration execution, no heavyweight embedding model installation, and no production latency/concordance benchmark. Full detail is in [`RAG_UPGRADE_PROGRESS.md`](RAG_UPGRADE_PROGRESS.md).
