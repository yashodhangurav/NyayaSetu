"""Legal AI Assistant and Grounded RAG API Router."""

import asyncio
import uuid
from typing import List, Optional

from jwt import InvalidTokenError
from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy import func, select
from sqlalchemy.exc import DBAPIError, OperationalError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.security import decode_jwt
from app.modules.auth.dependencies import oauth2_scheme, require_roles
from app.modules.legal_assistant.schemas import (
    LegalAskRequest,
    LegalAskResponse,
    LegalChunkCreate,
    LegalSearchRequest,
    LegalSearchResponse,
    LegalSourceCreate,
    LegalSourceResponse,
)
from app.modules.legal_assistant.observability import rag_observability
from app.modules.legal_assistant.service import LegalAssistantService, get_hybrid_engine
from app.modules.legal_knowledge.ingestion import LegalIngestionService
from app.modules.legal_knowledge.models import LegalChunk, LegalSource
from app.modules.users.models import User

# Main RAG router mounted under /api/v1/legal
router = APIRouter(prefix="/legal", tags=["Legal AI Assistant (RAG)"])

# Legacy / Health alias router mounted under /api/v1/legal-assistant
alias_router = APIRouter(prefix="/legal-assistant", tags=["Legal AI Assistant (RAG)"])


async def get_optional_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> Optional[User]:
    """Extract user if valid Bearer token provided, otherwise return None."""
    if not token:
        return None
    try:
        payload = decode_jwt(token)
        user_id_str = payload.get("sub")
        if payload.get("type") == "access" and user_id_str:
            async with asyncio.timeout(3 if settings.is_development else None):
                res = await db.execute(select(User).where(User.id == uuid.UUID(user_id_str)))
                return res.scalar_one_or_none()
    except (SQLAlchemyError, DBAPIError, OperationalError, TimeoutError, OSError):
        if not settings.is_development:
            raise
        await db.rollback()
    except (InvalidTokenError, TypeError, ValueError):
        pass
    return None


@router.get("/status", summary="Legal Module Status")
@alias_router.get("/status", summary="Legal Assistant Module Status")
async def get_legal_status():
    """Diagnostic health status for Legal Assistant module."""
    return {"module": "legal_assistant", "status": "initialized", "active": True}


# ──────────────────────────────────────────────────────────────
# Phase 1: Pure Statutory Retrieval Search (/api/v1/legal/search)
# ──────────────────────────────────────────────────────────────


@router.get(
    "/search",
    response_model=LegalSearchResponse,
    status_code=status.HTTP_200_OK,
    summary="Phase 1: Hybrid Legal Search (GET)",
    description="Executes BM25 + dense semantic vector search with concordance mapping and 0% repealed-law leakage.",
)
async def search_legal_corpus_get(
    q: str = Query(..., min_length=2, description="Citizen inquiry or legal topic"),
    top_k: int = Query(5, ge=1, le=20),
    jurisdiction: Optional[str] = Query(None),
):
    engine = get_hybrid_engine()
    return engine.search(query=q, top_k=top_k, jurisdiction=jurisdiction, filter_in_force_only=True)


@router.post(
    "/search",
    response_model=LegalSearchResponse,
    status_code=status.HTTP_200_OK,
    summary="Phase 1: Hybrid Legal Search (POST)",
    description="Executes BM25 + dense semantic vector search with concordance mapping and 0% repealed-law leakage.",
)
async def search_legal_corpus_post(payload: LegalSearchRequest):
    engine = get_hybrid_engine()
    return engine.search(
        query=payload.query,
        top_k=payload.top_k,
        jurisdiction=payload.jurisdiction,
        filter_in_force_only=payload.filter_in_force_only,
    )


# ──────────────────────────────────────────────────────────────
# 1. Grounded Legal AI Question Answering (POST /api/v1/legal/ask)
# ──────────────────────────────────────────────────────────────


@router.post(
    "/ask",
    response_model=LegalAskResponse,
    status_code=status.HTTP_200_OK,
    summary="Ask Legal AI Assistant",
    description=(
        "Executes grounded legal question answering over verified Indian Bare Acts and judicial precedents. "
        "Strictly grounded in retrieved source context; never invents legal sections or fabricates citations. "
        "Returns verified citations, source URLs, content checksums, and actionable next-step guidance."
    ),
)
async def ask_legal_assistant(
    payload: LegalAskRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user),
):
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")

    return await LegalAssistantService.ask(
        db=db,
        payload=payload,
        current_user=current_user,
        ip_address=ip_address,
        user_agent=user_agent,
    )


# ──────────────────────────────────────────────────────────────
# 2. Protected Admin Knowledge Ingestion Workflows
# ──────────────────────────────────────────────────────────────


@router.post(
    "/admin/sources",
    response_model=LegalSourceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Admin: Register Curated Legal Source",
    description="Registers an official Bare Act, published judgment, or legal aid scheme. Admin only.",
)
async def admin_create_source(
    payload: LegalSourceCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_roles("ADMIN")),
):
    source = await LegalIngestionService.create_source(db=db, payload=payload)
    return LegalSourceResponse(
        id=source.id,
        source_type=source.source_type,
        title=source.title,
        short_code=source.short_code,
        citation=source.citation,
        jurisdiction=source.jurisdiction,
        court=source.court,
        act_or_judgment_identifier=source.act_or_judgment_identifier,
        publication_date=source.publication_date,
        last_verified_date=source.last_verified_date,
        document_version=source.document_version,
        content_checksum=source.content_checksum,
        official_source_url=source.official_source_url,
        total_chunks=0,
        created_at=source.created_at,
        updated_at=source.updated_at,
    )


@router.post(
    "/admin/sources/{source_id}/chunks",
    status_code=status.HTTP_201_CREATED,
    summary="Admin: Ingest and Embed Statutory Chunk",
    description="Ingests a section or paragraph, generates dense vector embedding, and stores checksum. Admin only.",
)
async def admin_ingest_chunk(
    source_id: uuid.UUID,
    payload: LegalChunkCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_roles("ADMIN")),
):
    chunk = await LegalIngestionService.ingest_chunk(
        db=db,
        source_id=source_id,
        payload=payload,
    )
    return {
        "id": str(chunk.id),
        "source_id": str(chunk.source_id),
        "section_number": chunk.section_number,
        "clause_heading": chunk.clause_heading,
        "content_checksum": chunk.content_checksum,
        "token_count": chunk.token_count,
        "status": "embedded_and_stored",
    }


@router.post(
    "/admin/seed",
    status_code=status.HTTP_200_OK,
    summary="Admin: Seed Curated Initial Legal Corpus",
    description="Loads official Indian statutory Bare Acts into the vector repository. Admin only.",
)
async def admin_seed_corpus(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_roles("ADMIN")),
):
    count = await LegalIngestionService.seed_curated_corpus(db=db)
    return {"status": "success", "chunks_seeded": count}


@router.get(
    "/admin/observability",
    summary="Admin: RAG operational counters (no user or document content)",
)
async def admin_rag_observability(
    limit: int = Query(20, ge=1, le=100),
    admin: User = Depends(require_roles("ADMIN")),
):
    return rag_observability.summary(limit=limit)


@router.get(
    "/admin/sources",
    response_model=List[LegalSourceResponse],
    summary="Admin: List Curated Legal Sources",
    description="Lists all verified Indian legal sources in the repository. Admin only.",
)
async def admin_list_sources(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_roles("ADMIN")),
):
    res = await db.execute(select(LegalSource).order_by(LegalSource.created_at.desc()))
    sources = res.scalars().all()

    items = []
    for s in sources:
        chunk_count_res = await db.execute(
            select(func.count(LegalChunk.id)).where(LegalChunk.source_id == s.id)
        )
        c_count = chunk_count_res.scalar() or 0
        items.append(
            LegalSourceResponse(
                id=s.id,
                source_type=s.source_type,
                title=s.title,
                short_code=s.short_code,
                citation=s.citation,
                jurisdiction=s.jurisdiction,
                court=s.court,
                act_or_judgment_identifier=s.act_or_judgment_identifier,
                publication_date=s.publication_date,
                last_verified_date=s.last_verified_date,
                document_version=s.document_version,
                content_checksum=s.content_checksum,
                official_source_url=s.official_source_url,
                total_chunks=c_count,
                created_at=s.created_at,
                updated_at=s.updated_at,
            )
        )
    return items
