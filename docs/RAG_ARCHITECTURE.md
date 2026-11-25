# RAG Architecture

## Implemented before this upgrade (verified 2026-11-25)

- **Primary assistant path:** `LegalAssistantService.ask()` → `LegalRetrievalEngine.retrieve()` over `legal_sources` / `legal_chunks` (pgvector in PostgreSQL, Python cosine fallback in SQLite) → offline `LegalHybridSearchEngine` fallback over `backend/rag/data/processed/canonical_corpus.json` → Groq/Gemini/deterministic LLM → citation validation → audit log.
- **Ingestion:** manual admin/CLI calls to `LegalDocumentIngestionPipeline.ingest_document()`.
- **Source registry:** static trusted-domain allowlist in `ingestion_pipeline.py` plus a CSV of declared document URLs. No scheduler, no official-site fetching, no automated amendment tracking.
- **Online retrieval:** none. The only query-time outbound call was to the configured LLM provider.

## Current architecture

```text
Registry CSV / admin entries
  -> LegalSourceRegistry (candidate, disabled and PENDING by default)
  -> SecureFetcher (HTTPS only, official domains, robots.txt, DNS/SSRF,
     bounded redirects/bytes/types, retries, rate limit, ETag/If-Modified-Since)
  -> Discovery adapters (declared static document, robots-advertised sitemap,
     explicitly configured RSS/Atom feed, configured official listing page)
  -> Raw object storage + SHA-256 of fetched bytes + LegalDocumentVersion
  -> Review queue (new document, changed checksum, ambiguous legal status)
  -> Explicit admin/CLI promotion -> existing DocumentParser / LegalChunker /
     embedding provider -> legal_sources / legal_chunks

Question
  -> UnifiedLegalRetriever
       - query rewriting / language / legacy concordance / domain tags
       - verified database and pgvector first
       - immutable bundled corpus fallback
       - temporal validity filtering and authority-aware ranking
       - reciprocal rank fusion of semantic and lexical rankings
       - evidence sufficiency gate
  -> grounded LLM -> citation validation -> lexical claim support check
  -> confidence downgrade or controlled abstention
  -> backward-compatible LegalAskResponse + content-free observability event
```

## Component map

| Concern | Implementation |
|---|---|
| Persistent registry, versions, jobs, review items, relationships | `backend/app/modules/legal_knowledge/models.py`, `backend/migrations/versions/0016_legal_source_registry_and_versions.py` |
| Candidate loading | `backend/app/modules/legal_knowledge/source_registry.py` |
| Secure fetching | `backend/app/modules/legal_knowledge/fetcher.py` |
| Bounded discovery | `backend/app/modules/legal_knowledge/discovery.py` |
| Sync orchestration and explicit promotion | `backend/app/modules/legal_knowledge/sync_service.py` |
| Admin operations CLI | `backend/scripts/rag_ops.py` |
| Unified retrieval, RRF, temporal and authority ranking | `backend/app/modules/legal_assistant/unified_retriever.py` |
| Configurable embeddings | `backend/app/modules/legal_assistant/embedding_provider.py` |
| Citation and claim verification | `backend/app/modules/legal_assistant/citation_validator.py` |
| Content-free observability | `backend/app/modules/legal_assistant/observability.py` |
| Evaluation harness | `backend/rag/eval/run_upgrade_eval.py` |

## Evidence rules

- A registry row is a candidate. `verification_status=VERIFIED` is set only after a successful policy-compliant fetch and content validation; CSV-declared `VERIFIED` values are ignored.
- A declared checksum is compared only when the source config explicitly marks it as a content hash. A mismatch fails verification; metadata-derived CSV fingerprints are never treated as content hashes.
- A changed checksum is a **detected change**, not a legally effective amendment. It enters `LegalDocumentVersion` with `PENDING_REVIEW`; only an explicit administrative promotion indexes it.
- Explicit `STATIC_DOCUMENT` URLs may be extensionless official handles; extension filtering applies only to discovered sitemap/feed/listing links.
- Parsing format is inferred from fetched content type/URL before the declarative parser strategy, so stale registry metadata cannot discard a valid HTML/PDF/XML response.
- A section number explicitly named by the user receives a transparent ranking bonus; synonym expansion never silently displaces the cited section.
- Historical versions are immutable. Retrieval filters by validity date unless a historical date is supplied.
- Retrieved web content is parsed as data only; no page text is ever appended to an LLM instruction prompt.
- Official-source fallback only queues candidate documents for review. It never sends raw web text directly to generation.
- No query text, user identity, private document, or legal passage is written to observability output; only hashes, counts, and configuration state are recorded.

## API compatibility

- `LegalAskResponse` retains all pre-upgrade fields. New fields (`claim_support`, `evidence_sufficient`, `retrieval_source`) are additive with safe defaults.
- Existing `/api/v1/legal/ask`, `/api/v1/legal/search`, ingestion, auth, vault, scanning, and other domain routes remain unchanged in behavior except for grounded retrieval diagnostics in audit logs.
- New registry and observability operations are admin-only and additive.
