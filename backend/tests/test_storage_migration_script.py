"""Automated unit and integration test suite for NyayaSetu Document Storage Migration Utility."""

import hashlib
from pathlib import Path
import tempfile
from typing import Dict
import uuid
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.storage import BaseStorageProvider
from app.modules.cases.models import LegalCase
from app.modules.documents.models import Document
from app.modules.users.models import User, UserRole
from scripts.migrate_documents_to_cloud import generate_migration_storage_key, run_migration


class MockCloudStorageProvider(BaseStorageProvider):
    """In-memory mock Cloudflare R2 storage provider for testing migration."""

    def __init__(self, bucket_name: str = "nyayasetu-vault"):
        self.bucket_name = bucket_name
        self.objects: Dict[str, bytes] = {}
        self.uploaded_keys = []

    @property
    def backend_name(self) -> str:
        return "r2"

    @property
    def supports_presigned_urls(self) -> bool:
        return True

    async def upload(self, key: str, content, content_type: str = "application/octet-stream", metadata=None) -> str:
        clean_key = key.replace("\\", "/").lstrip("/")
        if isinstance(content, bytes):
            data = content
        else:
            data = content.read()
        self.objects[clean_key] = data
        self.uploaded_keys.append(clean_key)
        return clean_key

    async def download(self, key: str) -> bytes:
        clean_key = key.replace("\\", "/").lstrip("/")
        if clean_key not in self.objects:
            raise Exception("Object not found")
        return self.objects[clean_key]

    async def delete(self, key: str) -> bool:
        clean_key = key.replace("\\", "/").lstrip("/")
        self.objects.pop(clean_key, None)
        return True

    async def exists(self, key: str) -> bool:
        clean_key = key.replace("\\", "/").lstrip("/")
        return clean_key in self.objects

    async def generate_download_url(self, key: str, expiry_seconds: int = 900, filename=None, inline=False) -> str:
        clean_key = key.replace("\\", "/").lstrip("/")
        return f"https://mock-r2.cloudflarestorage.com/{self.bucket_name}/{clean_key}?expires={expiry_seconds}"

    def get_local_path(self, key: str):
        return None


async def setup_migration_test_case(db_session: AsyncSession) -> tuple[User, LegalCase]:
    """Create test citizen user and legal case."""
    unique_suffix = uuid.uuid4().hex[:8]
    user = User(
        id=uuid.uuid4(),
        phone=f"+9198{unique_suffix}",
        email=f"client_{unique_suffix}@example.com",
        full_name="Test Citizen Client",
        password_hash="test-password-hash",
        role=UserRole.CITIZEN,
        is_active=True,
    )
    db_session.add(user)
    await db_session.flush()

    case = LegalCase(
        id=uuid.uuid4(),
        client_id=user.id,
        case_reference=f"MIG-{unique_suffix.upper()}",
        title="Storage Migration Test Case",
        practice_group="Disputes",
        matter_type="Civil Suit",
    )
    db_session.add(case)
    await db_session.flush()
    return user, case


def test_generate_migration_storage_key():
    """Verify generated storage key format and randomness."""
    doc = Document(
        id=uuid.uuid4(),
        case_id=uuid.uuid4(),
        file_name="affidavit.pdf",
    )
    key = generate_migration_storage_key(doc)
    assert key.startswith(f"vault/cases/{doc.case_id}/{doc.id}_")
    assert key.endswith("_affidavit.pdf")
    # Verify randomness across invocations
    key2 = generate_migration_storage_key(doc)
    assert key != key2


@pytest.mark.asyncio
async def test_migration_dry_run_is_read_only(db_session: AsyncSession):
    """Test that dry-run mode identifies files without uploading or modifying the database."""
    user, case = await setup_migration_test_case(db_session)

    with tempfile.TemporaryDirectory() as temp_vault:
        vault_path = Path(temp_vault)
        case_vault = vault_path / str(case.id)
        case_vault.mkdir(parents=True, exist_ok=True)

        doc_id = uuid.uuid4()
        sample_bytes = b"%PDF-1.4 sample evidence affidavit content"
        local_file = case_vault / f"{doc_id}_evidence.pdf"
        local_file.write_bytes(sample_bytes)

        checksum = hashlib.sha256(sample_bytes).hexdigest()

        doc = Document(
            id=doc_id,
            case_id=case.id,
            uploader_id=user.id,
            file_name="evidence.pdf",
            file_size_bytes=len(sample_bytes),
            mime_type="application/pdf",
            storage_backend="local",
            storage_path=str(local_file),
            checksum_sha256=checksum,
            is_confidential=True,
            document_category="EVIDENCE",
        )
        db_session.add(doc)
        await db_session.commit()

        mock_cloud = MockCloudStorageProvider()

        # Run in DRY-RUN mode (execute=False)
        report = await run_migration(
            session=db_session,
            storage_provider=mock_cloud,
            execute=False,
            vault_dir=vault_path,
        )

        assert report.mode == "DRY_RUN"
        assert report.total_scanned == 1
        assert report.migrated_count == 1
        assert report.failed_count == 0
        assert report.missing_local_files == 0
        assert len(mock_cloud.objects) == 0  # No files uploaded

        # Refresh database entity: MUST still be local
        refreshed = (await db_session.execute(select(Document).where(Document.id == doc_id))).scalar_one()
        assert refreshed.storage_backend == "local"
        assert refreshed.storage_key is None
        # Local file must still exist
        assert local_file.is_file()


@pytest.mark.asyncio
async def test_migration_execute_success_and_preserves_local_files(db_session: AsyncSession):
    """Test live migration uploads to cloud, updates DB metadata, and NEVER deletes local file."""
    user, case = await setup_migration_test_case(db_session)

    with tempfile.TemporaryDirectory() as temp_vault:
        vault_path = Path(temp_vault)
        case_vault = vault_path / str(case.id)
        case_vault.mkdir(parents=True, exist_ok=True)

        doc_id = uuid.uuid4()
        sample_bytes = b"%PDF-1.4 verified petition filing content"
        local_file = case_vault / f"{doc_id}_petition.pdf"
        local_file.write_bytes(sample_bytes)
        checksum = hashlib.sha256(sample_bytes).hexdigest()

        doc = Document(
            id=doc_id,
            case_id=case.id,
            uploader_id=user.id,
            file_name="petition.pdf",
            file_size_bytes=len(sample_bytes),
            mime_type="application/pdf",
            storage_backend="local",
            storage_path=str(local_file),
            checksum_sha256=checksum,
        )
        db_session.add(doc)
        await db_session.commit()

        mock_cloud = MockCloudStorageProvider()

        # Run in LIVE EXECUTION mode
        report = await run_migration(
            session=db_session,
            storage_provider=mock_cloud,
            execute=True,
            vault_dir=vault_path,
        )

        assert report.mode == "EXECUTE"
        assert report.total_scanned == 1
        assert report.migrated_count == 1
        assert report.failed_count == 0

        # Verify object exists in mock cloud storage
        refreshed = (await db_session.execute(select(Document).where(Document.id == doc_id))).scalar_one()
        assert refreshed.storage_backend == "r2"
        assert refreshed.storage_key is not None
        assert refreshed.storage_key in mock_cloud.objects
        assert mock_cloud.objects[refreshed.storage_key] == sample_bytes

        # CRITICAL SAFETY CHECK: Original local file MUST still exist on disk!
        assert local_file.is_file()
        assert local_file.read_bytes() == sample_bytes


@pytest.mark.asyncio
async def test_migration_resumable_skips_already_migrated_documents(db_session: AsyncSession):
    """Test that already migrated documents verified in R2 are automatically skipped."""
    user, case = await setup_migration_test_case(db_session)

    mock_cloud = MockCloudStorageProvider()
    doc_id = uuid.uuid4()
    existing_key = f"vault/cases/{case.id}/{doc_id}_already_migrated.pdf"
    mock_cloud.objects[existing_key] = b"Pre-existing R2 bytes"

    doc = Document(
        id=doc_id,
        case_id=case.id,
        uploader_id=user.id,
        file_name="already_migrated.pdf",
        file_size_bytes=len(mock_cloud.objects[existing_key]),
        mime_type="application/pdf",
        storage_backend="r2",
        storage_key=existing_key,
        storage_path=f"r2://nyayasetu-vault/{existing_key}",
        checksum_sha256="dummy-hash",
    )
    db_session.add(doc)
    await db_session.commit()

    report = await run_migration(
        session=db_session,
        storage_provider=mock_cloud,
        execute=True,
    )

    assert report.total_scanned == 1
    assert report.already_migrated_skipped == 1
    assert report.migrated_count == 0
    assert len(mock_cloud.uploaded_keys) == 0  # No re-upload performed


@pytest.mark.asyncio
async def test_migration_reports_missing_local_file_safely(db_session: AsyncSession):
    """Test that a missing local file is recorded as MISSING without failing whole run."""
    user, case = await setup_migration_test_case(db_session)

    doc = Document(
        id=uuid.uuid4(),
        case_id=case.id,
        uploader_id=user.id,
        file_name="vanished_file.pdf",
        file_size_bytes=1024,
        mime_type="application/pdf",
        storage_backend="local",
        storage_path="/nonexistent/path/to/vanished_file.pdf",
        checksum_sha256="abc12345",
    )
    db_session.add(doc)
    await db_session.commit()

    with tempfile.TemporaryDirectory() as empty_vault:
        mock_cloud = MockCloudStorageProvider()
        report = await run_migration(
            session=db_session,
            storage_provider=mock_cloud,
            execute=True,
            vault_dir=Path(empty_vault),
        )

        assert report.total_scanned == 1
        assert report.missing_local_files == 1
        assert report.migrated_count == 0
        assert report.failed_count == 0


@pytest.mark.asyncio
async def test_migration_detects_checksum_mismatch(db_session: AsyncSession):
    """Test that local file with mismatched SHA-256 hash is rejected and flagged."""
    user, case = await setup_migration_test_case(db_session)

    with tempfile.TemporaryDirectory() as temp_vault:
        vault_path = Path(temp_vault)
        case_vault = vault_path / str(case.id)
        case_vault.mkdir(parents=True, exist_ok=True)

        doc_id = uuid.uuid4()
        actual_bytes = b"Actual altered content on disk"
        local_file = case_vault / f"{doc_id}_corrupt.pdf"
        local_file.write_bytes(actual_bytes)

        # Record a DIFFERENT hash in the database
        mismatched_hash = "0000000000000000000000000000000000000000000000000000000000000000"

        doc = Document(
            id=doc_id,
            case_id=case.id,
            uploader_id=user.id,
            file_name="corrupt.pdf",
            file_size_bytes=len(actual_bytes),
            mime_type="application/pdf",
            storage_backend="local",
            storage_path=str(local_file),
            checksum_sha256=mismatched_hash,
        )
        db_session.add(doc)
        await db_session.commit()

        mock_cloud = MockCloudStorageProvider()
        report = await run_migration(
            session=db_session,
            storage_provider=mock_cloud,
            execute=True,
            vault_dir=vault_path,
        )

        assert report.checksum_mismatches == 1
        assert report.migrated_count == 0
        assert len(mock_cloud.objects) == 0


@pytest.mark.asyncio
async def test_migration_halts_before_exceeding_capacity_limit(db_session: AsyncSession):
    """Test that migration halts when projected R2 usage exceeds application capacity limit."""
    user, case = await setup_migration_test_case(db_session)

    with tempfile.TemporaryDirectory() as temp_vault:
        vault_path = Path(temp_vault)
        case_vault = vault_path / str(case.id)
        case_vault.mkdir(parents=True, exist_ok=True)

        doc_id = uuid.uuid4()
        file_bytes = b"Large document content"
        local_file = case_vault / f"{doc_id}_large.pdf"
        local_file.write_bytes(file_bytes)
        checksum = hashlib.sha256(file_bytes).hexdigest()

        doc = Document(
            id=doc_id,
            case_id=case.id,
            uploader_id=user.id,
            file_name="large.pdf",
            file_size_bytes=len(file_bytes),
            mime_type="application/pdf",
            storage_backend="local",
            storage_path=str(local_file),
            checksum_sha256=checksum,
        )
        db_session.add(doc)
        await db_session.commit()

        mock_cloud = MockCloudStorageProvider()

        # Run with an artificially tiny capacity ceiling (e.g. 5 bytes)
        report_exceeded = await run_migration(
            session=db_session,
            storage_provider=mock_cloud,
            execute=True,
            vault_dir=vault_path,
            capacity_limit_bytes=5,
        )

        assert report_exceeded.limit_exceeded_count == 1
        assert report_exceeded.migrated_count == 0
        assert len(mock_cloud.objects) == 0


@pytest.mark.asyncio
async def test_migration_rollback_mode(db_session: AsyncSession):
    """Test that --rollback reverts all documents marked 'r2' back to 'local'."""
    user, case = await setup_migration_test_case(db_session)

    doc1 = Document(
        id=uuid.uuid4(),
        case_id=case.id,
        uploader_id=user.id,
        file_name="doc1.pdf",
        file_size_bytes=100,
        mime_type="application/pdf",
        storage_backend="r2",
        storage_key="vault/cases/doc1.pdf",
        storage_path="r2://nyayasetu-vault/vault/cases/doc1.pdf",
        checksum_sha256="dummy1",
    )
    doc2 = Document(
        id=uuid.uuid4(),
        case_id=case.id,
        uploader_id=user.id,
        file_name="doc2.pdf",
        file_size_bytes=200,
        mime_type="application/pdf",
        storage_backend="r2",
        storage_key="vault/cases/doc2.pdf",
        storage_path="r2://nyayasetu-vault/vault/cases/doc2.pdf",
        checksum_sha256="dummy2",
    )
    db_session.add_all([doc1, doc2])
    await db_session.commit()

    report = await run_migration(
        session=db_session,
        rollback=True,
    )

    assert report.mode == "ROLLBACK"
    assert report.migrated_count == 2

    # Check database entities: both must now be 'local'
    docs = (await db_session.execute(select(Document).where(Document.case_id == case.id))).scalars().all()
    for d in docs:
        assert d.storage_backend == "local"


@pytest.mark.asyncio
async def test_migration_verify_only_mode(db_session: AsyncSession):
    """Test that --verify-only accurately checks presence in cloud storage."""
    user, case = await setup_migration_test_case(db_session)

    mock_cloud = MockCloudStorageProvider()
    valid_key = f"vault/cases/{case.id}/valid.pdf"
    mock_cloud.objects[valid_key] = b"valid file in r2"

    # doc1: exists in R2
    doc1 = Document(
        id=uuid.uuid4(),
        case_id=case.id,
        uploader_id=user.id,
        file_name="valid.pdf",
        file_size_bytes=len(mock_cloud.objects[valid_key]),
        mime_type="application/pdf",
        storage_backend="r2",
        storage_key=valid_key,
        storage_path=f"r2://nyayasetu-vault/{valid_key}",
        checksum_sha256="valid_hash",
    )
    # doc2: missing from R2
    doc2 = Document(
        id=uuid.uuid4(),
        case_id=case.id,
        uploader_id=user.id,
        file_name="missing_in_r2.pdf",
        file_size_bytes=500,
        mime_type="application/pdf",
        storage_backend="r2",
        storage_key="vault/cases/nonexistent_key.pdf",
        storage_path="r2://nyayasetu-vault/vault/cases/nonexistent_key.pdf",
        checksum_sha256="missing_hash",
    )
    db_session.add_all([doc1, doc2])
    await db_session.commit()

    report = await run_migration(
        session=db_session,
        storage_provider=mock_cloud,
        verify_only=True,
    )

    assert report.mode == "VERIFY_ONLY"
    assert report.total_scanned == 2
    assert report.migrated_count == 1  # 1 verified
    assert report.failed_count == 1    # 1 missing in R2
