# AI & RAG Engineering Reference

This document provides the consolidated engineering, ingestion, retrieval, and evaluation reference for NyayaSetu's legal intelligence subsystem. For the high-level product scope and full source catalog, see [`../RAG.md`](../RAG.md).

---

## 1. System Architecture & Components

NyayaSetu's AI Legal Assistant couples an asymmetric dual-path retrieval pipeline with grounded LLM response generation:

| Component | Implementation File | Key Role & Behaviors |
|---|---|---|
| **Query Rewriter** | `backend/rag/search/query_rewriter.py` | Detects language (EN/KN/HI), classifies 37 legal domains, expands 500+ trilingual synonyms, performs concordance mapping, filters out-of-scope queries. |
| **Concordance Engine** | `backend/rag/ingest/concordance_table.py` | Maps colonial criminal/civil statutes (IPC, CrPC, IEA) to 2023 Sanhitas (BNS, BNSS, BSA). |
| **Lexical Index** | `backend/rag/search/bm25.py` | BM25 retrieval over Bare Act sections, numbers, and gazette identifiers. |
| **Semantic Store** | `backend/rag/search/vector_store.py` / pgvector | Multilingual dense embeddings (`BAAI/bge-m3` or deterministic hashed vectors). |
| **Hybrid Search** | `backend/rag/search/hybrid_search.py` | Reciprocal Rank Fusion ($k=60$) over lexical and vector hits; cross-encoder reranking; confidence gating ($\ge 0.45$). |
| **LLM Provider** | `backend/app/modules/legal_assistant/llm_provider.py` | Groq (`qwen/qwen3.8-27b`) or Gemini (`gemini-2.5-flash`), formatting structured JSON with decision badge, answer, 48-hour steps, and court deadlines. |
| **Citation Validator** | `backend/app/modules/legal_assistant/citation_validator.py` | Checksum grounding against retrieved source chunks; flags unverified section numbers; sanitizes prose. |
| **Service Layer** | `backend/app/modules/legal_assistant/service.py` | End-to-end orchestration, language translation, audit logging, and automated offline fallback. |

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

## 4. Evaluation Benchmark Results

Evaluated against the standardized legal benchmark test set:

| Evaluation Metric | Target Threshold | Measured Score | Evaluation Status |
|---|---|---|---|
| **Recall@5** | $\ge 85.0\%$ | **88.97%** | PASS (Exceeds Target) |
| **Mean Reciprocal Rank (MRR)** | $\ge 0.70$ | **0.84** | PASS |
| **Concordance Mapping Precision** | $100\%$ | **100.0%** | PASS (Zero Mismatches) |
| **Repealed Law Leakage** | $0.0\%$ | **0.0%** | PASS (Safe Sanhita Transition) |
| **Average Retrieval Latency** | $< 120\text{ ms}$ | **42 ms** | PASS |

---

## 5. Source Maintenance & Update Policy

1. **Official Sources Only**: Central Acts must originate from [India Code](https://www.indiacode.nic.in); Karnataka Acts from [Karnataka DPAL](https://dpal.karnataka.gov.in); Supreme Court judgments from [DigiSCR](https://digiscr.sci.gov.in).
2. **Repeal Governance**: Chunks from repealed laws (IPC 1860, CrPC 1973, IEA 1872) are marked `in_force: false` and mapped via `concordance_table.py`.
3. **Review Cadence**:
   - Central Sanhitas & Amendments: Monthly gazette checks.
   - Karnataka State Acts & Rules: Bi-monthly review.
   - Citizen Helplines (15100, 1930): Quarterly dial checks.
