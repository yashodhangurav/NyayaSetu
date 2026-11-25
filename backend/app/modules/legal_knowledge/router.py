"""Legal Knowledge & Official Statutory Document Ingestion Router."""

from datetime import date
from pathlib import Path
from typing import Any, List, Optional
import uuid

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.errors import BadRequestException
from app.modules.auth.dependencies import require_roles
from app.modules.legal_knowledge.fetcher import FetchError, SecureFetcher
from app.modules.legal_knowledge.ingestion_pipeline import LegalDocumentIngestionPipeline
from app.modules.legal_knowledge.models import (
    LegalChunk,
    LegalDocumentVersion,
    LegalIngestionJob,
    LegalReviewItem,
    LegalSource,
    LegalSourceRegistry,
    LegalSyncJob,
)
from app.modules.legal_knowledge.schemas import (
    DocumentVersionIngestRequest,
    LegalIngestionJobResponse,
    LegalIngestTextRequest,
    LegalSourceSummaryResponse,
    SourceRegistryBootstrapRequest,
    SourceSyncRequest,
    SourceVerificationRequest,
)
from app.modules.legal_knowledge.source_registry import bootstrap_source_registry
from app.modules.legal_knowledge.sync_service import (
    SourceSyncError,
    ingest_document_version,
    sync_source,
    verify_sources,
)
from app.modules.users.models import User

router = APIRouter(prefix="/legal-knowledge", tags=["Legal Knowledge & Statutory Ingestion"])


@router.get("/status", summary="Legal Knowledge Ingestion Status")
async def get_legal_knowledge_status(db: AsyncSession = Depends(get_db)):
    """Diagnostic health status and ingestion metrics for the legal knowledge base."""
    sources_count = await db.scalar(select(func.count(LegalSource.id))) or 0
    chunks_count = await db.scalar(select(func.count(LegalChunk.id))) or 0
    jobs_count = await db.scalar(select(func.count(LegalIngestionJob.id))) or 0

    return {
        "module": "legal_knowledge",
        "status": "initialized",
        "active": True,
        "total_sources": sources_count,
        "total_chunks": chunks_count,
        "total_ingestion_jobs": jobs_count,
    }


# ──────────────────────────────────────────────────────────────
# 1. Admin Text/HTML Ingestion (POST /ingest/text)
# ──────────────────────────────────────────────────────────────


@router.post(
    "/ingest/text",
    response_model=LegalIngestionJobResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Admin: Ingest Statutory Text or HTML",
    description="Parses, chunks, embeds, and stores verified legal text into PostgreSQL/pgvector.",
)
async def ingest_legal_text(
    payload: LegalIngestTextRequest,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(require_roles("ADMIN")),
):
    source_metadata = {
        "title": payload.title,
        "short_code": payload.short_code,
        "source_type": payload.source_type,
        "citation": payload.citation,
        "jurisdiction": payload.jurisdiction,
        "court": payload.court,
        "act_or_judgment_identifier": payload.act_or_judgment_identifier,
        "publication_date": payload.publication_date,
        "document_version": payload.document_version,
        "official_source_url": payload.official_source_url,
        "verification_status": "VERIFIED",
    }

    try:
        source, job = await LegalDocumentIngestionPipeline.ingest_document(
            db=db,
            source_metadata=source_metadata,
            raw_content=payload.content_text,
            file_format=payload.file_format,
            force_reprocess=payload.force_reprocess,
            require_verified_source=True,
        )
        return job
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# ──────────────────────────────────────────────────────────────
# 2. Admin File Upload Ingestion (POST /ingest/file)
# ──────────────────────────────────────────────────────────────


@router.post(
    "/ingest/file",
    response_model=LegalIngestionJobResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Admin: Ingest Legal Document File (PDF, HTML, TXT)",
    description="Upload an official gazette or Bare Act file. Extracts text, chunks provisions, and embeds in pgvector.",
)
async def ingest_legal_file(
    file: UploadFile = File(...),
    title: str = Form(...),
    short_code: Optional[str] = Form(None),
    source_type: str = Form("BARE_ACT"),
    citation: Optional[str] = Form(None),
    jurisdiction: str = Form("Union of India"),
    court: Optional[str] = Form(None),
    act_or_judgment_identifier: Optional[str] = Form(None),
    publication_date: Optional[date] = Form(None),
    document_version: str = Form("1.0"),
    official_source_url: Optional[str] = Form(None),
    force_reprocess: bool = Form(False),
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(require_roles("ADMIN")),
):
    # Read file bytes
    content_bytes = await file.read()
    if not content_bytes:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded file is empty.")

    # Determine file format from filename or content_type
    filename = file.filename or "uploaded_document"
    ext = filename.split(".")[-1].upper() if "." in filename else "TXT"

    source_metadata = {
        "title": title,
        "short_code": short_code,
        "source_type": source_type,
        "citation": citation,
        "jurisdiction": jurisdiction,
        "court": court,
        "act_or_judgment_identifier": act_or_judgment_identifier,
        "publication_date": publication_date,
        "document_version": document_version,
        "official_source_url": official_source_url,
        "verification_status": "VERIFIED",
    }

    try:
        source, job = await LegalDocumentIngestionPipeline.ingest_document(
            db=db,
            source_metadata=source_metadata,
            raw_content=content_bytes,
            file_format=ext,
            filename=filename,
            force_reprocess=force_reprocess,
            require_verified_source=True,
        )
        return job
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# ──────────────────────────────────────────────────────────────
# 3. Ingestion Job Monitoring (GET /jobs)
# ──────────────────────────────────────────────────────────────


@router.get(
    "/jobs",
    response_model=List[LegalIngestionJobResponse],
    summary="Admin: List Ingestion Jobs & Run Logs",
)
async def list_ingestion_jobs(
    status_filter: Optional[str] = Query(None, alias="status"),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(require_roles("ADMIN")),
):
    query = select(LegalIngestionJob).order_by(LegalIngestionJob.created_at.desc()).limit(limit)
    if status_filter:
        query = query.where(LegalIngestionJob.status == status_filter.upper())

    res = await db.execute(query)
    return res.scalars().all()


@router.get(
    "/jobs/{job_id}",
    response_model=LegalIngestionJobResponse,
    summary="Admin: Get Specific Ingestion Job Detail",
)
async def get_ingestion_job(
    job_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(require_roles("ADMIN")),
):
    res = await db.execute(select(LegalIngestionJob).where(LegalIngestionJob.id == job_id))
    job = res.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingestion job not found.")
    return job


# ──────────────────────────────────────────────────────────────
# 4. Verified Legal Sources (GET /sources)
# ──────────────────────────────────────────────────────────────


@router.get(
    "/sources",
    response_model=List[LegalSourceSummaryResponse],
    summary="List Ingested Legal Sources",
)
async def list_legal_sources(
    jurisdiction: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(LegalSource)
        .options(selectinload(LegalSource.chunks))
        .order_by(LegalSource.created_at.desc())
        .limit(limit)
    )
    if jurisdiction:
        query = query.where(LegalSource.jurisdiction == jurisdiction)

    res = await db.execute(query)
    sources = res.scalars().all()

    return [
        LegalSourceSummaryResponse(
            id=s.id,
            title=s.title,
            short_code=s.short_code,
            source_type=s.source_type,
            citation=s.citation,
            jurisdiction=s.jurisdiction,
            court=s.court,
            document_version=s.document_version,
            verification_status=s.verification_status,
            ingestion_status=s.ingestion_status,
            content_checksum=s.content_checksum,
            official_source_url=s.official_source_url,
            total_chunks=len(s.chunks),
            publication_date=s.publication_date,
            last_verified_date=s.last_verified_date,
            created_at=s.created_at,
        )
        for s in sources
    ]


# ──────────────────────────────────────────────────────────────
# 5. Active official-source registry operations (admin only)
# ──────────────────────────────────────────────────────────────


def _registry_row(row: LegalSourceRegistry) -> dict:
    return {
        "registry_key": row.registry_key,
        "name": row.name,
        "official_domain": row.official_domain,
        "source_category": row.source_category,
        "jurisdiction": row.jurisdiction,
        "fetch_strategy": row.fetch_strategy,
        "verification_status": row.verification_status,
        "enabled": row.enabled,
        "last_attempted_fetch": row.last_attempted_fetch,
        "last_successful_fetch": row.last_successful_fetch,
        "failure_count": row.failure_count,
    }


def _version_row(row: LegalDocumentVersion) -> dict:
    return {
        "id": row.id,
        "registry_key": row.registry_key,
        "document_key": row.document_key,
        "title": row.title,
        "source_url": row.source_url,
        "version": row.version,
        "status": row.status,
        "content_checksum": row.content_checksum,
        "jurisdiction": row.jurisdiction,
        "publication_date": row.publication_date,
        "effective_date": row.effective_date,
        "valid_from": row.valid_from,
        "valid_until": row.valid_until,
        "metadata_json": row.metadata_json,
    }


@router.post(
    "/admin/registry/bootstrap",
    status_code=status.HTTP_200_OK,
    summary="Admin: Load declared official sources into the active registry",
)
async def bootstrap_registry(
    payload: SourceRegistryBootstrapRequest,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(require_roles("ADMIN")),
):
    csv_path = Path(payload.csv_path) if payload.csv_path else None
    rows = await bootstrap_source_registry(
        db, path=csv_path, enable_verified=payload.enable_verified
    )
    return {"loaded": len(rows), "all_new_rows_unverified": True}


@router.get(
    "/admin/registry/sources",
    summary="Admin: List active official-source registry rows",
)
async def list_registry_sources(
    verification_status: Optional[str] = Query(None),
    limit: int = Query(200, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(require_roles("ADMIN")),
):
    query = select(LegalSourceRegistry).order_by(LegalSourceRegistry.registry_key).limit(limit)
    if verification_status:
        query = query.where(LegalSourceRegistry.verification_status == verification_status.upper())
    rows = (await db.execute(query)).scalars().all()
    return [_registry_row(row) for row in rows]


@router.post(
    "/admin/registry/verify",
    summary="Admin: Live-verify declared official document URLs",
)
async def verify_registry_sources(
    payload: SourceVerificationRequest,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(require_roles("ADMIN")),
):
    if not payload.source_keys and not payload.verify_all:
        raise BadRequestException("Provide source_keys or verify_all=true")
    try:
        async with SecureFetcher() as fetcher:
            return await verify_sources(
                db,
                fetcher=fetcher,
                source_keys=payload.source_keys or None,
                force=payload.force,
            )
    except (FetchError, SourceSyncError) as exc:
        raise BadRequestException(str(exc)) from exc


@router.post(
    "/admin/registry/sync",
    summary="Admin: Discover, fetch, and queue official documents for review",
)
async def sync_registry_source(
    payload: SourceSyncRequest,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(require_roles("ADMIN")),
):
    try:
        async with SecureFetcher() as fetcher:
            job = await sync_source(
                db,
                source_key=payload.source_key,
                fetcher=fetcher,
                mode=payload.mode,
                force=payload.force,
                enable_verified=payload.enable_verified,
                requested_by=str(admin_user.id),
            )
    except (FetchError, SourceSyncError) as exc:
        raise BadRequestException(str(exc)) from exc
    return {
        "job_id": job.id,
        "source_key": job.source_key,
        "status": job.status,
        "documents_discovered": job.documents_discovered,
        "documents_queued": job.documents_ingested,
        "documents_failed": job.documents_failed,
        "checkpoint": job.checkpoint_json,
    }


@router.get(
    "/admin/registry/jobs",
    summary="Admin: List persistent official-source sync jobs",
)
async def list_registry_jobs(
    source_key: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(require_roles("ADMIN")),
):
    query = select(LegalSyncJob).order_by(LegalSyncJob.created_at.desc()).limit(limit)
    if source_key:
        query = query.where(LegalSyncJob.source_key == source_key)
    rows = (await db.execute(query)).scalars().all()
    return [
        {
            "id": row.id,
            "source_key": row.source_key,
            "mode": row.mode,
            "status": row.status,
            "documents_discovered": row.documents_discovered,
            "documents_queued": row.documents_ingested,
            "documents_failed": row.documents_failed,
            "checkpoint": row.checkpoint_json,
            "error_message": row.error_message,
            "started_at": row.started_at,
            "finished_at": row.finished_at,
        }
        for row in rows
    ]


@router.get(
    "/admin/registry/versions",
    summary="Admin: List fetched immutable document versions",
)
async def list_document_versions(
    registry_key: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    limit: int = Query(100, ge=1, le=300),
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(require_roles("ADMIN")),
):
    query = select(LegalDocumentVersion).order_by(LegalDocumentVersion.created_at.desc()).limit(limit)
    if registry_key:
        query = query.where(LegalDocumentVersion.registry_key == registry_key)
    if status_filter:
        query = query.where(LegalDocumentVersion.status == status_filter.upper())
    rows = (await db.execute(query)).scalars().all()
    return [_version_row(row) for row in rows]


@router.get(
    "/admin/registry/review",
    summary="Admin: List legal review items",
)
async def list_review_items(
    status_filter: Optional[str] = Query(None, alias="status"),
    limit: int = Query(100, ge=1, le=300),
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(require_roles("ADMIN")),
):
    query = select(LegalReviewItem).order_by(LegalReviewItem.created_at.desc()).limit(limit)
    if status_filter:
        query = query.where(LegalReviewItem.status == status_filter.upper())
    rows = (await db.execute(query)).scalars().all()
    return [
        {
            "id": row.id,
            "document_version_id": row.document_version_id,
            "source_key": row.source_key,
            "reason": row.reason,
            "status": row.status,
            "details": row.details_json,
            "resolved_by": row.resolved_by,
            "resolved_at": row.resolved_at,
        }
        for row in rows
    ]


@router.post(
    "/admin/registry/versions/ingest",
    summary="Admin: Promote an approved document version into the searchable corpus",
)
async def promote_document_version(
    payload: DocumentVersionIngestRequest,
    db: AsyncSession = Depends(get_db),
    admin_user: User = Depends(require_roles("ADMIN")),
):
    actor = f"admin:{admin_user.id}"
    if payload.reviewer_note:
        actor += f":{payload.reviewer_note[:80]}"
    try:
        return await ingest_document_version(
            db, version_id=payload.version_id, actor=actor
        )
    except (SourceSyncError, ValueError) as exc:
        raise BadRequestException(str(exc)) from exc
