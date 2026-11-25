"""Add active legal source registry, document versions, sync jobs and review queue.

Revision ID: 0016_legal_source_registry_and_versions
Revises: 0015_advocate_feedback_and_reviews
Create Date: 2026-11-25 00:00:00.000000

Additive only: no existing legal data is modified or removed.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0016_legal_source_registry_and_versions"
down_revision: Union[str, None] = "0015_advocate_feedback_and_reviews"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

JSONB = postgresql.JSONB(astext_type=sa.Text()).with_variant(sa.JSON(), "sqlite")


def upgrade() -> None:
    op.create_table(
        "legal_source_registry",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("registry_key", sa.String(128), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("official_domain", sa.String(255), nullable=False),
        sa.Column("base_url", sa.Text(), nullable=False),
        sa.Column("source_category", sa.String(64), nullable=False),
        sa.Column("jurisdiction", sa.String(128), nullable=False, server_default="Union of India"),
        sa.Column("legal_domains", JSONB, nullable=True),
        sa.Column("document_types", JSONB, nullable=True),
        sa.Column("fetch_strategy", sa.String(64), nullable=False, server_default="STATIC_DOCUMENT"),
        sa.Column("parser_strategy", sa.String(64), nullable=False, server_default="PDF"),
        sa.Column("authority_level", sa.String(64), nullable=False, server_default="OFFICIAL"),
        sa.Column("supported_languages", JSONB, nullable=True),
        sa.Column("update_frequency_hours", sa.Integer(), nullable=True),
        sa.Column("last_successful_fetch", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_attempted_fetch", sa.DateTime(timezone=True), nullable=True),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("verification_status", sa.String(32), nullable=False, server_default="PENDING"),
        sa.Column("failure_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("rate_limit_per_minute", sa.Integer(), nullable=False, server_default="6"),
        sa.Column("source_config", JSONB, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("registry_key", name="uq_legal_source_registry_key"),
    )
    op.create_index("ix_legal_source_registry_id", "legal_source_registry", ["id"])
    for col in ("registry_key", "official_domain", "source_category", "jurisdiction", "enabled", "verification_status"):
        op.create_index(f"ix_legal_source_registry_{col}", "legal_source_registry", [col])

    op.create_table(
        "legal_document_versions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "registry_key",
            sa.String(128),
            sa.ForeignKey("legal_source_registry.registry_key", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("document_key", sa.String(255), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("source_url", sa.Text(), nullable=False),
        sa.Column("version", sa.String(64), nullable=False, server_default="1.0"),
        sa.Column("content_checksum", sa.String(64), nullable=False),
        sa.Column("normalized_text_checksum", sa.String(64), nullable=True),
        sa.Column("raw_storage_key", sa.String(512), nullable=True),
        sa.Column("status", sa.String(32), nullable=False, server_default="PENDING_REVIEW"),
        sa.Column("document_type", sa.String(64), nullable=False, server_default="BARE_ACT"),
        sa.Column("jurisdiction", sa.String(128), nullable=False, server_default="Union of India"),
        sa.Column("authority_level", sa.String(64), nullable=False, server_default="OFFICIAL"),
        sa.Column("publication_date", sa.Date(), nullable=True),
        sa.Column("effective_date", sa.Date(), nullable=True),
        sa.Column("valid_from", sa.Date(), nullable=True),
        sa.Column("valid_until", sa.Date(), nullable=True),
        sa.Column(
            "legal_source_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("legal_sources.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("metadata_json", JSONB, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint(
            "document_key", "content_checksum", name="uq_legal_document_version_checksum"
        ),
    )
    for col in (
        "id", "registry_key", "document_key", "content_checksum",
        "normalized_text_checksum", "status", "legal_source_id",
    ):
        op.create_index(f"ix_legal_document_versions_{col}", "legal_document_versions", [col])

    op.create_table(
        "legal_sync_jobs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("source_key", sa.String(128), nullable=False),
        sa.Column("mode", sa.String(32), nullable=False, server_default="INCREMENTAL"),
        sa.Column("status", sa.String(32), nullable=False, server_default="PENDING"),
        sa.Column("checkpoint_json", JSONB, nullable=True),
        sa.Column("documents_discovered", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("documents_ingested", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("documents_failed", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("requested_by", sa.String(128), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    for col in ("id", "source_key", "status"):
        op.create_index(f"ix_legal_sync_jobs_{col}", "legal_sync_jobs", [col])

    op.create_table(
        "legal_review_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "document_version_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("legal_document_versions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("source_key", sa.String(128), nullable=False),
        sa.Column("reason", sa.String(64), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="PENDING"),
        sa.Column("details_json", JSONB, nullable=True),
        sa.Column("resolved_by", sa.String(128), nullable=True),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    for col in ("id", "document_version_id", "source_key", "reason", "status"):
        op.create_index(f"ix_legal_review_items_{col}", "legal_review_items", [col])

    op.create_table(
        "legal_relationships",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("source_ref", sa.String(128), nullable=False),
        sa.Column("target_ref", sa.String(128), nullable=False),
        sa.Column("relationship_type", sa.String(64), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("jurisdiction", sa.String(128), nullable=False, server_default="Union of India"),
        sa.Column("metadata_json", JSONB, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    for col in ("id", "source_ref", "target_ref", "relationship_type", "jurisdiction"):
        op.create_index(f"ix_legal_relationships_{col}", "legal_relationships", [col])


def downgrade() -> None:
    op.drop_table("legal_relationships")
    op.drop_table("legal_review_items")
    op.drop_table("legal_sync_jobs")
    op.drop_table("legal_document_versions")
    op.drop_table("legal_source_registry")
