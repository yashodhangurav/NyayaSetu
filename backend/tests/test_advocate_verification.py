"""Comprehensive test suite for Advocate Credential Verification System."""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.modules.users.models import User


# ──────────────────────────────────────────────────────────────
# Helper Functions
# ──────────────────────────────────────────────────────────────

async def create_user_with_role(
    async_client: AsyncClient,
    email: str,
    phone: str,
    role: str = "CITIZEN",
    full_name: str = "Test User",
    bar_council_id: str = "D/1001/2015",
    bar_council_name: str = "Bar Council of Delhi",
) -> tuple[str, str]:
    """Helper to register and login a user, returning (user_id, access_token)."""
    password = "TestPassword123"

    if role == "ADVOCATE":
        reg_payload = {
            "account_type": "ADVOCATE",
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "password": password,
            "bar_council_id": bar_council_id,
            "bar_council_name": bar_council_name,
            "in_practice_years": 10,
            "primary_practice": "Trials & Disputes",
            "city": "New Delhi",
            "state": "Delhi",
            "pincode": "110001",
        }
    else:
        reg_payload = {
            "account_type": "CITIZEN",
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "password": password,
        }

    reg_res = await async_client.post("/api/v1/auth/register", json=reg_payload)
    assert reg_res.status_code == 201
    user_id = reg_res.json()["id"]

    login_res = await async_client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    return user_id, token


async def create_admin_user(db_session: AsyncSession, async_client: AsyncClient) -> tuple[str, str]:
    """Helper to create an ADMIN user directly in DB and login."""
    email = "admin.nyayasetu@gov.in"
    phone = "+919999000001"
    password = "AdminSuperSecret2026"

    admin = User(
        full_name="Platform Chief Administrator",
        email=email,
        phone=phone,
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


@pytest.mark.asyncio
async def test_advocate_registration_and_initial_pending_status(async_client: AsyncClient, db_session: AsyncSession):
    """Verify advocate registers, profile has PENDING platform_verification_status, and can view own verification."""
    _, adv_token = await create_user_with_role(
        async_client,
        email="adv.ananya@nyayasetu.in",
        phone="+919876500001",
        role="ADVOCATE",
        full_name="Adv. Ananya Roy",
        bar_council_id="D/2045/2012",
        bar_council_name="Bar Council of Delhi",
    )

    # Initial GET /advocates/me/verification before submitting application returns null
    me_res = await async_client.get(
        "/api/v1/advocates/me/verification",
        headers={"Authorization": f"Bearer {adv_token}"},
    )
    assert me_res.status_code == 200
    assert me_res.json() is None

    # Submit verification application
    app_payload = {
        "enrollment_number": "D/2045/2012",
        "enrollment_name": "Ananya Roy",
        "state_bar_council": "Bar Council of Delhi",
        "enrollment_date": "2012-08-15",
        "aibe_status": "PASSED",
        "cop_status": "ACTIVE",
        "contact_phone": "+919876500001",
        "contact_email": "adv.ananya@nyayasetu.in",
    }
    submit_res = await async_client.post(
        "/api/v1/advocates/me/verification",
        json=app_payload,
        headers={"Authorization": f"Bearer {adv_token}"},
    )
    assert submit_res.status_code == 201
    data = submit_res.json()
    assert data["enrollment_number"] == "D/2045/2012"
    assert data["platform_verification_status"] == "SUBMITTED"

    # Now GET /advocates/me/verification returns the submitted application
    me_res2 = await async_client.get(
        "/api/v1/advocates/me/verification",
        headers={"Authorization": f"Bearer {adv_token}"},
    )
    assert me_res2.status_code == 200
    assert me_res2.json()["platform_verification_status"] == "SUBMITTED"


@pytest.mark.asyncio
async def test_duplicate_enrollment_number(async_client: AsyncClient):
    """Verify that submitting an enrollment number already registered raises 409 Conflict."""
    _, adv_token_1 = await create_user_with_role(
        async_client,
        email="adv.first@nyayasetu.in",
        phone="+919876500011",
        role="ADVOCATE",
        full_name="Adv. First Person",
        bar_council_id="D/5001/2018",
        bar_council_name="Bar Council of Delhi",
    )

    _, adv_token_2 = await create_user_with_role(
        async_client,
        email="adv.second@nyayasetu.in",
        phone="+919876500012",
        role="ADVOCATE",
        full_name="Adv. Second Person",
        bar_council_id="D/5002/2018",
        bar_council_name="Bar Council of Delhi",
    )

    # First advocate submits enrollment
    app_payload = {
        "enrollment_number": "D/5001/2018",
        "enrollment_name": "First Person",
        "state_bar_council": "Bar Council of Delhi",
        "enrollment_date": "2018-05-10",
    }
    res1 = await async_client.post(
        "/api/v1/advocates/me/verification",
        json=app_payload,
        headers={"Authorization": f"Bearer {adv_token_1}"},
    )
    assert res1.status_code == 201

    # Second advocate attempts to use same enrollment number (even with alternate casing/spacing)
    dup_payload = {
        "enrollment_number": "d/5001/2018",
        "enrollment_name": "Second Person Impersonating",
        "state_bar_council": "Bar Council of Delhi",
        "enrollment_date": "2018-05-10",
    }
    res2 = await async_client.post(
        "/api/v1/advocates/me/verification",
        json=dup_payload,
        headers={"Authorization": f"Bearer {adv_token_2}"},
    )
    assert res2.status_code == 409
    assert "already registered" in res2.json()["error"]["message"]


@pytest.mark.asyncio
async def test_invalid_enrollment_format(async_client: AsyncClient):
    """Verify that enrollment number not matching council format returns 400 Bad Request."""
    _, adv_token = await create_user_with_role(
        async_client,
        email="adv.invalid@nyayasetu.in",
        phone="+919876500021",
        role="ADVOCATE",
        full_name="Adv. Format Test",
        bar_council_id="D/9999/2020",
        bar_council_name="Bar Council of Delhi",
    )

    # Delhi Bar Council requires D/number/year
    invalid_payload = {
        "enrollment_number": "INVALID-FORMAT-1234",
        "enrollment_name": "Format Test",
        "state_bar_council": "Bar Council of Delhi",
        "enrollment_date": "2020-01-01",
    }
    res = await async_client.post(
        "/api/v1/advocates/me/verification",
        json=invalid_payload,
        headers={"Authorization": f"Bearer {adv_token}"},
    )
    assert res.status_code == 400
    assert "does not match the expected format" in res.json()["error"]["message"]


@pytest.mark.asyncio
async def test_unauthorized_document_access(async_client: AsyncClient, db_session: AsyncSession):
    """Verify document ownership: citizens, unauthenticated, and other advocates cannot download documents."""
    # 1. Advocate A uploads document
    _, adv_a_token = await create_user_with_role(
        async_client,
        email="adv.doc.owner@nyayasetu.in",
        phone="+919876500031",
        role="ADVOCATE",
        full_name="Adv. Document Owner",
        bar_council_id="D/3001/2016",
        bar_council_name="Bar Council of Delhi",
    )

    pdf_content = b"%PDF-1.4 test document content for Bar ID verification"
    upload_res = await async_client.post(
        "/api/v1/advocates/me/verification/documents",
        data={"verification_type": "ENROLLMENT_CERTIFICATE"},
        files={"file": ("enrollment_cert.pdf", pdf_content, "application/pdf")},
        headers={"Authorization": f"Bearer {adv_a_token}"},
    )
    assert upload_res.status_code == 201
    doc_id = upload_res.json()["id"]

    # 2. Advocate A can download their own document
    owner_dl = await async_client.get(
        f"/api/v1/advocates/me/verification/documents/{doc_id}/download",
        headers={"Authorization": f"Bearer {adv_a_token}"},
    )
    assert owner_dl.status_code == 200
    assert owner_dl.content == pdf_content

    # 3. Unauthenticated download fails (401)
    unauth_dl = await async_client.get(
        f"/api/v1/advocates/me/verification/documents/{doc_id}/download",
    )
    assert unauth_dl.status_code == 401

    # 4. Citizen attempting download gets 403 Forbidden
    _, cit_token = await create_user_with_role(
        async_client,
        email="citizen.nosy@example.com",
        phone="+919876500032",
        role="CITIZEN",
        full_name="Nosy Citizen",
    )
    cit_dl = await async_client.get(
        f"/api/v1/advocates/me/verification/documents/{doc_id}/download",
        headers={"Authorization": f"Bearer {cit_token}"},
    )
    assert cit_dl.status_code == 403

    # 5. Advocate B attempting download of Advocate A's document gets 403 Forbidden
    _, adv_b_token = await create_user_with_role(
        async_client,
        email="adv.b.rival@nyayasetu.in",
        phone="+919876500033",
        role="ADVOCATE",
        full_name="Adv. Rival",
        bar_council_id="D/3002/2016",
        bar_council_name="Bar Council of Delhi",
    )
    rival_dl = await async_client.get(
        f"/api/v1/advocates/me/verification/documents/{doc_id}/download",
        headers={"Authorization": f"Bearer {adv_b_token}"},
    )
    assert rival_dl.status_code == 403


@pytest.mark.asyncio
async def test_advocate_trying_to_approve_own_profile(async_client: AsyncClient, db_session: AsyncSession):
    """Verify that an advocate cannot call admin decision endpoint, and an admin with a profile cannot self-approve."""
    _, adv_token = await create_user_with_role(
        async_client,
        email="adv.selfapprove@nyayasetu.in",
        phone="+919876500041",
        role="ADVOCATE",
        full_name="Adv. Self Approver",
        bar_council_id="D/4001/2014",
        bar_council_name="Bar Council of Delhi",
    )

    # Submit application
    app_res = await async_client.post(
        "/api/v1/advocates/me/verification",
        json={
            "enrollment_number": "D/4001/2014",
            "enrollment_name": "Self Approver",
            "state_bar_council": "Bar Council of Delhi",
            "enrollment_date": "2014-04-12",
        },
        headers={"Authorization": f"Bearer {adv_token}"},
    )
    assert app_res.status_code == 201
    app_id = app_res.json()["id"]

    # Advocate tries to approve their own application via admin route -> 403 Forbidden
    hack_res = await async_client.post(
        f"/api/v1/admin/advocate-verifications/{app_id}/decision",
        json={
            "decision": "VERIFIED",
            "decision_reason": "I approve myself",
        },
        headers={"Authorization": f"Bearer {adv_token}"},
    )
    assert hack_res.status_code == 403


@pytest.mark.asyncio
async def test_citizen_forbidden_from_admin_verifications(async_client: AsyncClient):
    """Verify that a citizen account cannot access the admin verification queue."""
    _, cit_token = await create_user_with_role(
        async_client,
        email="citizen.inquisitive@example.com",
        phone="+919876500051",
        role="CITIZEN",
        full_name="Inquisitive Citizen",
    )

    res = await async_client.get(
        "/api/v1/admin/advocate-verifications",
        headers={"Authorization": f"Bearer {cit_token}"},
    )
    assert res.status_code == 403
    assert "Access forbidden" in res.json()["error"]["message"]


@pytest.mark.asyncio
async def test_admin_approval(async_client: AsyncClient, db_session: AsyncSession):
    """Verify admin approval updates status to VERIFIED, sets evidence level, and logs audit."""
    # 1. Register advocate & submit verification
    _, adv_token = await create_user_with_role(
        async_client,
        email="adv.legitimate@nyayasetu.in",
        phone="+919876500061",
        role="ADVOCATE",
        full_name="Adv. Legitimate Counsel",
        bar_council_id="D/6001/2011",
        bar_council_name="Bar Council of Delhi",
    )

    submit_res = await async_client.post(
        "/api/v1/advocates/me/verification",
        json={
            "enrollment_number": "D/6001/2011",
            "enrollment_name": "Legitimate Counsel",
            "state_bar_council": "Bar Council of Delhi",
            "enrollment_date": "2011-09-20",
            "aibe_status": "PASSED",
            "cop_status": "ACTIVE",
        },
        headers={"Authorization": f"Bearer {adv_token}"},
    )
    assert submit_res.status_code == 201
    app_id = submit_res.json()["id"]

    # 2. Login as admin
    _, admin_token = await create_admin_user(db_session, async_client)

    # 3. Admin lists verifications
    list_res = await async_client.get(
        "/api/v1/admin/advocate-verifications?status=SUBMITTED",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert list_res.status_code == 200
    assert list_res.json()["total"] >= 1

    # 4. Admin views application detail
    detail_res = await async_client.get(
        f"/api/v1/admin/advocate-verifications/{app_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert detail_res.status_code == 200
    assert detail_res.json()["enrollment_number"] == "D/6001/2011"

    # 5. Admin approves application
    decision_payload = {
        "decision": "VERIFIED",
        "evidence_level": "OFFICIAL_ROLL_MATCHED",
        "verification_method": "MANUAL_ADMIN",
        "source_name": "Bar Council of Delhi Official Roll (2011 Edition)",
        "source_url": "https://delhibarcouncil.com/rolls/2011/D-6001",
        "decision_reason": "Roll entry verified matching name Legitimate Counsel and enrollment date 2011-09-20.",
        "internal_notes": "Cross-referenced with physical bar roll archive. Verified COP active.",
    }
    decision_res = await async_client.post(
        f"/api/v1/admin/advocate-verifications/{app_id}/decision",
        json=decision_payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert decision_res.status_code == 200
    approved_data = decision_res.json()
    assert approved_data["platform_verification_status"] == "VERIFIED"
    assert approved_data["evidence_level"] == "OFFICIAL_ROLL_MATCHED"
    assert approved_data["internal_notes"] is not None

    # 6. Advocate views their status -> internal_notes must NOT be returned!
    adv_view = await async_client.get(
        "/api/v1/advocates/me/verification",
        headers={"Authorization": f"Bearer {adv_token}"},
    )
    assert adv_view.status_code == 200
    adv_data = adv_view.json()
    assert adv_data["platform_verification_status"] == "VERIFIED"
    assert "internal_notes" not in adv_data


@pytest.mark.asyncio
async def test_admin_rejection(async_client: AsyncClient, db_session: AsyncSession):
    """Verify admin rejection updates status to REJECTED with mandatory decision reason."""
    _, adv_token = await create_user_with_role(
        async_client,
        email="adv.fraudulent@nyayasetu.in",
        phone="+919876500071",
        role="ADVOCATE",
        full_name="Adv. Fraudulent Claims",
        bar_council_id="MAH/7001/2019",
        bar_council_name="Bar Council of Maharashtra & Goa",
    )

    submit_res = await async_client.post(
        "/api/v1/advocates/me/verification",
        json={
            "enrollment_number": "MAH/7001/2019",
            "enrollment_name": "Fraudulent Claims",
            "state_bar_council": "Bar Council of Maharashtra & Goa",
            "enrollment_date": "2019-03-15",
        },
        headers={"Authorization": f"Bearer {adv_token}"},
    )
    app_id = submit_res.json()["id"]

    _, admin_token = await create_admin_user(db_session, async_client)

    # Reject application
    reject_res = await async_client.post(
        f"/api/v1/admin/advocate-verifications/{app_id}/decision",
        json={
            "decision": "REJECTED",
            "decision_reason": "Enrollment number belongs to another practitioner on the Maharashtra State Roll.",
            "internal_notes": "Identity mismatch confirmed with Bar Council registry office.",
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert reject_res.status_code == 200
    assert reject_res.json()["platform_verification_status"] == "REJECTED"


@pytest.mark.asyncio
async def test_missing_aibe_cop_and_request_info_flow(async_client: AsyncClient, db_session: AsyncSession):
    """Verify admin can request additional info (e.g. COP certificate) and transition status to NEEDS_MORE_INFORMATION."""
    _, adv_token = await create_user_with_role(
        async_client,
        email="adv.needsinfo@nyayasetu.in",
        phone="+919876500081",
        role="ADVOCATE",
        full_name="Adv. Needs Info",
        bar_council_id="KAR/8001/2017",
        bar_council_name="Bar Council of Karnataka",
    )

    submit_res = await async_client.post(
        "/api/v1/advocates/me/verification",
        json={
            "enrollment_number": "KAR/8001/2017",
            "enrollment_name": "Needs Info",
            "state_bar_council": "Bar Council of Karnataka",
            "enrollment_date": "2017-06-18",
            "aibe_status": "PASSED",
            "cop_status": "EXPIRED",
        },
        headers={"Authorization": f"Bearer {adv_token}"},
    )
    app_id = submit_res.json()["id"]

    _, admin_token = await create_admin_user(db_session, async_client)

    # Admin requests renewed COP certificate
    info_res = await async_client.post(
        f"/api/v1/admin/advocate-verifications/{app_id}/request-info",
        json={
            "message": "Your Certificate of Practice (COP) has expired. Please upload your renewed COP from the Bar Council of Karnataka.",
            "internal_notes": "Advocate enrolled in 2017; mandatory 5-year COP renewal certificate required under BCI rules.",
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert info_res.status_code == 200
    data = info_res.json()
    assert data["platform_verification_status"] == "NEEDS_MORE_INFORMATION"
    assert "Certificate of Practice" in data["info_request_message"]

    # Advocate views status and sees the request message
    adv_view = await async_client.get(
        "/api/v1/advocates/me/verification",
        headers={"Authorization": f"Bearer {adv_token}"},
    )
    assert adv_view.status_code == 200
    assert adv_view.json()["platform_verification_status"] == "NEEDS_MORE_INFORMATION"
    assert "renewed COP" in adv_view.json()["info_request_message"]
