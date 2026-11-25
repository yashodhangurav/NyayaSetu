# Legal Source Registry

`docs/source_registry.csv` is a declaration of **candidate** official sources, not proof that a URL works, that a document is current, or that a declared checksum matches downloaded bytes. The generator `backend/rag/ingest/build_expanded_registry.py` produces metadata-only placeholders; the runtime pipeline replaces them with checksums of actually fetched bytes before a version is verified.

Verified 2026-11-25 from the current file: **161 candidate rows with 161 unique source IDs; 155 include a declared document URL and use the `STATIC_DOCUMENT` fetch strategy.** These are declarative counts only, not live-verified sources.

Runtime status after the completion pass: **1 source (`SRC_PROC_KAVERI_001`) fetch-verified** through the CLI with a policy-compliant HTTP 200 and content hash `149ea6f7d95b8ca71bc9c12f8de80116f30a688b4cd1c4e8a1a7dca22178c3ed`. Its live sync discovered one document and queued one `PENDING_REVIEW` version; `legal_sources` and `legal_chunks` remain empty. The other 160 rows remain unverified. Many live checks failed robots policy, returned 404, had certificate failures, or had unresolvable hosts; no check was bypassed. Fetch verification does not establish legal authenticity or current-law validity.

## Registry fields

The persistent registry stores: unique key, name, official domain, base URL, category, jurisdiction, legal domains, document types, fetch strategy, parser strategy, authority level, supported languages, update frequency, last successful fetch, last attempted fetch, enabled flag, verification status, failure count, rate limit, and source-specific JSON configuration.

The runtime loader (`source_registry.py`) deliberately:

- requires HTTPS on Indian government/public legal domains;
- keeps every loaded row `PENDING` and disabled by default;
- ignores CSV-declared `verification_status` and `ingestion_status`;
- treats `content_checksum` as a declared value with `declared_checksum_is_content_hash=False` until real bytes are fetched.

## Verification sequence

1. Parse and normalize URL; require HTTPS and an official Indian legal domain.
2. Resolve DNS and reject private/loopback/link-local/multicast destinations (SSRF protection).
3. Fetch `robots.txt` and require permission for the target path and user agent. A robots failure fails closed.
4. Fetch with bounded retries, timeout, redirect validation, maximum bytes, and allowed content types.
5. Send `If-None-Match` / `If-Modified-Since` when prior metadata exists.
6. Hash actual fetched bytes; compare with a declared checksum only when the source config explicitly marks that checksum as a real content hash. A declared mismatch fails verification, is reported as `DECLARED_CHECKSUM_MISMATCH`, and does not mark the source verified or overwrite a prior version. Separately, changed checksums between synced versions create a `LegalReviewItem`.
7. Only then mark the source `VERIFIED` and allow synchronization when enabled.
8. During sync, parse using the fetched content type/URL before the declarative parser strategy; a stale `PDF` label must not discard an HTML response.

## Operational commands

From `backend/` with the virtual environment active:

```powershell
python scripts/rag_ops.py bootstrap
python scripts/rag_ops.py verify --source SRC_NI_138 --force
python scripts/rag_ops.py sync --source SRC_NI_138 --force
python scripts/rag_ops.py review-list
python scripts/rag_ops.py ingest-version --version-id <uuid>
python scripts/rag_ops.py jobs
python scripts/rag_ops.py registry
```

Administrative API equivalents are mounted under `/api/v1/legal-knowledge/admin/registry/*`.

## Enabling automated sources

Automated fetching is disabled by default (`RAG_SOURCE_FETCH_ENABLED=false`). Enable only after an operator verifies the source's terms of use and runs `rag_ops.py verify`. Sources without an official API or accessible listing remain `STATIC_DOCUMENT` candidates and are fetched only from declared, verified document URLs. Explicit static URLs may be extensionless official handles; the extension heuristic is applied only to discovered sitemap/feed/listing links. When `RAG_OFFICIAL_FALLBACK_ENABLED=true`, that flag is itself the operator opt-in and forces its own sync despite the default fetch flag, still queueing only reviewed documents. No CAPTCHA, login, paywall, or access control is bypassed.

## Promotion policy

- Fetched bytes are stored under `legal-sources/<source>/<sha256>` through the configured storage provider.
- Every fetched document becomes an immutable `LegalDocumentVersion` with `PENDING_REVIEW`.
- New documents, changed checksums, and ambiguous commencement states (`PARTIALLY_COMMENCED`, `MODEL_LAW`, `HISTORICAL`, `REPEALED`, `SUPERSEDED`, `UNKNOWN`) create `LegalReviewItem` rows.
- Only `rag_ops.py ingest-version` or `POST /api/v1/legal-knowledge/admin/registry/versions/ingest` calls the existing ingestion pipeline and marks the version `INDEXED`.
- No automated legal determination of commencement, repeal, or amendment is performed.
