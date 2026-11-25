"""Admin API coverage for the official-source registry operations."""

from types import SimpleNamespace
from uuid import uuid4

import pytest

from app.core.security import hash_password
from app.modules.users.models import User

BASE = "/api/v1/legal-knowledge"


async def _login(async_client, email: str) -> str:
    res = await async_client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "SecurePassword2026"},
    )
    assert res.status_code == 200
    return res.json()["access_token"]


@pytest.mark.asyncio
async def test_registry_admin_api_is_role_protected_and_delegates_operations(
    async_client, db_session, monkeypatch, tmp_path
):
    def make_user(email: str, phone: str, role: str) -> User:
        user = User(
            full_name="Registry Tester",
            email=email,
            phone=phone,
            password_hash=hash_password("SecurePassword2026"),
            role=role,
            is_verified=True,
            is_active=True,
        )
        db_session.add(user)
        return user

    admin = make_user("registry.admin@example.com", "+919876543100", "ADMIN")
    citizen = make_user("registry.citizen@example.com", "+919876543101", "CITIZEN")
    await db_session.commit()
    assert admin and citizen

    admin_headers = {"Authorization": f"Bearer {await _login(async_client, 'registry.admin@example.com')}"}
    citizen_headers = {"Authorization": f"Bearer {await _login(async_client, 'registry.citizen@example.com')}"}

    csv_path = tmp_path / "source_registry.csv"
    csv_path.write_text(
        "source_id,title,official_url,exact_document_url,source_type,jurisdiction,format,tier,language\n"
        "SRC_API_TEST,API Test Act,https://www.indiacode.nic.in/handle/api,https://www.indiacode.nic.in/handle/api,CENTRAL_ACT,Union of India,HTML,Tier 1,English\n",
        encoding="utf-8",
    )

    citizen_bootstrap = await async_client.post(
        f"{BASE}/admin/registry/bootstrap",
        json={"csv_path": str(csv_path)},
        headers=citizen_headers,
    )
    assert citizen_bootstrap.status_code == 403

    bootstrap = await async_client.post(
        f"{BASE}/admin/registry/bootstrap",
        json={"csv_path": str(csv_path)},
        headers=admin_headers,
    )
    assert bootstrap.status_code == 200
    assert bootstrap.json() == {"loaded": 1, "all_new_rows_unverified": True}

    listed = await async_client.get(f"{BASE}/admin/registry/sources", headers=admin_headers)
    assert listed.status_code == 200
    row = next(item for item in listed.json() if item["registry_key"] == "SRC_API_TEST")
    assert row["verification_status"] == "PENDING"
    assert row["enabled"] is False

    async def fake_verify(db, *, fetcher, source_keys, force):
        return [{"registry_key": "SRC_API_TEST", "verified": True, "force": force}]

    monkeypatch.setattr("app.modules.legal_knowledge.router.verify_sources", fake_verify)
    verified = await async_client.post(
        f"{BASE}/admin/registry/verify",
        json={"verify_all": True, "force": True},
        headers=admin_headers,
    )
    assert verified.status_code == 200
    assert verified.json()[0]["force"] is True

    job_id = uuid4()
    fake_job = SimpleNamespace(
        id=job_id,
        source_key="SRC_API_TEST",
        status="COMPLETED",
        documents_discovered=1,
        documents_ingested=1,
        documents_failed=0,
        checkpoint_json={"https://www.indiacode.nic.in/handle/api": {"status": "QUEUED_FOR_REVIEW"}},
    )

    async def fake_sync(db, *, source_key, fetcher, mode, force, enable_verified, requested_by):
        return fake_job

    monkeypatch.setattr("app.modules.legal_knowledge.router.sync_source", fake_sync)
    synced = await async_client.post(
        f"{BASE}/admin/registry/sync",
        json={"source_key": "SRC_API_TEST", "force": True},
        headers=admin_headers,
    )
    assert synced.status_code == 200
    assert synced.json()["job_id"] == str(job_id)
    assert synced.json()["documents_queued"] == 1

    jobs = await async_client.get(f"{BASE}/admin/registry/jobs", headers=admin_headers)
    assert jobs.status_code == 200
    assert jobs.json() == []

    versions = await async_client.get(f"{BASE}/admin/registry/versions", headers=admin_headers)
    assert versions.status_code == 200
    assert versions.json() == []

    review = await async_client.get(f"{BASE}/admin/registry/review", headers=admin_headers)
    assert review.status_code == 200
    assert review.json() == []

    version_id = uuid4()

    async def fake_ingest(db, *, version_id, actor):
        return {
            "document_version_id": str(version_id),
            "legal_source_id": str(uuid4()),
            "ingestion_job_id": str(uuid4()),
            "chunks_extracted": 2,
            "status": "INDEXED",
        }

    monkeypatch.setattr("app.modules.legal_knowledge.router.ingest_document_version", fake_ingest)
    promoted = await async_client.post(
        f"{BASE}/admin/registry/versions/ingest",
        json={"version_id": str(version_id), "reviewer_note": "approved"},
        headers=admin_headers,
    )
    assert promoted.status_code == 200
    assert promoted.json()["status"] == "INDEXED"
