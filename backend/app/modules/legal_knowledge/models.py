"""LegalSource and LegalChunk entity models with pgvector embeddings."""

import uuid
from typing import Any, List, Optional
from datetime import date
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Index, Integer, JSON, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

from app.core.config import settings
from app.core.database import Base, TimestampMixin


class LegalSource(Base, TimestampMixin):
    """Parent repository entry for Indian statutes, central codes, and landmark judicial decisions."""

    __tablename__ = "legal_sources"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    source_type: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        index=True,
        comment="BARE_ACT | COURT_JUDGMENT | GAZETTE_NOTIFICATION | LEGAL_AID_SCHEME",
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
        comment="e.g. Bharatiya Nyaya Sanhita 2023, Negotiable Instruments Act 1881",
    )
    short_code: Mapped[Optional[str]] = mapped_column(
        String(64),
        nullable=True,
        index=True,
        comment="BNS, BNSS, BSA, ICA, NI_ACT, RERA, CPA_2019",
    )
    citation: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True,
        comment="Act No. 45 of 2023, (2024) 2 SCC 1",
    )
    jurisdiction: Mapped[str] = mapped_column(
        String(128),
        default="Supreme Court of India / Bharat Central",
        nullable=False,
        index=True,
    )
    court: Mapped[Optional[str]] = mapped_column(
        String(128),
        nullable=True,
        index=True,
        comment="Supreme Court of India, Bombay High Court, Delhi High Court",
    )
    act_or_judgment_identifier: Mapped[Optional[str]] = mapped_column(
        String(128),
        nullable=True,
        index=True,
        comment="e.g., Act No. 26 of 1881, Criminal Appeal No. 1234/2023",
    )
    publication_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )
    last_verified_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )
    document_version: Mapped[str] = mapped_column(
        String(32),
        default="1.0",
        nullable=False,
    )
    content_checksum: Mapped[Optional[str]] = mapped_column(
        String(64),
        nullable=True,
        comment="SHA-256 hexadecimal hash of verified source text",
    )
    year: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        index=True,
    )
    official_source_url: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    verification_status: Mapped[str] = mapped_column(
        String(32),
        default="VERIFIED",
        nullable=False,
        index=True,
        comment="PENDING_VERIFICATION | VERIFIED | REJECTED",
    )
    ingestion_status: Mapped[str] = mapped_column(
        String(32),
        default="COMPLETED",
        nullable=False,
        index=True,
        comment="PENDING | PROCESSING | COMPLETED | FAILED",
    )
    raw_content_path: Mapped[Optional[str]] = mapped_column(
        String(512),
        nullable=True,
        comment="File path to raw ingested document artifact",
    )
    metadata_json: Mapped[Optional[dict]] = mapped_column(
        JSONB().with_variant(JSON, "sqlite"),
        nullable=True,
        default=dict,
    )

    # Relationships
    chunks: Mapped[List["LegalChunk"]] = relationship(
        "LegalChunk",
        back_populates="source",
        cascade="all, delete-orphan",
        order_by="LegalChunk.section_number",
    )
    ingestion_jobs: Mapped[List["LegalIngestionJob"]] = relationship(
        "LegalIngestionJob",
        back_populates="source",
        cascade="all, delete-orphan",
    )


class LegalChunk(Base, TimestampMixin):
    """Statutory section or judgment paragraph vector chunk for semantic similarity retrieval."""

    __tablename__ = "legal_chunks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    source_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("legal_sources.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    section_number: Mapped[Optional[str]] = mapped_column(
        String(64),
        nullable=True,
        index=True,
        comment="e.g., Section 27, Section 74, Section 138, Section 420",
    )
    clause_heading: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="e.g., Agreement in restraint of trade, void",
    )
    chunk_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    token_count: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    content_checksum: Mapped[Optional[str]] = mapped_column(
        String(64),
        nullable=True,
        comment="SHA-256 hash of chunk content",
    )
    embedding_status: Mapped[str] = mapped_column(
        String(32),
        default="COMPLETED",
        nullable=False,
        index=True,
        comment="PENDING | COMPLETED | FAILED",
    )
    metadata_json: Mapped[Optional[dict]] = mapped_column(
        JSONB().with_variant(JSON, "sqlite"),
        nullable=True,
        default=dict,
    )

    # pgvector embedding: dimension is read dynamically from settings
    # (Configurable per embedding model provider e.g. 768 for Gemini, 1536 for OpenAI)
    embedding: Mapped[Optional[Any]] = mapped_column(
        Vector(settings.EMBEDDING_VECTOR_DIMENSION).with_variant(JSON, "sqlite"),
        nullable=True,
        comment=f"Dense vector embedding (configured dimension: {settings.EMBEDDING_VECTOR_DIMENSION})",
    )

    # Relationships
    source: Mapped["LegalSource"] = relationship(
        "LegalSource",
        back_populates="chunks",
    )

    __table_args__ = (
        Index("idx_legal_chunks_source_section", "source_id", "section_number"),
        Index(
            "ix_legal_chunks_embedding_hnsw",
            "embedding",
            postgresql_using="hnsw",
            postgresql_with={"m": 16, "ef_construction": 64},
            postgresql_ops={"embedding": "vector_cosine_ops"},
        ),
    )


class LegalIngestionJob(Base, TimestampMixin):
    """Tracks legal document ingestion runs, extraction metrics, and error logs."""

    __tablename__ = "legal_ingestion_jobs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    source_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("legal_sources.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    source_title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )
    file_format: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        comment="PDF | HTML | TXT | JSON",
    )
    status: Mapped[str] = mapped_column(
        String(32),
        default="PENDING",
        nullable=False,
        index=True,
        comment="PENDING | PROCESSING | COMPLETED | FAILED | DUPLICATE_SKIPPED",
    )
    content_checksum: Mapped[Optional[str]] = mapped_column(
        String(64),
        nullable=True,
        index=True,
        comment="SHA-256 of raw source payload",
    )
    chunks_extracted: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    chunks_embedded: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    error_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    details_json: Mapped[Optional[dict]] = mapped_column(
        JSONB().with_variant(JSON, "sqlite"),
        nullable=True,
        default=dict,
    )

    # Relationships
    source: Mapped[Optional["LegalSource"]] = relationship(
        "LegalSource",
        back_populates="ingestion_jobs",
    )


class LegalSourceRegistry(Base, TimestampMixin):
    """Active configuration and operational state for an official legal source."""

    __tablename__ = "legal_source_registry"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    registry_key: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    official_domain: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    base_url: Mapped[str] = mapped_column(Text, nullable=False)
    source_category: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    jurisdiction: Mapped[str] = mapped_column(String(128), nullable=False, default="Union of India", index=True)
    legal_domains: Mapped[Optional[dict]] = mapped_column(
        JSONB().with_variant(JSON, "sqlite"), nullable=True, default=list
    )
    document_types: Mapped[Optional[dict]] = mapped_column(
        JSONB().with_variant(JSON, "sqlite"), nullable=True, default=list
    )
    fetch_strategy: Mapped[str] = mapped_column(String(64), nullable=False, default="STATIC_DOCUMENT")
    parser_strategy: Mapped[str] = mapped_column(String(64), nullable=False, default="PDF")
    authority_level: Mapped[str] = mapped_column(String(64), nullable=False, default="OFFICIAL")
    supported_languages: Mapped[Optional[dict]] = mapped_column(
        JSONB().with_variant(JSON, "sqlite"), nullable=True, default=list
    )
    update_frequency_hours: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    last_successful_fetch: Mapped[Optional[Any]] = mapped_column(DateTime(timezone=True), nullable=True)
    last_attempted_fetch: Mapped[Optional[Any]] = mapped_column(DateTime(timezone=True), nullable=True)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)
    verification_status: Mapped[str] = mapped_column(
        String(32), nullable=False, default="PENDING", index=True
    )
    failure_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rate_limit_per_minute: Mapped[int] = mapped_column(Integer, nullable=False, default=6)
    source_config: Mapped[Optional[dict]] = mapped_column(
        JSONB().with_variant(JSON, "sqlite"), nullable=True, default=dict
    )


class LegalDocumentVersion(Base, TimestampMixin):
    """Immutable snapshot of a fetched official legal document."""

    __tablename__ = "legal_document_versions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    registry_key: Mapped[str] = mapped_column(
        String(128), ForeignKey("legal_source_registry.registry_key", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    document_key: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    source_url: Mapped[str] = mapped_column(Text, nullable=False)
    version: Mapped[str] = mapped_column(String(64), nullable=False, default="1.0")
    content_checksum: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    normalized_text_checksum: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    raw_storage_key: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    status: Mapped[str] = mapped_column(
        String(32), nullable=False, default="PENDING_REVIEW", index=True
    )
    document_type: Mapped[str] = mapped_column(String(64), nullable=False, default="BARE_ACT")
    jurisdiction: Mapped[str] = mapped_column(String(128), nullable=False, default="Union of India")
    authority_level: Mapped[str] = mapped_column(String(64), nullable=False, default="OFFICIAL")
    publication_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    effective_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    valid_from: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    valid_until: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    legal_source_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("legal_sources.id", ondelete="SET NULL"), nullable=True, index=True
    )
    metadata_json: Mapped[Optional[dict]] = mapped_column(
        JSONB().with_variant(JSON, "sqlite"), nullable=True, default=dict
    )

    __table_args__ = (
        UniqueConstraint("document_key", "content_checksum", name="uq_legal_document_version_checksum"),
    )


class LegalSyncJob(Base, TimestampMixin):
    """Persistent checkpoint and counters for an official-source synchronization run."""

    __tablename__ = "legal_sync_jobs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    source_key: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    mode: Mapped[str] = mapped_column(String(32), nullable=False, default="INCREMENTAL")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="PENDING", index=True)
    checkpoint_json: Mapped[Optional[dict]] = mapped_column(
        JSONB().with_variant(JSON, "sqlite"), nullable=True, default=dict
    )
    documents_discovered: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    documents_ingested: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    documents_failed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    started_at: Mapped[Optional[Any]] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[Optional[Any]] = mapped_column(DateTime(timezone=True), nullable=True)
    requested_by: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)


class LegalReviewItem(Base, TimestampMixin):
    """Ambiguous or changed source content awaiting human legal review."""

    __tablename__ = "legal_review_items"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    document_version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("legal_document_versions.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    source_key: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    reason: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="PENDING", index=True)
    details_json: Mapped[Optional[dict]] = mapped_column(
        JSONB().with_variant(JSON, "sqlite"), nullable=True, default=dict
    )
    resolved_by: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    resolved_at: Mapped[Optional[Any]] = mapped_column(DateTime(timezone=True), nullable=True)


class LegalRelationship(Base, TimestampMixin):
    """Knowledge layer connecting acts to sections, old laws to new laws,
    precedents to interpreted provisions, legal problems to applicable statutes,
    remedies to competent authorities, and procedures to deadlines and documents."""

    __tablename__ = "legal_relationships"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    source_ref: Mapped[str] = mapped_column(
        String(128), nullable=False, index=True,
        comment="Statutory short code, section ref, precedent ID, or legal scenario ID",
    )
    target_ref: Mapped[str] = mapped_column(
        String(128), nullable=False, index=True,
        comment="Target statute, rule, section, forum, procedure, or document requirement",
    )
    relationship_type: Mapped[str] = mapped_column(
        String(64), nullable=False, index=True,
        comment="REPLACES | INTERPRETS | GOVERNED_BY_RULE | APPLIES_TO_PROBLEM | REMEDY_AUTHORITY | REQUIRED_DOCUMENT | STATUTORY_DEADLINE | SUBSECTION | EXCEPTION",
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True,
        comment="Precise legal description of the relationship and statutory basis",
    )
    jurisdiction: Mapped[str] = mapped_column(
        String(128), nullable=False, default="Union of India", index=True
    )
    metadata_json: Mapped[Optional[dict]] = mapped_column(
        JSONB().with_variant(JSON, "sqlite"), nullable=True, default=dict
    )
