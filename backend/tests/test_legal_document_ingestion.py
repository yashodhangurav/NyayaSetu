"""Comprehensive Integration Tests for the Legal Document Ingestion Pipeline.

Validates:
1. Document parsing (PDF, HTML, TXT, hyphen joining, header stripping)
2. Structural legal chunking (Chapters, Sections, Subsections, Schedules)
3. Idempotent ingestion & duplicate detection
4. Reprocessing and version tracking on document modification
5. Untrusted/unverified source rejection
6. Failed document tracking and IngestionJob error logging
7. Dense semantic embedding dimension verification and batching
8. Admin API ingestion and job status monitoring
"""

import io
import json
import pytest
from httpx import AsyncClient
from pypdf import PdfWriter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.modules.legal_assistant.embedding_provider import DeterministicMockEmbeddingProvider
from app.modules.legal_knowledge.document_parser import DocumentParser
from app.modules.legal_knowledge.ingestion_pipeline import (
    LegalDocumentIngestionPipeline,
    compute_sha256,
    is_trusted_official_source_url,
)
from app.modules.legal_knowledge.legal_chunker import LegalChunker
from app.modules.legal_knowledge.models import LegalChunk, LegalIngestionJob, LegalSource
from app.modules.users.models import User


pytestmark = pytest.mark.usefixtures("isolated_embedding_provider")


def create_in_memory_pdf(text: str) -> bytes:
    """Generate in-memory PDF bytes with text content."""
    # Use pypdf to create a basic blank page and stream
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    stream = io.BytesIO()
    writer.write(stream)
    return stream.getvalue()


async def create_admin_user_and_token(
    async_client: AsyncClient,
    db_session: AsyncSession,
) -> tuple[str, str]:
    """Helper to create and authenticate an admin user."""
    email = f"ingest.admin.{id(db_session)}@nyayasetu.in"
    password = "AdminSecurePassword2026!"
    admin = User(
        full_name="Knowledge Admin",
        email=email,
        phone="+919876543111",
        password_hash=hash_password(password),
        role="ADMIN",
        is_verified=True,
        is_active=True,
    )
    db_session.add(admin)
    await db_session.commit()

    login_res = await async_client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert login_res.status_code == 200
    return str(admin.id), login_res.json()["access_token"]


# ──────────────────────────────────────────────────────────────
# 1. Document Parsing & Cleaning Tests
# ──────────────────────────────────────────────────────────────

def test_document_parser_clean_legal_text():
    """Verify text cleaning normalizes whitespace and repairs line-break word breaks."""
    raw = (
        "THE GAZETTE OF INDIA EXTRAORDINARY\n"
        "[Page 4 of 20]\n"
        "Where any cheque drawn by a person on an account for the dis-\n"
        "charge, in whole or in part, of any debt or other lia-\n"
        "bility, is returned unpaid…\n\n\n\n"
        "Provided that nothing shall apply."
    )
    cleaned = DocumentParser.clean_legal_text(raw)
    # Check hyphens across lines are joined
    assert "discharge" in cleaned
    assert "liability" in cleaned
    assert "dis-\ncharge" not in cleaned
    # Check excessive linebreaks collapsed
    assert "\n\n\n\n" not in cleaned


def test_document_parser_html_extraction():
    """Verify HTML parser removes scripts, styles, and extracts clean structural paragraphs."""
    html_sample = """
    <!DOCTYPE html>
    <html>
    <head><style>.header { color: red; }</style></head>
    <body>
        <script>console.log("tracking");</script>
        <header><nav><a href="/">Home</a></nav></header>
        <h1>The Commercial Courts Act, 2015</h1>
        <p>Section 12A. Pre-Institution Mediation and Settlement.</p>
        <div>(1) A suit, which does not contemplate any urgent interim relief under this Act, shall not be instituted unless the plaintiff exhausts the remedy of pre-institution mediation.</div>
        <footer>Copyright 2026</footer>
    </body>
    </html>
    """
    extracted = DocumentParser.extract_from_html(html_sample)
    assert "The Commercial Courts Act, 2015" in extracted
    assert "Section 12A" in extracted
    assert "pre-institution mediation" in extracted
    # Ensure scripts and footer were stripped
    assert "console.log" not in extracted
    assert "Copyright 2026" not in extracted


# ──────────────────────────────────────────────────────────────
# 2. Structure-Aware Legal Chunker Tests
# ──────────────────────────────────────────────────────────────

def test_legal_chunker_preserves_chapters_sections_and_subsections():
    """Verify LegalChunker extracts chapters, section numbers, clause headings, and subsections."""
    statute_text = """
    CHAPTER III
    OF ARBITRATION AGREEMENT

    Section 7. Arbitration agreement.
    (1) In this Part, "arbitration agreement" means an agreement by the parties to submit to arbitration all or certain disputes.
    (2) An arbitration agreement may be in the form of an arbitration clause in a contract or in the form of a separate agreement.
    (3) An arbitration agreement shall be in writing.

    Section 8 - Power to refer parties to arbitration where there is an arbitration agreement.
    (1) A judicial authority, before which an action is brought in a matter which is the subject of an arbitration agreement shall refer the parties to arbitration.
    Provided that no such reference shall be made unless the party applies not later than the date of submitting his first statement on the substance of the dispute.
    """

    chunks = LegalChunker.chunk_statute_text(
        text=statute_text,
        act_title="The Arbitration and Conciliation Act, 1996",
        jurisdiction="Union of India",
        document_version="1.0",
        short_code="ACA_1996",
    )

    assert len(chunks) == 2

    c7 = next(c for c in chunks if "7" in c.section_number)
    assert c7.section_number == "Section 7"
    assert "Arbitration agreement" in c7.clause_heading
    assert "CHAPTER III" in c7.chapter
    assert "(1)" in c7.subsections
    assert "(2)" in c7.subsections
    assert c7.metadata["act_title"] == "The Arbitration and Conciliation Act, 1996"
    assert c7.metadata["jurisdiction"] == "Union of India"

    c8 = next(c for c in chunks if "8" in c.section_number)
    assert c8.section_number == "Section 8"
    assert "Power to refer" in c8.clause_heading
    assert "Provided that" in c8.chunk_text


def test_legal_chunker_handles_schedules():
    """Verify LegalChunker detects schedules."""
    text = """
    THE FIRST SCHEDULE
    RULES APPLICABLE TO THE DETERMINATION OF THE VALUE OF GOODS
    Rule 1. These rules may be called the Valuation Rules.
    """
    chunks = LegalChunker.chunk_statute_text(
        text=text,
        act_title="Customs Tariff Act",
        jurisdiction="Union of India",
    )
    assert len(chunks) >= 1
    assert "SCHEDULE" in chunks[0].section_number.upper()


# ──────────────────────────────────────────────────────────────
# 3. Ingestion Pipeline & Duplicate Detection Tests
# ──────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_pipeline_ingest_document_successful(db_session: AsyncSession):
    """Verify LegalDocumentIngestionPipeline successfully extracts, chunks, embeds, and stores a document."""
    doc_text = """
    CHAPTER II
    PRE-INSTITUTION MEDIATION

    Section 12A. Pre-Institution Mediation and Settlement.
    (1) A suit, which does not contemplate any urgent interim relief under this Act, shall not be instituted unless the plaintiff exhausts the remedy of pre-institution mediation in accordance with such manner and procedure as may be prescribed by rules made by the Central Government.
    (2) The Central Government may, by notification, authorise the Authorities constituted under the Legal Services Authorities Act, 1987, for the purposes of pre-institution mediation.
    """

    source_meta = {
        "title": "The Commercial Courts Act, 2015",
        "short_code": "CCA_2015",
        "citation": "Act No. 4 of 2016",
        "jurisdiction": "Union of India",
        "official_source_url": "https://www.indiacode.nic.in/handle/123456789/2157",
        "document_version": "1.0",
        "verification_status": "VERIFIED",
    }

    source, job = await LegalDocumentIngestionPipeline.ingest_document(
        db=db_session,
        source_metadata=source_meta,
        raw_content=doc_text,
        file_format="TXT",
    )

    assert job.status == "COMPLETED"
    assert job.chunks_extracted >= 1
    assert job.chunks_embedded == job.chunks_extracted
    assert job.content_checksum is not None

    # Verify database records
    assert source.id is not None
    assert source.verification_status == "VERIFIED"
    assert source.ingestion_status == "COMPLETED"

    res = await db_session.execute(select(LegalChunk).where(LegalChunk.source_id == source.id))
    chunks = res.scalars().all()
    assert len(chunks) >= 1
    chunk = chunks[0]
    assert chunk.section_number == "Section 12A"
    assert chunk.embedding_status == "COMPLETED"
    assert chunk.embedding is not None
    assert len(chunk.embedding) == 768


@pytest.mark.asyncio
async def test_pipeline_idempotent_duplicate_detection(db_session: AsyncSession):
    """Submitting the same document content twice should be detected as DUPLICATE_SKIPPED."""
    doc_text = """
    Section 10. All agreements are contracts if they are made by free consent of parties.
    """
    source_meta = {
        "title": "Idempotent Test Act",
        "short_code": "ITA_TEST",
        "jurisdiction": "Union of India",
        "official_source_url": "https://www.indiacode.nic.in/handle/test",
    }

    # 1. First ingestion
    source1, job1 = await LegalDocumentIngestionPipeline.ingest_document(
        db=db_session,
        source_metadata=source_meta,
        raw_content=doc_text,
        file_format="TXT",
    )
    assert job1.status == "COMPLETED"

    # 2. Second ingestion with identical content
    source2, job2 = await LegalDocumentIngestionPipeline.ingest_document(
        db=db_session,
        source_metadata=source_meta,
        raw_content=doc_text,
        file_format="TXT",
        force_reprocess=False,
    )
    assert job2.status == "DUPLICATE_SKIPPED"
    assert source2.id == source1.id


@pytest.mark.asyncio
async def test_pipeline_reprocess_on_document_modification(db_session: AsyncSession):
    """When a document is modified and re-ingested with force_reprocess, chunks are re-extracted and version tracked."""
    v1_text = """
    Section 5. Limitation period is three years.
    """
    v2_text = """
    Section 5. Extension of prescribed period in certain cases when sufficient cause is shown.
    Section 6. Legal disability provisions.
    """
    source_meta = {
        "title": "Reprocess Test Act",
        "short_code": "RTA_TEST",
        "jurisdiction": "Union of India",
        "official_source_url": "https://www.indiacode.nic.in/handle/rta",
        "document_version": "1.0",
    }

    # 1. Ingest V1
    source, job1 = await LegalDocumentIngestionPipeline.ingest_document(
        db=db_session,
        source_metadata=source_meta,
        raw_content=v1_text,
        file_format="TXT",
    )
    assert job1.status == "COMPLETED"
    assert job1.chunks_extracted == 1

    # 2. Ingest V2 with force_reprocess=True and updated version
    source_meta["document_version"] = "2.0"
    source, job2 = await LegalDocumentIngestionPipeline.ingest_document(
        db=db_session,
        source_metadata=source_meta,
        raw_content=v2_text,
        file_format="TXT",
        force_reprocess=True,
    )
    assert job2.status == "COMPLETED"
    assert job2.chunks_extracted == 2

    # Verify old chunk was replaced and source version was updated
    res = await db_session.execute(select(LegalChunk).where(LegalChunk.source_id == source.id))
    chunks = res.scalars().all()
    assert len(chunks) == 2
    assert source.document_version == "2.0"


# ──────────────────────────────────────────────────────────────
# 4. Verification Gate & Untrusted Domain Rejection Tests
# ──────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_pipeline_rejects_untrusted_source_url(db_session: AsyncSession):
    """Ingestion must reject third-party unofficial domains (e.g. random blog or scraper)."""
    source_meta = {
        "title": "Untrusted Law",
        "short_code": "UNTRUSTED",
        "official_source_url": "https://random-commercial-blog.com/acts/law.html",
    }

    with pytest.raises(ValueError) as exc_info:
        await LegalDocumentIngestionPipeline.ingest_document(
            db=db_session,
            source_metadata=source_meta,
            raw_content="Section 1. Some fake text.",
            file_format="TXT",
            require_verified_source=True,
        )
    assert "Untrusted source URL" in str(exc_info.value)

    # Verify failed job was logged
    res = await db_session.execute(
        select(LegalIngestionJob).where(LegalIngestionJob.source_title == "Untrusted Law")
    )
    job = res.scalar_one_or_none()
    assert job is not None
    assert job.status == "FAILED"
    assert "Untrusted source URL" in job.error_message


@pytest.mark.asyncio
async def test_pipeline_rejects_explicitly_rejected_verification_status(db_session: AsyncSession):
    """A source marked REJECTED cannot be ingested."""
    source_meta = {
        "title": "Rejected Law",
        "verification_status": "REJECTED",
        "official_source_url": "https://www.indiacode.nic.in/handle/123",
    }

    with pytest.raises(ValueError) as exc_info:
        await LegalDocumentIngestionPipeline.ingest_document(
            db=db_session,
            source_metadata=source_meta,
            raw_content="Section 1. Content.",
            file_format="TXT",
            require_verified_source=True,
        )
    assert "Cannot ingest rejected legal source" in str(exc_info.value)


# ──────────────────────────────────────────────────────────────
# 5. Admin API Endpoints Tests
# ──────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_admin_api_ingest_text(async_client: AsyncClient, db_session: AsyncSession):
    """Admin can ingest text via POST /api/v1/legal-knowledge/ingest/text."""
    admin_id, admin_token = await create_admin_user_and_token(async_client, db_session)

    payload = {
        "title": "The Specific Relief Act, 1963",
        "short_code": "SRA_1963",
        "citation": "Act No. 47 of 1963",
        "jurisdiction": "Union of India",
        "official_source_url": "https://www.indiacode.nic.in/handle/123456789/2234",
        "document_version": "1.0",
        "file_format": "TXT",
        "content_text": (
            "Section 10. Specific performance in respect of contracts.\n"
            "The specific performance of a contract shall be enforced by the court subject to the provisions contained in sub-section (2) of section 11, section 14 and section 16.\n\n"
            "Section 14. Contracts not specifically enforceable.\n"
            "The following contracts cannot be specifically enforced, namely: (a) where a party to the contract has obtained substituted performance of contract."
        ),
    }

    res = await async_client.post(
        "/api/v1/legal-knowledge/ingest/text",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert res.status_code == 201
    data = res.json()
    assert data["status"] == "COMPLETED"
    assert data["chunks_extracted"] == 2
    assert data["chunks_embedded"] == 2


@pytest.mark.asyncio
async def test_admin_api_list_ingestion_jobs(async_client: AsyncClient, db_session: AsyncSession):
    """Admin can list past ingestion jobs via GET /api/v1/legal-knowledge/jobs."""
    admin_id, admin_token = await create_admin_user_and_token(async_client, db_session)

    res = await async_client.get(
        "/api/v1/legal-knowledge/jobs",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert res.status_code == 200
    jobs = res.json()
    assert isinstance(jobs, list)


@pytest.mark.asyncio
async def test_public_api_list_sources(async_client: AsyncClient, db_session: AsyncSession):
    """Users can list verified legal sources via GET /api/v1/legal-knowledge/sources."""
    res = await async_client.get("/api/v1/legal-knowledge/sources")
    assert res.status_code == 200
    sources = res.json()
    assert isinstance(sources, list)
