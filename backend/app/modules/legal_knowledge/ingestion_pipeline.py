"""Production Legal Document Ingestion Pipeline.

Orchestrates verification, deduplication, text extraction, structural chunking,
batch semantic embedding, pgvector storage, and failure tracking.
"""

from datetime import date, datetime, timezone
import hashlib
import os
import re
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import urlparse
import uuid

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.core.logging import logger
from app.modules.legal_assistant.embedding_provider import get_embedding_provider
from app.modules.legal_knowledge.document_parser import DocumentParser
from app.modules.legal_knowledge.legal_chunker import LegalChunker, ParsedLegalChunk
from app.modules.legal_knowledge.models import LegalChunk, LegalIngestionJob, LegalSource


# Authoritative government and judicial domains for Indian legal sources
TRUSTED_LEGAL_DOMAINS = {
    "indiacode.nic.in",
    "egazette.gov.in",
    "gazetteofindia.nic.in",
    "mha.gov.in",
    "meity.gov.in",
    "morth.nic.in",
    "nalsa.gov.in",
    "sci.gov.in",
    "main.sci.gov.in",
    "ecourts.gov.in",
    "judgments.ecourts.gov.in",
    "labour.gov.in",
    "ipindia.gov.in",
    "legislative.gov.in",
}


def compute_sha256(content: Union[str, bytes]) -> str:
    """Compute SHA-256 hash of string or raw bytes."""
    if isinstance(content, str):
        content = content.encode("utf-8")
    return hashlib.sha256(content).hexdigest()


def is_trusted_official_source_url(url: Optional[str]) -> bool:
    """Validate whether an official source URL originates from an accredited government domain."""
    if not url:
        return False
    try:
        parsed = urlparse(url)
        domain = (parsed.netloc or "").lower().split(":")[0]
        return any(domain == trusted or domain.endswith("." + trusted) for trusted in TRUSTED_LEGAL_DOMAINS)
    except Exception:
        return False


class LegalDocumentIngestionPipeline:
    """Production ingestion engine for verified Indian statutes and judicial records."""

    @staticmethod
    def _extract_text(
        content: Union[bytes, str],
        file_format: str,
        filename: Optional[str] = None,
    ) -> str:
        """Extract document text without creating an ingestion job."""
        return DocumentParser.extract_text(
            content=content,
            file_format=file_format,
            filename=filename,
        )

    @classmethod
    async def ingest_document(
        cls,
        db: AsyncSession,
        source_metadata: Dict[str, Any],
        raw_content: Union[bytes, str],
        file_format: str,
        filename: Optional[str] = None,
        force_reprocess: bool = False,
        require_verified_source: bool = True,
        batch_size: int = 50,
    ) -> Tuple[LegalSource, LegalIngestionJob]:
        """Execute the end-to-end ingestion pipeline with idempotency, validation, and failure tracking.
        
        Args:
            db: Active async database session.
            source_metadata: Statutory metadata (title, short_code, citation, jurisdiction, official_source_url, etc.).
            raw_content: Document bytes or text payload.
            file_format: 'PDF', 'HTML', 'TXT', or 'JSON'.
            filename: Optional source file name for format hints.
            force_reprocess: Force chunk re-extraction and re-embedding if already exists.
            require_verified_source: Enforce accredited domain validation and non-rejected status.
            batch_size: Number of chunks embedded per batch call.

        Returns:
            Tuple of (LegalSource, LegalIngestionJob).
        """
        title = source_metadata.get("title", "").strip()
        if not title:
            raise ValueError("Document ingestion requires a valid statutory 'title'.")

        short_code = source_metadata.get("short_code", "").strip() or None
        official_url = source_metadata.get("official_source_url")
        verification_status = source_metadata.get("verification_status", "VERIFIED")

        content_checksum = compute_sha256(raw_content)

        # 1. Verification Gate
        if require_verified_source:
            if verification_status == "REJECTED":
                err_msg = f"Cannot ingest rejected legal source '{title}'."
                job = await cls._record_failed_job(
                    db=db,
                    title=title,
                    file_format=file_format,
                    content_checksum=content_checksum,
                    error=err_msg,
                )
                raise ValueError(err_msg)

            if official_url and not is_trusted_official_source_url(official_url):
                # If explicit URL is provided from an unknown third-party domain, flag it
                err_msg = (
                    f"Untrusted source URL '{official_url}'. Official sources must originate "
                    f"from recognized government portals (IndiaCode, Gazette, Supreme Court, Ministries)."
                )
                job = await cls._record_failed_job(
                    db=db,
                    title=title,
                    file_format=file_format,
                    content_checksum=content_checksum,
                    error=err_msg,
                )
                raise ValueError(err_msg)

        # 2. Duplicate Detection & Idempotency Check
        # Check by content checksum
        existing_source = None
        if content_checksum:
            res_sum = await db.execute(
                select(LegalSource)
                .options(selectinload(LegalSource.chunks))
                .where(LegalSource.content_checksum == content_checksum)
            )
            existing_source = res_sum.scalar_one_or_none()

        # Or check by short_code
        if not existing_source and short_code:
            res_code = await db.execute(
                select(LegalSource)
                .options(selectinload(LegalSource.chunks))
                .where(LegalSource.short_code == short_code)
            )
            existing_source = res_code.scalar_one_or_none()

        # Idempotent skip if source already exists with identical content and chunks
        if existing_source and existing_source.content_checksum == content_checksum and not force_reprocess:
            if existing_source.chunks and len(existing_source.chunks) > 0:
                logger.info(f"Idempotent skip: Source '{title}' ({short_code}) already ingested with matching checksum.")
                job = LegalIngestionJob(
                    source_id=existing_source.id,
                    source_title=title,
                    file_format=file_format.upper(),
                    status="DUPLICATE_SKIPPED",
                    content_checksum=content_checksum,
                    chunks_extracted=len(existing_source.chunks),
                    chunks_embedded=len(existing_source.chunks),
                    details_json={"idempotent_skip": True, "source_id": str(existing_source.id)},
                )
                db.add(job)
                await db.commit()
                await db.refresh(job)
                return existing_source, job

        # 3. Create Ingestion Job Record (PROCESSING)
        job = LegalIngestionJob(
            source_id=existing_source.id if existing_source else None,
            source_title=title,
            file_format=file_format.upper(),
            status="PROCESSING",
            content_checksum=content_checksum,
            details_json={"force_reprocess": force_reprocess},
        )
        db.add(job)
        await db.flush()

        try:
            # 4. Extract Text
            extracted_text = DocumentParser.extract_text(
                content=raw_content,
                file_format=file_format,
                filename=filename,
            )
            if not extracted_text or len(extracted_text.strip()) < 20:
                raise ValueError(f"Extracted document text from '{title}' is empty or insufficient.")

            # 5. Structural Chunking
            jurisdiction = source_metadata.get("jurisdiction", "Union of India")
            document_version = source_metadata.get("document_version", "1.0")

            parsed_chunks: List[ParsedLegalChunk] = LegalChunker.chunk_statute_text(
                text=extracted_text,
                act_title=title,
                jurisdiction=jurisdiction,
                document_version=document_version,
                short_code=short_code,
            )

            if not parsed_chunks:
                raise ValueError(f"Failed to identify statutory sections or schedules in '{title}'.")

            job.chunks_extracted = len(parsed_chunks)

            # 6. Dense Semantic Embedding Generation
            embedding_provider = get_embedding_provider()
            if settings.is_production and embedding_provider.is_mock:
                raise RuntimeError("Production mode cannot use mock embedding provider for legal ingestion.")

            chunk_texts = [
                f"{c.section_number or ''} {c.clause_heading or ''}: {c.chunk_text}"
                for c in parsed_chunks
            ]

            # Batch embedding generation
            embeddings: List[List[float]] = []
            for i in range(0, len(chunk_texts), batch_size):
                batch = chunk_texts[i : i + batch_size]
                batch_vectors = embedding_provider.embed_documents(batch)
                for vec in batch_vectors:
                    if len(vec) != settings.EMBEDDING_VECTOR_DIMENSION:
                        raise ValueError(
                            f"Embedding dimension mismatch: expected {settings.EMBEDDING_VECTOR_DIMENSION}, got {len(vec)}"
                        )
                embeddings.extend(batch_vectors)

            job.chunks_embedded = len(embeddings)

            # 7. Persistence: Create or Update LegalSource
            if existing_source:
                source = existing_source
                # Clean old chunks during reprocessing
                await db.execute(delete(LegalChunk).where(LegalChunk.source_id == source.id))
                source.title = title
                source.content_checksum = content_checksum
                source.document_version = document_version
                source.last_verified_date = source_metadata.get("last_verified_date") or date.today()
                source.verification_status = "VERIFIED"
                source.ingestion_status = "COMPLETED"
                # Update version history metadata
                vh = source.metadata_json.get("version_history", []) if source.metadata_json else []
                vh.append({
                    "version": document_version,
                    "reprocessed_at": datetime.now(timezone.utc).isoformat(),
                    "chunks_count": len(parsed_chunks),
                })
                meta = dict(source.metadata_json or {})
                meta["version_history"] = vh
                source.metadata_json = meta
            else:
                source = LegalSource(
                    source_type=source_metadata.get("source_type", "BARE_ACT"),
                    title=title,
                    short_code=short_code,
                    citation=source_metadata.get("citation"),
                    jurisdiction=jurisdiction,
                    court=source_metadata.get("court"),
                    act_or_judgment_identifier=source_metadata.get("act_or_judgment_identifier"),
                    publication_date=source_metadata.get("publication_date"),
                    last_verified_date=source_metadata.get("last_verified_date") or date.today(),
                    document_version=document_version,
                    content_checksum=content_checksum,
                    year=source_metadata.get("year"),
                    official_source_url=official_url,
                    verification_status="VERIFIED",
                    ingestion_status="COMPLETED",
                    metadata_json=source_metadata.get("metadata_json") or {},
                )
                db.add(source)
                await db.flush()

            # 8. Persist Chunks
            for parsed_chunk, vector in zip(parsed_chunks, embeddings):
                db_chunk = LegalChunk(
                    source_id=source.id,
                    section_number=parsed_chunk.section_number,
                    clause_heading=parsed_chunk.clause_heading,
                    chunk_text=parsed_chunk.chunk_text,
                    token_count=parsed_chunk.token_count,
                    content_checksum=parsed_chunk.content_checksum,
                    embedding_status="COMPLETED",
                    embedding=vector,
                    metadata_json=parsed_chunk.metadata,
                )
                db.add(db_chunk)

            # Update job record
            job.source_id = source.id
            job.status = "COMPLETED"
            job.details_json = {
                "source_title": title,
                "sections_extracted": len(parsed_chunks),
                "sections_embedded": len(embeddings),
                "version": document_version,
            }

            await db.commit()
            await db.refresh(source)
            await db.refresh(job)

            logger.info(
                f"Successfully ingested legal document '{title}' ({len(parsed_chunks)} sections embedded)."
            )
            return source, job

        except Exception as e:
            await db.rollback()
            # Record failure in separate transaction
            sanitized_err = re.sub(r"AIza[a-zA-Z0-9_\-]{20,}", "[REDACTED_API_KEY]", str(e))
            logger.error(f"Legal document ingestion failed for '{title}': {sanitized_err}")

            job.status = "FAILED"
            job.error_message = sanitized_err[:1000]
            db.add(job)
            await db.commit()
            await db.refresh(job)
            raise

    @classmethod
    async def _record_failed_job(
        cls,
        db: AsyncSession,
        title: str,
        file_format: str,
        content_checksum: str,
        error: str,
    ) -> LegalIngestionJob:
        """Create and commit a FAILED LegalIngestionJob entry."""
        job = LegalIngestionJob(
            source_title=title,
            file_format=file_format.upper(),
            status="FAILED",
            content_checksum=content_checksum,
            error_message=error[:1000],
            details_json={"error": error},
        )
        db.add(job)
        await db.commit()
        await db.refresh(job)
        return job
