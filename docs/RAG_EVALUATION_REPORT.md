# RAG Evaluation Report

## Baseline (before upgrade)

- Environment: repository working tree on 2026-11-25, Python virtual environment at `venv/`, backend `pytest.ini`.
- Command: `& ..\venv\Scripts\python.exe -m pytest -q` from `backend/`.
- Result: **154 passed in 64.72s**.
- Bundled corpus: `backend/rag/data/processed/canonical_corpus.json`, 71 chunks (pre-upgrade audit).
- Local SQLite database at audit time: 0 legal sources, 0 legal chunks, 0 ingestion jobs.
- Generation provider under tests: deterministic mock (`AI_PROVIDER=mock`).

This baseline is a regression gate, not a legal-quality score.

## Evaluation set status

- `backend/rag/eval/testset.jsonl` contains **156 generated items**. It is **not human-verified legal ground truth**.
- A 300-question human-verified corpus is a manual legal-review dependency; it was not fabricated.
- The harness therefore reports regression signals only. Its quality gate is explicitly `passed: false`.

## Executed upgrade evaluation

Command:

```powershell
cd backend
& ..\venv\Scripts\python.exe -m rag.eval.run_upgrade_eval
```

Generated report: `backend/rag/eval/latest_upgrade_report.json` (2026-11-25T16:19:58Z, regenerated after the bundled corpus expanded from 71 to 128 chunks).

| Field | Executed value |
|---|---|
| Evidence items | 156 (145 in scope, 11 out of scope), `human_verified: false` |
| Corpus | `rag/data/processed/canonical_corpus.json` |
| Corpus SHA-256 | `65ef953df13787289b7657501b4340d70a0f330b799de19667744c2bc51d7216` |
| Embedding provider | `DeterministicMockEmbeddingProvider`, dimension 768 |
| Generation provider | `DeterministicGroundedLLMProvider` |
| Retrieval configuration | `top_k=5`, `RAG_EVIDENCE_MIN_SCORE=0.45`, `RAG_EVIDENCE_MIN_CHUNKS=1` |
| Feature flags | `source_fetch=false`, `neural_embedding=false`, `official_fallback=false`, environment `development` |

### Retrieval regression metrics

| Metric | Value |
|---|---|
| Recall@1 | 0.7586 |
| Recall@3 | 0.8759 |
| Recall@5 | 0.8966 |
| MRR@5 | 0.8175 |
| Out-of-scope correct | 11 / 11 |
| Repealed-law leakage in results | 0 |

Per-language recall@5 / MRR@5: English 0.9306 / 0.8368, Hindi 0.8148 / 0.7019, Kannada 0.8667 / 0.8111, mixed 0.9375 / 0.9375.

### Grounding regression metrics

| Metric | Value |
|---|---|
| Verified citations retained | 536 |
| Unverified citations pruned | 0 |
| Supported claims (lexical diagnostic) | 1411 |
| Unsupported claims (lexical diagnostic) | 0 |
| Claim-support ratio | 1.0 |
| Answers with sources | 139 / 145 in-scope items |

These numbers measure consistency against the bundled corpus and deterministic provider. They do **not** establish legal correctness, current-law validity, or production latency.

## Quality gate

`passed: false` — no human-verified legal ground truth is available. Latency, concordance-mapping precision, and production-provider quality were not benchmarked in this upgrade and must not be claimed as verified.

## Operational observability

- `GET /api/v1/legal/admin/observability` (ADMIN only) exposes in-process event counts and bounded recent events.
- Events contain request IDs, query fingerprints, language, retrieval source, chunk/citation counts, claim-support counts, and provider name. No query text, answer text, user identity, or document content is included.
- Optional `RAG_OBSERVABILITY_LOG_PATH` appends the same content-free events to a local JSONL file.
- Observability counters are operational signals, not an evaluation benchmark.

## Final verification

`& ..\venv\Scripts\python.exe -m pytest -q` from `backend/` → **183 passed in 79.94s**. The changed RAG test modules also pass together: **38 passed in 10.46s** (final focused run including the explicit-section and format-detection regressions).

Live health probe: `& ..\venv\Scripts\python.exe scripts\verify_health.py` → `200 OK`, `status: healthy`, SQLite connected.
