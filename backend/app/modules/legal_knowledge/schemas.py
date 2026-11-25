"""Pydantic schemas for the Legal Knowledge Ingestion Pipeline."""

from datetime import date, datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class LegalIngestTextRequest(BaseModel):
    """Payload for submitting raw legal text/HTML/JSON for structured ingestion."""

    title: str = Field(..., min_length=3, max_length=255, description="Official title of the statute or judgment")
    short_code: Optional[str] = Field(None, max_length=64, description="Standard statutory acronym (e.g. BNS, NI_ACT)")
    source_type: str = Field("BARE_ACT", description="BARE_ACT | COURT_JUDGMENT | GAZETTE_NOTIFICATION | LEGAL_AID_SCHEME")
    citation: Optional[str] = Field(None, max_length=255, description="Official Act number or law report citation")
    jurisdiction: str = Field("Union of India", max_length=128)
    court: Optional[str] = Field(None, max_length=128)
    act_or_judgment_identifier: Optional[str] = Field(None, max_length=128)
    publication_date: Optional[date] = None
    document_version: str = Field("1.0", max_length=32)
    official_source_url: Optional[str] = Field(None, description="Government or court publication URL")
    content_text: str = Field(..., min_length=20, description="Raw statutory or judgment text content")
    file_format: str = Field("TXT", description="TXT | HTML | JSON")
    force_reprocess: bool = Field(False, description="Whether to reprocess and re-embed if document already exists")


class LegalIngestionJobResponse(BaseModel):
    """Schema representing an ingestion run and its extraction metrics."""

    id: UUID
    source_id: Optional[UUID] = None
    source_title: str
    file_format: str
    status: str = Field(..., description="PENDING | PROCESSING | COMPLETED | FAILED | DUPLICATE_SKIPPED")
    content_checksum: Optional[str] = None
    chunks_extracted: int = 0
    chunks_embedded: int = 0
    error_message: Optional[str] = None
    details_json: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SourceRegistryBootstrapRequest(BaseModel):
    """Load declared official-source candidates into the persistent registry."""

    csv_path: Optional[str] = Field(None, description="Optional absolute path to an alternate registry CSV")
    enable_verified: bool = Field(False, description="Enable rows that were previously live-verified")


class SourceVerificationRequest(BaseModel):
    """Request live verification of declared official document URLs."""

    source_keys: List[str] = Field(default_factory=list, max_length=500)
    verify_all: bool = Field(False)
    force: bool = Field(False, description="Override RAG_SOURCE_FETCH_ENABLED for this explicit action")


class SourceSyncRequest(BaseModel):
    """Request discovery, fetch, checksum, and review-queue creation."""

    source_key: str = Field(..., min_length=2, max_length=128)
    mode: str = Field("INCREMENTAL", max_length=32)
    force: bool = Field(False)
    enable_verified: bool = Field(False)


class DocumentVersionIngestRequest(BaseModel):
    """Explicit administrative promotion of an approved document version."""

    version_id: UUID
    reviewer_note: Optional[str] = Field(None, max_length=1000)


class LegalSourceSummaryResponse(BaseModel):
    """Public summary representation of an ingested legal source."""

    id: UUID
    title: str
    short_code: Optional[str] = None
    source_type: str
    citation: Optional[str] = None
    jurisdiction: str
    court: Optional[str] = None
    document_version: str
    verification_status: str
    ingestion_status: str
    content_checksum: Optional[str] = None
    official_source_url: Optional[str] = None
    total_chunks: int = 0
    publication_date: Optional[date] = None
    last_verified_date: Optional[date] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
