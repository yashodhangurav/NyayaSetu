"""Tests for the active legal-source registry loader and persistence."""

from datetime import date

import pytest
from sqlalchemy import select

from app.modules.legal_knowledge.models import LegalSourceRegistry
from app.modules.legal_knowledge.source_registry import (
    SourceCandidate,
    bootstrap_source_registry,
    is_official_indian_domain,
    load_source_candidates,
    upsert_source_registry,
)


def test_only_https_indian_government_domains_are_official():
    assert is_official_indian_domain("https://www.indiacode.nic.in/handle/1")
    assert is_official_indian_domain("https://egazette.gov.in/WriteReadData/x.pdf")
    assert is_official_indian_domain("https://dpal.karnataka.gov.in/storage/y.pdf")
    assert not is_official_indian_domain("http://indiacode.nic.in/handle/1")
    assert not is_official_indian_domain("https://random-blog.example/law.pdf")
    assert not is_official_indian_domain("not a url")


def test_csv_loader_marks_declared_sources_as_unverified_candidates(tmp_path):
    csv_path = tmp_path / "sources.csv"
    csv_path.write_text(
        "source_id,title,official_url,exact_document_url,source_type,jurisdiction,legal_domains,format,content_checksum\n"
        "SRC_TEST_1,Test Act,https://www.indiacode.nic.in/handle/1,"
        "https://www.indiacode.nic.in/bitstream/1.pdf,CENTRAL_ACT,Union of India,"
        "Property Law; Contracts,PDF,declared-not-a-content-hash\n",
        encoding="utf-8",
    )

    candidates = load_source_candidates(csv_path)

    assert len(candidates) == 1
    candidate = candidates[0]
    assert candidate.fetch_strategy == "STATIC_DOCUMENT"
    assert candidate.parser_strategy == "PDF"
    assert candidate.source_config["declared_checksum_is_content_hash"] is False
    assert candidate.source_config["document_urls"] == [
        "https://www.indiacode.nic.in/bitstream/1.pdf"
    ]


@pytest.mark.asyncio
async def test_registry_upsert_is_idempotent_and_preserves_verification(db_session):
    candidate = SourceCandidate(
        registry_key="SRC_TEST_1",
        name="Test Act",
        official_domain="www.indiacode.nic.in",
        base_url="https://www.indiacode.nic.in/handle/1",
        source_category="CENTRAL_ACT",
        jurisdiction="Union of India",
        legal_domains=["Property Law"],
        document_types=["CENTRAL_ACT"],
        fetch_strategy="STATIC_DOCUMENT",
        parser_strategy="PDF",
        authority_level="TIER 1",
        supported_languages=["English"],
        update_frequency_hours=168,
        source_config={"document_urls": []},
    )

    await upsert_source_registry(db_session, [candidate])
    await upsert_source_registry(db_session, [candidate])

    result = await db_session.execute(
        select(LegalSourceRegistry).where(LegalSourceRegistry.registry_key == "SRC_TEST_1")
    )
    rows = result.scalars().all()
    assert len(rows) == 1
    assert rows[0].verification_status == "PENDING"
    assert rows[0].enabled is False

    rows[0].verification_status = "VERIFIED"
    await db_session.commit()
    await upsert_source_registry(db_session, [candidate], enable_verified=True)

    result = await db_session.execute(
        select(LegalSourceRegistry).where(LegalSourceRegistry.registry_key == "SRC_TEST_1")
    )
    row = result.scalar_one()
    assert row.verification_status == "VERIFIED"
    assert row.enabled is True


@pytest.mark.asyncio
async def test_bootstrap_reads_default_repository_registry(db_session):
    rows = await bootstrap_source_registry(db_session)

    assert len(rows) > 100
    assert all(row.verification_status == "PENDING" for row in rows)
    assert all(row.enabled is False for row in rows)
    assert all(row.source_config["declared_checksum_is_content_hash"] is False for row in rows)
