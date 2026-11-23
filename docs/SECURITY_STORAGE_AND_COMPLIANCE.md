# Security, storage and compliance

## Authentication and ownership

The [security module](../backend/app/core/security.py) handles password hashing and JWTs. [Auth services](../backend/app/modules/auth/) handle registration, refresh sessions and role checks. Keep administrative roles server-controlled. Domain services must check access to the requested case, file or conversation even when the caller has a valid token.

## Private document storage

The [document module](../backend/app/modules/documents/) authorizes upload, scan, download and deletion. The [storage adapter](../backend/app/core/storage.py) separates storage keys from public URLs. Keep client evidence outside the frontend public directory and keep cloud credentials in the backend environment.

Set `STORAGE_PROVIDER=r2` in production and configure the private bucket, endpoint and access credentials using the [backend settings](../backend/app/core/config.py). Startup validates the provider configuration. Check object availability and permissions separately.

## Moving local documents to R2

From `backend/` with the environment active, inspect the [migration utility](../backend/scripts/migrate_documents_to_cloud.py) and run a dry run before changing storage metadata. Keep local originals and a database backup for rollback.

```bash
python scripts/migrate_documents_to_cloud.py --dry-run
python scripts/migrate_documents_to_cloud.py --execute --batch-size 25
python scripts/migrate_documents_to_cloud.py --verify-only
```

Use `--limit` to constrain a migration. If rollback is necessary, `--rollback --confirm` switches eligible records back to local serving. `--rollback-case` scopes it to a case. Confirm that the local originals are available before rollback.

## Product obligations

Preserve the BCI non-solicitation notice, the legal-assistance disclosure and advocate review of deadline estimates. Keep intake and document-sharing purposes visible and log consent where required. The [repository guide](../AGENTS.md) contains the mandatory wording and access-control conventions. [Isolation and storage tests](../backend/tests/) exercise these boundaries.
