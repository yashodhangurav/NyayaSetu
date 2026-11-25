"""Operational CLI for the active official legal-source registry.

Examples:
    python scripts/rag_ops.py bootstrap
    python scripts/rag_ops.py verify --all --force
    python scripts/rag_ops.py sync --source SRC_NI_138 --force
    python scripts/rag_ops.py review-list
    python scripts/rag_ops.py ingest-version --version-id <uuid>

``--force`` is an explicit operator override of RAG_SOURCE_FETCH_ENABLED. No
command sends private user data or document-vault content to an external host.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Any, Optional
from uuid import UUID

# Allow direct execution from backend/ (``python scripts/rag_ops.py ...``).
backend_dir = str(Path(__file__).resolve().parent.parent)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from sqlalchemy import select

from app.core.config import settings
from app.core.database import AsyncSessionLocal, initialize_database
from app.modules.legal_knowledge.fetcher import SecureFetcher
from app.modules.legal_knowledge.models import LegalReviewItem, LegalSourceRegistry, LegalSyncJob
from app.modules.legal_knowledge.source_registry import bootstrap_source_registry
from app.modules.legal_knowledge.sync_service import (
    ingest_document_version,
    sync_source,
    verify_sources,
)


def _json_default(value: Any) -> str:
    return str(value)


def _print(payload: Any) -> None:
    print(json.dumps(payload, indent=2, default=_json_default))


async def _session_scope():
    if settings.is_sqlite:
        await initialize_database()
    async with AsyncSessionLocal() as session:
        yield session


async def _bootstrap(args: argparse.Namespace) -> None:
    async for db in _session_scope():
        rows = await bootstrap_source_registry(
            db, path=args.csv, enable_verified=args.enable_verified
        )
    _print({"bootstrapped": len(rows), "all_unverified_by_default": True})


async def _verify(args: argparse.Namespace) -> None:
    keys = [args.source] if args.source else None
    if not keys and not args.all:
        raise SystemExit("Provide --source KEY or --all")
    async with SecureFetcher() as fetcher:
        async for db in _session_scope():
            result = await verify_sources(db, fetcher=fetcher, source_keys=keys, force=args.force)
    _print(result)


async def _sync(args: argparse.Namespace) -> None:
    if not args.source:
        raise SystemExit("--source KEY is required")
    async with SecureFetcher() as fetcher:
        async for db in _session_scope():
            job = await sync_source(
                db,
                source_key=args.source,
                fetcher=fetcher,
                mode=args.mode,
                force=args.force,
                enable_verified=args.enable_verified,
                requested_by=args.actor,
            )
            await db.refresh(job)
    _print(
        {
            "job_id": str(job.id),
            "source_key": job.source_key,
            "status": job.status,
            "documents_discovered": job.documents_discovered,
            "documents_queued": job.documents_ingested,
            "documents_failed": job.documents_failed,
            "error": job.error_message,
        }
    )


async def _review_list(args: argparse.Namespace) -> None:
    async for db in _session_scope():
        query = select(LegalReviewItem).order_by(LegalReviewItem.created_at.desc()).limit(args.limit)
        if args.status:
            query = query.where(LegalReviewItem.status == args.status.upper())
        rows = (await db.execute(query)).scalars().all()
    _print(
        [
            {
                "id": str(row.id),
                "source_key": row.source_key,
                "reason": row.reason,
                "status": row.status,
                "details": row.details_json,
            }
            for row in rows
        ]
    )


async def _ingest_version(args: argparse.Namespace) -> None:
    async for db in _session_scope():
        result = await ingest_document_version(
            db, version_id=UUID(args.version_id), actor=args.actor
        )
    _print(result)


async def _jobs(args: argparse.Namespace) -> None:
    async for db in _session_scope():
        query = select(LegalSyncJob).order_by(LegalSyncJob.created_at.desc()).limit(args.limit)
        if args.source:
            query = query.where(LegalSyncJob.source_key == args.source)
        rows = (await db.execute(query)).scalars().all()
    _print(
        [
            {
                "id": str(row.id),
                "source_key": row.source_key,
                "status": row.status,
                "discovered": row.documents_discovered,
                "queued": row.documents_ingested,
                "failed": row.documents_failed,
                "checkpoint": row.checkpoint_json,
                "error": row.error_message,
            }
            for row in rows
        ]
    )


async def _registry(args: argparse.Namespace) -> None:
    async for db in _session_scope():
        query = select(LegalSourceRegistry).order_by(LegalSourceRegistry.registry_key).limit(args.limit)
        if args.status:
            query = query.where(LegalSourceRegistry.verification_status == args.status.upper())
        rows = (await db.execute(query)).scalars().all()
    _print(
        [
            {
                "registry_key": row.registry_key,
                "name": row.name,
                "official_domain": row.official_domain,
                "fetch_strategy": row.fetch_strategy,
                "verification_status": row.verification_status,
                "enabled": row.enabled,
                "last_successful_fetch": row.last_successful_fetch,
            }
            for row in rows
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="NyayaSetu legal source registry operations")
    sub = parser.add_subparsers(dest="command", required=True)

    bootstrap = sub.add_parser("bootstrap", help="Load declared CSV sources into the persistent registry")
    bootstrap.add_argument("--csv", default=None)
    bootstrap.add_argument("--enable-verified", action="store_true")
    bootstrap.set_defaults(handler=_bootstrap)

    verify = sub.add_parser("verify", help="Live-check declared official document URLs")
    verify.add_argument("--source")
    verify.add_argument("--all", action="store_true")
    verify.add_argument("--force", action="store_true")
    verify.set_defaults(handler=_verify)

    sync = sub.add_parser("sync", help="Discover, fetch, and queue official documents for review")
    sync.add_argument("--source", required=True)
    sync.add_argument("--mode", default="INCREMENTAL")
    sync.add_argument("--force", action="store_true")
    sync.add_argument("--enable-verified", action="store_true")
    sync.add_argument("--actor", default=None)
    sync.set_defaults(handler=_sync)

    review = sub.add_parser("review-list", help="List items awaiting legal review")
    review.add_argument("--status")
    review.add_argument("--limit", type=int, default=50)
    review.set_defaults(handler=_review_list)

    ingest = sub.add_parser("ingest-version", help="Promote an approved document version into the corpus")
    ingest.add_argument("--version-id", required=True)
    ingest.add_argument("--actor", default=None)
    ingest.set_defaults(handler=_ingest_version)

    jobs = sub.add_parser("jobs", help="List persistent source sync jobs")
    jobs.add_argument("--source")
    jobs.add_argument("--limit", type=int, default=50)
    jobs.set_defaults(handler=_jobs)

    registry = sub.add_parser("registry", help="List persisted registry rows")
    registry.add_argument("--status")
    registry.add_argument("--limit", type=int, default=200)
    registry.set_defaults(handler=_registry)

    return parser


def main() -> None:
    args = build_parser().parse_args()
    asyncio.run(args.handler(args))


if __name__ == "__main__":
    main()
