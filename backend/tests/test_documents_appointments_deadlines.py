"""Comprehensive test suite for Document Management, Appointments, and Deadlines modules."""

from datetime import datetime, timedelta, timezone
import io
import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.modules.admin.models import AuditLog
from app.modules.advocates.models import AdvocateProfile
from app.modules.users.models import User, UserRole


# ──────────────────────────────────────────────────────────────
# Helper Functions
# ──────────────────────────────────────────────────────────────

async def create_citizen(
    async_client: AsyncClient,
    email: str = "citizen.doc@example.com",
    name: str = "Sunita Rao",
    phone: str = "+919876540001",
) -> tuple[str, str]:
    """Helper to register and log in a citizen, returning (user_id, token)."""
    reg_payload = {
        "account_type": "CITIZEN",
        "full_name": name,
        "email": email,
        "phone": phone,
        "password": "CitizenPassword2026",
        "preferred_language": "en",
    }
    reg_res = await async_client.post("/api/v1/auth/register", json=reg_payload)
    assert reg_res.status_code == 201

    login_res = await async_client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "CitizenPassword2026"},
    )
    assert login_res.status_code == 200
    return reg_res.json()["id"], login_res.json()["access_token"]


async def create_advocate_user(
    db: AsyncSession,
    async_client: AsyncClient,
    email: str = "advocate.doc@example.com",
    name: str = "Adv. Rajesh Sharma",
    phone: str = "+919876540002",
    bar_id: str = "D/4501/2014",
    verification_status: str = "VERIFIED",
) -> tuple[str, str, str]:
    """Helper to create and log in a verified advocate, returning (user_id, adv_profile_id, token)."""
    user = User(
        full_name=name,
        email=email,
        phone=phone,
        password_hash=hash_password("AdvocatePassword2026"),
        role=UserRole.ADVOCATE,
        is_active=True,
    )
    db.add(user)
    await db.flush()

    adv_profile = AdvocateProfile(
        user_id=user.id,
        bar_council_id=bar_id,
        bar_council_name="Bar Council of Delhi",
        primary_practice="Trials & Disputes",
        secondary_practices=["Cheque Bounce", "Civil Litigation"],
        courts_of_practice=["Delhi High Court", "Saket District Court"],
        languages=["en", "hi"],
        in_practice_years=12,
        city="New Delhi",
        district="South Delhi",
        state="Delhi",
        fixed_consultation_fee_inr=2000.0,
        hourly_rate_inr=4000.0,
        platform_verification_status=verification_status,
    )
    db.add(adv_profile)
    await db.commit()
    await db.refresh(user)
    await db.refresh(adv_profile)

    login_res = await async_client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "AdvocatePassword2026"},
    )
    assert login_res.status_code == 200
    return str(user.id), str(adv_profile.id), login_res.json()["access_token"]


async def create_admin_user(
    db: AsyncSession,
    async_client: AsyncClient,
    email: str = "admin.vault@example.com",
) -> tuple[str, str]:
    """Helper to create and log in an admin user."""
    user = User(
        full_name="Admin Supervisor",
        email=email,
        phone="+919876549999",
        password_hash=hash_password("AdminSecure2026"),
        role=UserRole.ADMIN,
        is_active=True,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    login_res = await async_client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "AdminSecure2026"},
    )
    assert login_res.status_code == 200
    return str(user.id), login_res.json()["access_token"]


async def create_test_case(
    async_client: AsyncClient,
    token: str,
    title: str = "Cheque Dishonour Case under Section 138",
) -> dict:
    """Helper for a citizen to submit a case intake."""
    headers = {"Authorization": f"Bearer {token}"}
    case_payload = {
        "title": title,
        "problem_description": "Cheque of Rs 5,00,000 was bounced by payer citing insufficient funds. Notice sent 10 days ago.",
        "legal_issue_category": "Cheque Bounce",
        "state": "Delhi",
        "district": "South Delhi",
        "relevant_court": "Saket District Court",
        "incident_date": "2026-03-01",
        "preferred_language": "en",
        "urgency": "HIGH",
    }
    res = await async_client.post("/api/v1/cases", json=case_payload, headers=headers)
    assert res.status_code == 201
    return res.json()


# ──────────────────────────────────────────────────────────────
# Module A: Document Management Tests
# ──────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_case_document_upload_and_sha256_integrity(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Verify citizen uploads a PDF document to their case with SHA-256 calculation and private storage."""
    citizen_id, token = await create_citizen(async_client, email="doc.citizen1@example.com")
    case = await create_test_case(async_client, token)
    case_id = case["id"]

    pdf_content = b"%PDF-1.4 test case evidence document for legal proceedings\n%%EOF"
    files = {"file": ("cheque_return_memo.pdf", io.BytesIO(pdf_content), "application/pdf")}
    data = {"document_category": "EVIDENCE", "is_confidential": "true"}

    upload_res = await async_client.post(
        f"/api/v1/documents/cases/{case_id}/upload",
        headers={"Authorization": f"Bearer {token}"},
        files=files,
        data=data,
    )
    assert upload_res.status_code == 201
    doc_data = upload_res.json()

    assert doc_data["file_name"] == "cheque_return_memo.pdf"
    assert doc_data["mime_type"] == "application/pdf"
    assert doc_data["file_size_bytes"] == len(pdf_content)
    assert doc_data["is_confidential"] is True
    assert doc_data["checksum_sha256"] is not None
    assert len(doc_data["checksum_sha256"]) == 64  # Valid 64-char hex SHA-256

    # Verify audit log was recorded
    audit_res = await db_session.execute(
        select(AuditLog).where(AuditLog.action == "DOCUMENT_UPLOADED")
    )
    assert audit_res.scalar_one_or_none() is not None


@pytest.mark.asyncio
async def test_document_case_ownership_access_isolation(
    async_client: AsyncClient,
):
    """Verify that Citizen B cannot upload to or view documents of Citizen A's case (403 Forbidden)."""
    # Citizen A creates case and uploads document
    _, token_a = await create_citizen(async_client, email="user.a@example.com", phone="+919876540010")
    case_a = await create_test_case(async_client, token_a)
    case_a_id = case_a["id"]

    pdf_content = b"%PDF-1.4 confidential evidence\n%%EOF"
    upload_res = await async_client.post(
        f"/api/v1/documents/cases/{case_a_id}/upload",
        headers={"Authorization": f"Bearer {token_a}"},
        files={"file": ("case_a_doc.pdf", io.BytesIO(pdf_content), "application/pdf")},
    )
    assert upload_res.status_code == 201
    doc_id = upload_res.json()["id"]

    # Citizen B tries to upload to Case A
    _, token_b = await create_citizen(async_client, email="user.b@example.com", phone="+919876540020")
    b_upload_res = await async_client.post(
        f"/api/v1/documents/cases/{case_a_id}/upload",
        headers={"Authorization": f"Bearer {token_b}"},
        files={"file": ("intruder.pdf", io.BytesIO(pdf_content), "application/pdf")},
    )
    assert b_upload_res.status_code == 403

    # Citizen B tries to list Case A's documents
    b_list_res = await async_client.get(
        f"/api/v1/documents/cases/{case_a_id}",
        headers={"Authorization": f"Bearer {token_b}"},
    )
    assert b_list_res.status_code == 403

    # Citizen B tries to request download token for Doc A
    b_token_res = await async_client.get(
        f"/api/v1/documents/{doc_id}/access-token",
        headers={"Authorization": f"Bearer {token_b}"},
    )
    assert b_token_res.status_code == 403


@pytest.mark.asyncio
async def test_short_lived_download_token_and_secure_streaming(
    async_client: AsyncClient,
):
    """Verify generation of 15-minute download token and authorized file streaming."""
    _, token = await create_citizen(async_client, email="stream.citizen@example.com", phone="+919876540030")
    case = await create_test_case(async_client, token)
    case_id = case["id"]

    pdf_bytes = b"%PDF-1.4 authenticated streaming content\n%%EOF"
    upload_res = await async_client.post(
        f"/api/v1/documents/cases/{case_id}/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("contract.pdf", io.BytesIO(pdf_bytes), "application/pdf")},
    )
    doc_id = upload_res.json()["id"]

    # 1. Request short-lived download token
    token_res = await async_client.get(
        f"/api/v1/documents/{doc_id}/access-token",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert token_res.status_code == 200
    token_data = token_res.json()
    assert token_data["document_id"] == doc_id
    assert token_data["expires_in_seconds"] == 900
    download_token = token_data["token"]

    # 2. Download file using query parameter token (no Authorization header required)
    download_res = await async_client.get(
        f"/api/v1/documents/{doc_id}/download?token={download_token}"
    )
    assert download_res.status_code == 200
    assert download_res.content == pdf_bytes
    assert "attachment; filename=\"contract.pdf\"" in download_res.headers["content-disposition"]

    # 3. Direct unauthenticated request without token must fail (401)
    unauth_res = await async_client.get(f"/api/v1/documents/{doc_id}/download")
    assert unauth_res.status_code == 401


# ──────────────────────────────────────────────────────────────
# Module B: Appointments & Consultations Tests
# ──────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_appointment_booking_and_conflict_prevention(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Verify citizen books consultation and overlapping duplicate bookings are prevented with HTTP 409."""
    _, adv_id, adv_token = await create_advocate_user(
        db_session, async_client, email="adv.booking@example.com", bar_id="D/8899/2012"
    )
    _, citizen_token = await create_citizen(
        async_client, email="client.booking@example.com", phone="+919876540040"
    )

    start_time = datetime.now(timezone.utc) + timedelta(days=2, hours=10)
    end_time = start_time + timedelta(minutes=45)

    booking_payload = {
        "advocate_id": adv_id,
        "scheduled_start": start_time.isoformat(),
        "scheduled_end": end_time.isoformat(),
        "timezone": "Asia/Kolkata",
        "mode": "VIDEO",
        "client_notes": "Preliminary consultation regarding property title dispute.",
    }

    # 1. Successful booking
    book_res = await async_client.post(
        "/api/v1/appointments",
        headers={"Authorization": f"Bearer {citizen_token}"},
        json=booking_payload,
    )
    assert book_res.status_code == 201
    appt_data = book_res.json()
    assert appt_data["status"] == "REQUESTED"
    assert appt_data["booking_reference"].startswith("NYA-BK-2026-")
    assert appt_data["fee_inr"] == 2000.0

    # 2. Conflicting booking attempt (overlapping slot for same advocate)
    overlap_start = start_time + timedelta(minutes=15)
    overlap_end = overlap_start + timedelta(minutes=30)
    conflict_payload = {
        "advocate_id": adv_id,
        "scheduled_start": overlap_start.isoformat(),
        "scheduled_end": overlap_end.isoformat(),
        "mode": "IN_PERSON",
        "client_notes": "Another client booking the same advocate at overlapping time",
    }
    conflict_res = await async_client.post(
        "/api/v1/appointments",
        headers={"Authorization": f"Bearer {citizen_token}"},
        json=conflict_payload,
    )
    assert conflict_res.status_code == 409
    assert "existing consultation or pending request during this time slot" in conflict_res.json()["error"]["message"]


@pytest.mark.asyncio
async def test_appointment_advocate_accept_reject_lifecycle(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Verify advocate reviews consultation request: accept to CONFIRMED or reject with reason."""
    _, adv_id, adv_token = await create_advocate_user(
        db_session, async_client, email="adv.lifecycle@example.com", bar_id="D/7766/2015"
    )
    _, citizen_token = await create_citizen(
        async_client, email="client.lifecycle@example.com", phone="+919876540050"
    )

    start_time = datetime.now(timezone.utc) + timedelta(days=3, hours=14)
    end_time = start_time + timedelta(minutes=30)

    # Citizen books
    book_res = await async_client.post(
        "/api/v1/appointments",
        headers={"Authorization": f"Bearer {citizen_token}"},
        json={
            "advocate_id": adv_id,
            "scheduled_start": start_time.isoformat(),
            "scheduled_end": end_time.isoformat(),
            "mode": "VIDEO",
        },
    )
    appt_id = book_res.json()["id"]

    # Citizen cannot approve/confirm appointment (403 Forbidden)
    unauth_confirm = await async_client.patch(
        f"/api/v1/appointments/{appt_id}/status",
        headers={"Authorization": f"Bearer {citizen_token}"},
        json={"status": "CONFIRMED"},
    )
    assert unauth_confirm.status_code == 403

    # Advocate confirms appointment
    confirm_res = await async_client.patch(
        f"/api/v1/appointments/{appt_id}/status",
        headers={"Authorization": f"Bearer {adv_token}"},
        json={"status": "CONFIRMED", "meeting_link": "https://meet.nyayasetu.gov.in/chamber-7766"},
    )
    assert confirm_res.status_code == 200
    assert confirm_res.json()["status"] == "CONFIRMED"
    assert "chamber-7766" in confirm_res.json()["meeting_link"]

    # Rejection requires rejection_reason
    book_res2 = await async_client.post(
        "/api/v1/appointments",
        headers={"Authorization": f"Bearer {citizen_token}"},
        json={
            "advocate_id": adv_id,
            "scheduled_start": (start_time + timedelta(days=1)).isoformat(),
            "scheduled_end": (end_time + timedelta(days=1)).isoformat(),
            "mode": "PHONE",
        },
    )
    appt_id2 = book_res2.json()["id"]

    reject_res = await async_client.patch(
        f"/api/v1/appointments/{appt_id2}/status",
        headers={"Authorization": f"Bearer {adv_token}"},
        json={"status": "REJECTED", "rejection_reason": "Pre-scheduled High Court bench appearance."},
    )
    assert reject_res.status_code == 200
    assert reject_res.json()["status"] == "REJECTED"
    assert "High Court bench" in reject_res.json()["rejection_reason"]


@pytest.mark.asyncio
async def test_admin_can_inspect_all_appointments(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Verify administrator has comprehensive oversight across all citizen and advocate appointments."""
    _, adv_id, _ = await create_advocate_user(
        db_session, async_client, email="adv.admininspect@example.com", bar_id="D/1122/2018"
    )
    _, citizen_token = await create_citizen(
        async_client, email="client.admininspect@example.com", phone="+919876540060"
    )
    _, admin_token = await create_admin_user(db_session, async_client, email="admin.inspect@example.com")

    start_time = datetime.now(timezone.utc) + timedelta(days=4)
    end_time = start_time + timedelta(minutes=30)

    await async_client.post(
        "/api/v1/appointments",
        headers={"Authorization": f"Bearer {citizen_token}"},
        json={
            "advocate_id": adv_id,
            "scheduled_start": start_time.isoformat(),
            "scheduled_end": end_time.isoformat(),
            "mode": "VIDEO",
        },
    )

    admin_res = await async_client.get(
        "/api/v1/appointments",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert admin_res.status_code == 200
    assert admin_res.json()["total"] >= 1


# ──────────────────────────────────────────────────────────────
# Module C: Deadline Management Tests
# ──────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_statutory_deadline_creation_manual_and_reminder_schedule(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Verify citizen registers statutory limitation deadline without automated unverified LLM calculation."""
    _, citizen_token = await create_citizen(
        async_client, email="deadline.client@example.com", phone="+919876540070"
    )
    case = await create_test_case(async_client, citizen_token, title="Dishonoured Cheque Statutory Notice")
    case_id = case["id"]

    limitation_due = datetime.now(timezone.utc) + timedelta(days=15)

    deadline_payload = {
        "case_id": case_id,
        "title": "Section 138 15-Day Statutory Demand Notice Expiry",
        "description": "Period for drawer to make payment following legal notice service.",
        "deadline_type": "STATUTORY_LIMITATION",
        "source_basis": "Section 138(c) Negotiable Instruments Act 1881",
        "statutory_provision": "Section 138(c) NI Act",
        "due_date": limitation_due.isoformat(),
        "priority": "CRITICAL",
        "reminder_days_before": [7, 3, 1],
    }

    create_res = await async_client.post(
        "/api/v1/deadlines",
        headers={"Authorization": f"Bearer {citizen_token}"},
        json=deadline_payload,
    )
    assert create_res.status_code == 201
    d_data = create_res.json()

    assert d_data["title"] == "Section 138 15-Day Statutory Demand Notice Expiry"
    assert d_data["deadline_type"] == "STATUTORY_LIMITATION"
    assert d_data["source_basis"] == "Section 138(c) Negotiable Instruments Act 1881"
    assert d_data["is_advocate_confirmed"] is False  # Must NOT be automatically confirmed
    assert d_data["is_completed"] is False
    assert d_data["reminders_json"] is not None
    assert len(d_data["reminders_json"]["scheduled_alerts"]) == 3


@pytest.mark.asyncio
async def test_advocate_statutory_limitation_review_and_confirmation(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Verify advocate reviews and validates limitation basis, while citizen is forbidden from confirming."""
    _, adv_profile_id, adv_token = await create_advocate_user(
        db_session, async_client, email="adv.limitation@example.com", bar_id="D/9922/2011"
    )
    _, citizen_token = await create_citizen(
        async_client, email="client.limitation@example.com", phone="+919876540080"
    )
    case = await create_test_case(async_client, citizen_token)
    case_id = case["id"]

    due_date = datetime.now(timezone.utc) + timedelta(days=30)
    create_res = await async_client.post(
        "/api/v1/deadlines",
        headers={"Authorization": f"Bearer {citizen_token}"},
        json={
            "case_id": case_id,
            "title": "Written Statement 30-Day Filing Period",
            "deadline_type": "STATUTORY_LIMITATION",
            "source_basis": "Order VIII Rule 1 CPC",
            "due_date": due_date.isoformat(),
            "priority": "HIGH",
        },
    )
    deadline_id = create_res.json()["id"]

    # 1. Citizen cannot confirm their own statutory deadline (403 Forbidden)
    unauth_res = await async_client.patch(
        f"/api/v1/deadlines/{deadline_id}/confirm",
        headers={"Authorization": f"Bearer {citizen_token}"},
        json={"verified_statutory_basis": "Order VIII Rule 1 CPC Verified"},
    )
    assert unauth_res.status_code == 403
    assert "Only verified legal advocates or administrators" in unauth_res.json()["error"]["message"]

    # 2. Verified advocate confirms and validates statutory basis
    confirm_res = await async_client.patch(
        f"/api/v1/deadlines/{deadline_id}/confirm",
        headers={"Authorization": f"Bearer {adv_token}"},
        json={
            "verified_statutory_basis": "Order VIII Rule 1 CPC (extendable up to 90/120 days on court discretion)",
            "confirmation_notes": "Summons served on 1st March. 30 days limitation verified against court registry.",
        },
    )
    assert confirm_res.status_code == 200
    confirmed_data = confirm_res.json()
    assert confirmed_data["is_advocate_confirmed"] is True
    assert confirmed_data["confirmed_by_advocate_id"] == adv_profile_id
    assert confirmed_data["confirmed_at"] is not None
    assert "Order VIII Rule 1 CPC" in confirmed_data["statutory_provision"]


@pytest.mark.asyncio
async def test_deadline_mark_completed_and_audit_trail(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Verify case owner can mark statutory reminder as completed and audit trail is recorded."""
    _, citizen_token = await create_citizen(
        async_client, email="client.complete@example.com", phone="+919876540090"
    )
    case = await create_test_case(async_client, citizen_token)
    case_id = case["id"]

    due_date = datetime.now(timezone.utc) + timedelta(days=7)
    create_res = await async_client.post(
        "/api/v1/deadlines",
        headers={"Authorization": f"Bearer {citizen_token}"},
        json={
            "case_id": case_id,
            "title": "Serve Demand Notice by Registered AD Post",
            "deadline_type": "NOTICE_EXPIRY",
            "due_date": due_date.isoformat(),
            "priority": "MEDIUM",
        },
    )
    deadline_id = create_res.json()["id"]

    # Complete deadline
    complete_res = await async_client.patch(
        f"/api/v1/deadlines/{deadline_id}/complete",
        headers={"Authorization": f"Bearer {citizen_token}"},
    )
    assert complete_res.status_code == 200
    assert complete_res.json()["is_completed"] is True
    assert complete_res.json()["completed_at"] is not None

    # Check audit log
    audit_res = await db_session.execute(
        select(AuditLog).where(
            AuditLog.action == "DEADLINE_COMPLETED",
            AuditLog.entity_id == deadline_id,
        )
    )
    assert audit_res.scalar_one_or_none() is not None
