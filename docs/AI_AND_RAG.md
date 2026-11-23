# NyayaSetu AI & RAG Reference

Groq answers open with a plain-language summary. Each legal explanation links to its retrieved passage by checksum. The response also includes ordered actions, relevant records to gather, and missing facts that could affect the answer.

Short greetings receive a localized reply without invoking retrieval or Groq. Legal questions use the same endpoint and return source-backed answers when matching material is available. The dashboard chat posts to `/api/v1/legal/ask` through the Next.js API rewrite. Set `AI_PROVIDER=groq`, `GROQ_API_KEY`, and `GROQ_LLM_MODEL` in the backend environment for live generation. The service searches the database first and uses the bundled JSON corpus when there is no database match or local PostgreSQL is unavailable in development. Queries served during a local database outage cannot be audited to PostgreSQL. The bundled search combines BM25 with deterministic hashed vectors. Groq receives retrieved statutory text and cites numbered sources. If generation fails, the answer indicates low confidence and uses retrieved excerpts.

## Ingestion and evaluation

- The [legal knowledge module](../backend/app/modules/legal_knowledge/) owns database sources and chunks. From `backend/`, run `python scripts/ingest_legal_document.py --help` for supported file inputs, source metadata and re-embedding options. Seeding and re-embedding write to the configured database.
- The [bundled corpus](../backend/rag/data/processed/canonical_corpus.json) provides searchable passages when the database has no matching records. Its [data dictionary](RAG_DATA_DICTIONARY.md) and [source registry](source_registry.csv) describe the records.
- Run `python -m rag.eval.metrics` from `backend/` to evaluate bundled search against its [benchmark queries](../backend/rag/eval/testset.jsonl). The [answer evaluation runner](../backend/scripts/run_ai_eval.py) separately exercises retrieval and generation with an isolated database. Select the intended AI provider before running it.
- The [service](../backend/app/modules/legal_assistant/service.py) handles orchestration, language detection and auditing. The [provider](../backend/app/modules/legal_assistant/llm_provider.py) formats grounded responses. Review citation excerpts and unsupported queries when changing either component.
