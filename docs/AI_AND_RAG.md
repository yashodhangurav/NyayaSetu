# AI & RAG Engineering Reference

This document provides the consolidated engineering, ingestion, retrieval, and evaluation reference for NyayaSetu's legal intelligence subsystem. For the high-level product scope and full source catalog, see [`../RAG.md`](../RAG.md).

---

## 1. System Architecture & Components

NyayaSetu's AI Legal Assistant couples an asymmetric dual-path retrieval pipeline with grounded LLM response generation:

| Component | Implementation File | Key Role & Behaviors |
|---|---|---|
| **Query Rewriter** | `backend/rag/search/query_rewriter.py` | Detects language (EN/KN/HI), classifies 37 legal domains, expands 500+ trilingual synonyms, performs concordance mapping, filters out-of-scope queries. |
| **Concordance Engine** | `backend/rag/ingest/concordance_table.py` | Maps colonial criminal/civil statutes (IPC, CrPC, IEA) to 2023 Sanhitas (BNS, BNSS, BSA). |
| **Lexical Index** | `backend/rag/index/bm25_index.py` | BM25 retrieval over Bare Act sections, numbers, and gazette identifiers. |
| **Semantic Store** | `backend/rag/index/embeddings.py` / pgvector | Multilingual dense embeddings (`BAAI/bge-m3` or deterministic hashed vectors). |
| **Hybrid Search** | `backend/rag/search/hybrid_search.py` | Reciprocal Rank Fusion ($k=60$) over lexical and vector hits; cross-encoder reranking; confidence gating ($\ge 0.45$). |
| **Unified Retriever** | `backend/app/modules/legal_assistant/unified_retriever.py` | Single DB-first facade with bundled fallback, temporal validity, authority-aware ranking, RRF, and evidence sufficiency. |
| **Source Acquisition** | `backend/app/modules/legal_knowledge/{source_registry,fetcher,discovery,sync_service}.py` | Opt-in, robots-aware official-source fetching, SSRF/content limits, bounded discovery, immutable versions, and review queue. |
| **LLM Provider** | `backend/app/modules/legal_assistant/llm_provider.py` | Groq (`qwen/qwen3.8-27b`) or Gemini (`gemini-2.5-flash`), formatting structured JSON with decision badge, answer, 48-hour steps, and court deadlines. |
| **Citation Validator** | `backend/app/modules/legal_assistant/citation_validator.py` | Checksum grounding, unverified section pruning, lexical claim-support diagnostics, and sanitization. |
| **Embedding Provider** | `backend/app/modules/legal_assistant/embedding_provider.py` | Gemini/mock providers plus opt-in `sentence-transformers` neural provider with dimension validation; no silent mock fallback in production. |
| **Observability** | `backend/app/modules/legal_assistant/observability.py` | Admin-only, content-free counters and optional local JSONL event sink. |
| **Service Layer** | `backend/app/modules/legal_assistant/service.py` | End-to-end orchestration, audit logging, confidence downgrade, controlled abstention, and offline fallback. |

### Generation budget and failure handling

Groq generation is deliberately bounded for low-tier output-token quotas: `GROQ_MAX_COMPLETION_TOKENS` defaults to 800, context is capped by `GROQ_MAX_CONTEXT_CHUNKS`, `GROQ_MAX_CONTEXT_CHARS`, and `GROQ_MAX_CHUNK_CHARS`, and a rolling local counter tracks `GROQ_OUTPUT_TOKEN_BUDGET_PER_MINUTE` across requests. Retry behavior is configured by `GROQ_MAX_RETRIES`, `GROQ_RETRY_BACKOFF_SECONDS`, `GROQ_RETRY_JITTER_SECONDS`, and `GROQ_REQUEST_TIMEOUT_SECONDS`. HTTP 429 responses honour `Retry-After` (numeric seconds or HTTP date); otherwise the configured backoff with jitter is used. If the required wait exceeds the configured timeout, the service returns immediately.

No provider failure is silently replaced with deterministic legal prose. `rate_limited`, `timeout`, `provider_unavailable`, and `generation_error` are returned as structured generation statuses with a safe user-facing message. Gemini uses the same status vocabulary through the provider abstraction; its output budget and retry settings are `GEMINI_MAX_COMPLETION_TOKENS`, `GEMINI_MAX_RETRIES`, `GEMINI_RETRY_BACKOFF_SECONDS`, and `GEMINI_REQUEST_TIMEOUT_SECONDS`. Only whitelisted, non-identifying case facts are summarized into generation context; raw chat history and direct identifiers are not sent to external providers. The provider is selected by `AI_PROVIDER`; the service never auto-upgrades to a paid model or assumes a higher account tier.

---

## 2. Bundled Canonical Corpus Data Dictionary

When PostgreSQL is unavailable, `LegalHybridSearchEngine` queries the canonical corpus (`backend/rag/data/processed/canonical_corpus.json`):

| Field | Type | Description |
|---|---|---|
| `chunk_id` | `str` | Unique chunk identifier (e.g., `chk_tpa_section_54_8a9f`). |
| `source_id` | `str` | Reference to official source in [`source_registry.csv`](source_registry.csv). |
| `doc_type` | `str` | Category: `STATUTE`, `PROCEDURE`, `JUDGMENT`, `GLOSSARY`. |
| `act` | `str` | Official Bare Act or precedent title. |
| `short_code` | `str` | Canonical statute abbreviation (`BNS`, `BNSS`, `BSA`, `TPA`, `KLRA`). |
| `section` | `str` | Section number, Article, or procedural step heading. |
| `clause_heading` | `str` | Subordinate heading or statutory title. |
| `jurisdiction` | `str` | `India (Central)` or `Karnataka (State)`. |
| `language` | `str` | Primary language code (`en`, `kn`, `hi`). |
| `in_force` | `bool` | Current statutory validity (`false` for repealed IPC/CrPC provisions). |
| `effective_date` | `str` | Date when the provision came into force (e.g., `2024-07-01` for Sanhitas). |
| `topic_tags` | `List[str]` | Semantic keywords used for hybrid retrieval. |
| `chunk_text` | `str` | Structure-preserved statutory or judicial excerpt. |
| `token_count` | `int` | Estimated token length (~1.3 tokens per word). |
| `content_checksum` | `str` | SHA-256 fingerprint for strict citation verification. |
| `source_url` | `str` | Authentic government or court portal link. |

---

## 3. Chunking & Ingestion Methodology

Statutes are chunked by section rather than arbitrary character lengths:
- **Statutes**: Chunked at the section / article level. Subsections, provisos, and explanations remain unified.
- **Heading Prepending**: Every chunk begins with `{act} · {section} ({clause_heading})\n\n` to anchor semantic context.
- **Token Bounds**: 800-token threshold before hierarchical division.
- **Judgments**: Formatted with Issue, Holding, and Ratio Decidendi to exclude extraneous judicial procedure.
- **Guides**: Step-by-step procedural guides for portals like Bhoomi, Kaveri 2.0, and e-Daakhil.

**To rebuild the canonical offline corpus:**
```powershell
cd backend
python -m rag.ingest.corpus_builder
```

**To seed PostgreSQL + pgvector:**
```powershell
cd backend
python scripts/seed_legal_sources.py
```

---

## 4. Evaluation Results (executed regression harness)

The only executed evaluation in this upgrade is `backend/rag/eval/run_upgrade_eval.py` against 156 **generated, non-human-verified** items using the deterministic provider and the bundled corpus. See [`RAG_EVALUATION_REPORT.md`](RAG_EVALUATION_REPORT.md) and `backend/rag/eval/latest_upgrade_report.json`.

| Metric | Executed value | Interpretation |
|---|---|---|
| **Recall@5** | 0.8966 | Regression signal on generated items, not legal ground truth |
| **MRR@5** | 0.8175 | Regression signal on generated items |
| **Out-of-scope correct** | 11 / 11 | Deterministic gate behavior |
| **Repealed-law leakage in results** | 0 | Bundled corpus filter |
| **Claim-support ratio** | 1.0 | Lexical diagnostic, not legal reasoning |
| **Quality gate** | `passed: false` | No human-verified ground truth |

Concordance-mapping precision, production latency, live-provider answer quality, and live official-source verification were **not** benchmarked in this upgrade and are not claimed as verified.

---

## 5. Source Maintenance & Update Policy

1. **Official Sources Only**: Central Acts must originate from [India Code](https://www.indiacode.nic.in); Karnataka Acts from [Karnataka DPAL](https://dpal.karnataka.gov.in); Supreme Court judgments from [DigiSCR](https://digiscr.sci.gov.in).
2. **Repeal Governance**: Chunks from repealed laws (IPC 1860, CrPC 1973, IEA 1872) are marked `in_force: false` and mapped via `concordance_table.py`.
3. **Review Cadence**:
   - Central Sanhitas & Amendments: Monthly gazette checks.
   - Karnataka State Acts & Rules: Bi-monthly review.
   - Citizen Helplines (15100, 1930): Quarterly dial checks.
