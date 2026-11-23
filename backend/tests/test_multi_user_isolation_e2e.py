"""Cross-account isolation for profiles, document analysis, reviews, exports and deletion."""

import uuid
from datetime import datetime, timedelta, timezone
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.modules.advocates.models import AdvocateProfile
from app.modules.appointments.models import Appointment
from app.modules.cases.models import LegalCase
from app.modules.users.models import User


def create_selectable_pdf(text_lines: list[str]) -> bytes:
    """Create a valid PDF byte string with real selectable text stream."""
    stream_content = "BT\n/F1 12 Tf\n50 700 Td\n"
    for i, line in enumerate(text_lines):
        safe_line = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        if i == 0:
            stream_content += f"({safe_line}) Tj\n"
        else:
            stream_content += f"0 -20 Td\n({safe_line}) Tj\n"
    stream_content += "ET"
    stream_bytes = stream_content.encode("latin-1")
    length = len(stream_bytes)
    return (
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n"
        b"4 0 obj\n<< /Length " + str(length).encode("ascii") + b" >>\nstream\n"
        + stream_bytes
        + b"\nendstream\nendobj\n"
        b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
        b"xref\n0 6\n0000000000 65535 f \n"
        b"0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n"
        b"0000000244 00000 n \n0000000350 00000 n \n"
        b"trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n435\n%%EOF\n"
    )


async def create_user_session(
    async_client: AsyncClient,
    db: AsyncSession,
    role: str = "CITIZEN",
    full_name: str = "Test User",
    email_prefix: str = "user",
    city: str = "Mumbai",
) -> dict:
    """Helper creating user record and obtaining real JWT token."""
    unique_suffix = uuid.uuid4().hex[:8]
    email = f"{email_prefix}_{unique_suffix}@example.com"
    phone = f"+9198{uuid.uuid4().hex[:8]}"
    password = "TestPassword2026!"

    user = User(
        email=email,
        phone=phone,
        password_hash=hash_password(password),
        full_name=full_name,
        role=role,
        is_verified=True,
        is_active=True,
        preferred_language="en",
        city=city,
        state="Maharashtra",
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    advocate_profile = None
    if role == "ADVOCATE":
        advocate_profile = AdvocateProfile(
            user_id=user.id,
            bar_council_id=f"MAH/{uuid.uuid4().hex[:6].upper()}/2018",
            bar_council_name="Bar Council of Maharashtra & Goa",
            in_practice_years=12,
            primary_practice="Trials & Disputes",
            secondary_practices=["Commercial Arbitration"],
            courts_of_practice=["Bombay High Court", "City Civil Court, Mumbai"],
            languages=["English", "Marathi", "Hindi"],
            city="Mumbai",
            district="Mumbai",
            state="Maharashtra",
            platform_verification_status="VERIFIED",
            fixed_consultation_fee_inr=3500.0,
            hourly_rate_inr=5000.0,
        )
        db.add(advocate_profile)
        await db.commit()
        await db.refresh(advocate_profile)

    login_res = await async_client.post(
        "/api/v1/auth/login",
        json={"email": user.email, "password": password},
    )
    assert login_res.status_code == 200, f"Login failed: {login_res.text}"
    token = login_res.json()["access_token"]

    return {
        "user": user,
        "advocate_profile": advocate_profile,
        "token": token,
        "headers": {"Authorization": f"Bearer {token}"},
    }


@pytest.mark.asyncio
async def test_multi_user_profile_isolation(async_client: AsyncClient, db_session: AsyncSession):
    """Verify Profile updates for User A do not affect User B, and users cannot modify privileged fields."""
    user_a = await create_user_session(async_client, db_session, email_prefix="citizena", full_name="Aarav Deshmukh", city="Pune")
    user_b = await create_user_session(async_client, db_session, email_prefix="citizenb", full_name="Bhavna Mehta", city="Nagpur")

    # User A attempts to pass unauthorized field (role) -> strictly rejected by Pydantic extra="forbid"
    illegal_put = await async_client.put(
        "/api/v1/users/me",
        headers=user_a["headers"],
        json={"full_name": "Aarav S. Deshmukh", "city": "Pune Cantt", "role": "ADMIN"},
    )
    assert illegal_put.status_code == 422

    # User A updates profile with allowed fields
    put_a = await async_client.put(
        "/api/v1/users/me",
        headers=user_a["headers"],
        json={"full_name": "Aarav S. Deshmukh", "city": "Pune Cantt"},
    )
    assert put_a.status_code == 200
    data_a = put_a.json()
    assert data_a["full_name"] == "Aarav S. Deshmukh"
    assert data_a["city"] == "Pune Cantt"
    assert data_a["role"] == "CITIZEN"

    # User B fetches profile -> B retains own info without cross-contamination
    get_b = await async_client.get("/api/v1/users/me", headers=user_b["headers"])
    assert get_b.status_code == 200
    data_b = get_b.json()
    assert data_b["full_name"] == "Bhavna Mehta"
    assert data_b["city"] == "Nagpur"
    assert data_b["id"] != data_a["id"]


@pytest.mark.asyncio
async def test_multi_user_document_vault_and_explanation_isolation(async_client: AsyncClient, db_session: AsyncSession):
    """Verify document upload, OCR, and explanation isolate access between users."""
    user_a = await create_user_session(async_client, db_session, email_prefix="citizena")
    user_b = await create_user_session(async_client, db_session, email_prefix="citizenb")

    # Case for User B
    case_b = LegalCase(
        case_reference=f"NYA-DOC-{uuid.uuid4().hex[:6].upper()}",
        client_id=user_b["user"].id,
        title="Document Vault Test Case",
        practice_group="Trials & Disputes",
        matter_type="Civil Suit",
        summary="Document isolation testing",
    )
    db_session.add(case_b)
    await db_session.commit()
    await db_session.refresh(case_b)

    # User B uploads a document
    file_content = create_selectable_pdf([
        "LEGAL NOTICE: Demand under Section 138 of Negotiable Instruments Act, 1881.",
        "Statutory demand for cheque bounce recovery.",
    ])
    files = {"file": ("notice_sec138.pdf", file_content, "application/pdf")}
    data = {"document_category": "EVIDENCE", "is_confidential": "true"}

    upload_res = await async_client.post(
        f"/api/v1/documents/cases/{case_b.id}/upload",
        headers=user_b["headers"],
        files=files,
        data=data,
    )
    assert upload_res.status_code == 201
    doc_id = upload_res.json()["id"]

    # User A attempts to access User B's document download token -> 403 or 404
    unauth_token = await async_client.get(
        f"/api/v1/documents/{doc_id}/access-token",
        headers=user_a["headers"],
    )
    assert unauth_token.status_code in [403, 404]

    # User A attempts to run OCR on User B's document -> 403 Forbidden
    unauth_ocr = await async_client.post(
        f"/api/v1/documents/{doc_id}/ocr",
        headers=user_a["headers"],
    )
    assert unauth_ocr.status_code == 403

    # User B runs OCR on their own document -> 200
    valid_ocr = await async_client.post(
        f"/api/v1/documents/{doc_id}/ocr",
        headers=user_b["headers"],
    )
    assert valid_ocr.status_code == 200
    assert "Section 138" in valid_ocr.json()["text"]

    # User B runs explanation -> 200
    valid_explain = await async_client.post(
        f"/api/v1/documents/{doc_id}/explain",
        headers=user_b["headers"],
    )
    assert valid_explain.status_code == 200
    assert valid_explain.json()["document_id"] == doc_id


@pytest.mark.asyncio
async def test_multi_user_advocate_review_isolation_and_flow(async_client: AsyncClient, db_session: AsyncSession):
    """Verify Advocate review requires a COMPLETED booking, enforces single-review, and prevents other users from rating."""
    user_a = await create_user_session(async_client, db_session, email_prefix="citizena")
    user_b = await create_user_session(async_client, db_session, email_prefix="citizenb")
    advocate_c = await create_user_session(async_client, db_session, role="ADVOCATE", email_prefix="advocatec")

    # Appointment between User B and Advocate C
    now = datetime.now(timezone.utc)
    appointment = Appointment(
        booking_reference=f"NYA-BK-{uuid.uuid4().hex[:6].upper()}",
        client_id=user_b["user"].id,
        advocate_id=advocate_c["advocate_profile"].id,
        scheduled_start=now - timedelta(days=2),
        scheduled_end=now - timedelta(days=2, hours=-1),
        timezone="Asia/Kolkata",
        status="REQUESTED",
        mode="VIDEO_CONFERENCE",
        fee_inr=3500.0,
        payment_status="PAID",
        client_notes="Initial tenancy consultation session.",
    )
    db_session.add(appointment)
    await db_session.commit()
    await db_session.refresh(appointment)

    # User B attempts to review non-completed consultation -> 400 Bad Request
    pending_review = await async_client.post(
        "/api/v1/reviews",
        headers=user_b["headers"],
        json={"booking_id": str(appointment.id), "rating": 5, "comment": "Excellent counsel"},
    )
    assert pending_review.status_code == 400
    err_msg = pending_review.json()["error"]["message"].lower()
    assert "concluded" in err_msg or "completed" in err_msg

    # Mark appointment COMPLETED
    appointment.status = "COMPLETED"
    await db_session.commit()

    # User A attempts to submit a review for User B's appointment -> 403 Forbidden!
    unauth_review = await async_client.post(
        "/api/v1/reviews",
        headers=user_a["headers"],
        json={"booking_id": str(appointment.id), "rating": 1, "comment": "Malicious competitor rating"},
    )
    assert unauth_review.status_code == 403

    # User B submits valid 5-star review
    valid_review = await async_client.post(
        "/api/v1/reviews",
        headers=user_b["headers"],
        json={
            "booking_id": str(appointment.id),
            "rating": 5,
            "comment": "Exceptional clarity on commercial tenancy dispute.",
            "tags": ["Professional", "Thorough", "Responsive"],
            "matter_resolution": "yes",
        },
    )
    assert valid_review.status_code == 201
    assert valid_review.json()["rating"] == 5

    # User B attempts to submit a second review for the same booking -> 409 Conflict
    dup_review = await async_client.post(
        "/api/v1/reviews",
        headers=user_b["headers"],
        json={"booking_id": str(appointment.id), "rating": 4},
    )
    assert dup_review.status_code == 409

    # Public reviews listing for Advocate C displays the review and dynamic aggregate
    adv_reviews = await async_client.get(
        f"/api/v1/reviews/advocates/{advocate_c['advocate_profile'].id}",
    )
    assert adv_reviews.status_code == 200
    rev_data = adv_reviews.json()
    assert rev_data["total"] == 1
    assert rev_data["summary"]["average_rating"] == 5.0
    assert rev_data["summary"]["review_count"] == 1


@pytest.mark.asyncio
async def test_multi_user_data_export_and_account_deletion_isolation(async_client: AsyncClient, db_session: AsyncSession):
    """Verify Download My Data exports only the requester's records, and Account Deletion does not disturb other tenants."""
    user_a = await create_user_session(async_client, db_session, email_prefix="citizena")
    user_b = await create_user_session(async_client, db_session, email_prefix="citizenb")

    # User A grants consent
    await async_client.post(
        "/api/v1/users/me/consents",
        headers=user_a["headers"],
        json={"consent_type": "terms", "version": "1.0", "purpose": "Testing export isolation"},
    )

    # User A requests data export
    export_a = await async_client.post("/api/v1/users/me/data-export", headers=user_a["headers"])
    assert export_a.status_code == 200
    export_json = export_a.json()
    assert export_json["data"]["profile"]["email"] == user_a["user"].email
    assert user_b["user"].email not in str(export_json)

    # User A deletes account
    del_res = await async_client.request(
        "DELETE",
        "/api/v1/users/me",
        headers=user_a["headers"],
        json={"confirmation": "CONFIRM_DELETE_NYAYASETU_ACCOUNT"},
    )
    assert del_res.status_code == 200

    # User A's token can no longer access /users/me (deactivated -> 403 Forbidden)
    a_me = await async_client.get("/api/v1/users/me", headers=user_a["headers"])
    assert a_me.status_code == 403

    # User B remains active and undisturbed
    b_me = await async_client.get("/api/v1/users/me", headers=user_b["headers"])
    assert b_me.status_code == 200
    assert b_me.json()["email"] == user_b["user"].email
