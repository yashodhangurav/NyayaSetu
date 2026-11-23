"""Comprehensive test suite for Advocate Feedback and Client Evaluations (/api/v1/reviews)."""

from datetime import datetime, timedelta, timezone
import uuid
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.modules.advocates.models import AdvocateProfile
from app.modules.appointments.models import Appointment
from app.modules.users.models import User


async def create_user_and_token(
    async_client: AsyncClient,
    db: AsyncSession,
    role: str = "CITIZEN",
    full_name: str = "Test User",
    email_prefix: str = "user",
) -> dict:
    """Helper creating user record and logging in to obtain JWT access token."""
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
        city="Bengaluru",
        state="Karnataka",
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    advocate_profile = None
    if role == "ADVOCATE":
        advocate_profile = AdvocateProfile(
            user_id=user.id,
            bar_council_id=f"KAR/{uuid.uuid4().hex[:6].upper()}/2019",
            bar_council_name="Karnataka State Bar Council",
            in_practice_years=7,
            primary_practice="Trials & Disputes",
            secondary_practices=["Commercial Arbitration", "Real Estate"],
            courts_of_practice=["Karnataka High Court", "City Civil Court, Bengaluru"],
            languages=["English", "Kannada", "Hindi"],
            city="Bengaluru",
            district="Bengaluru Urban",
            state="Karnataka",
            platform_verification_status="VERIFIED",
            fixed_consultation_fee_inr=1800.0,
            hourly_rate_inr=4000.0,
        )
        db.add(advocate_profile)
        await db.commit()
        await db.refresh(advocate_profile)

    login_res = await async_client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert login_res.status_code == 200, f"Login failed: {login_res.text}"
    token = login_res.json()["access_token"]

    return {
        "user": user,
        "advocate_profile": advocate_profile,
        "token": token,
        "headers": {"Authorization": f"Bearer {token}"},
    }


async def create_appointment(
    db: AsyncSession,
    client_id: uuid.UUID,
    advocate_id: uuid.UUID,
    status: str = "COMPLETED",
) -> Appointment:
    """Helper creating an appointment booking with specific status."""
    now = datetime.now(timezone.utc)
    appt = Appointment(
        booking_reference=f"NYA-BK-{uuid.uuid4().hex[:6].upper()}",
        client_id=client_id,
        advocate_id=advocate_id,
        scheduled_start=now - timedelta(days=2),
        scheduled_end=now - timedelta(days=2, hours=-1),
        timezone="Asia/Kolkata",
        status=status,
        mode="VIDEO_CONFERENCE",
        fee_inr=1800.0,
        payment_status="PAID",
        client_notes="Initial tenancy consultation session.",
    )
    db.add(appt)
    await db.commit()
    await db.refresh(appt)
    return appt


@pytest.mark.asyncio
async def test_review_unauthenticated_rejected(async_client: AsyncClient):
    """Unauthenticated requests to submit or modify reviews must be rejected with 401."""
    res = await async_client.post(
        "/api/v1/reviews",
        json={"booking_id": str(uuid.uuid4()), "rating": 5},
    )
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_review_for_nonexistent_booking_rejected(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Submitting evaluation for a nonexistent booking UUID returns 404 Not Found."""
    citizen = await create_user_and_token(async_client, db_session, role="CITIZEN", full_name="Citizen", email_prefix="cit")

    fake_booking_id = uuid.uuid4()
    res = await async_client.post(
        "/api/v1/reviews",
        headers=citizen["headers"],
        json={"booking_id": str(fake_booking_id), "rating": 5},
    )
    assert res.status_code == 404
    assert "not found" in res.text.lower()


@pytest.mark.asyncio
async def test_review_for_incomplete_or_cancelled_booking_rejected(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Consultations that are not yet COMPLETED cannot be evaluated (HTTP 400)."""
    citizen = await create_user_and_token(async_client, db_session, role="CITIZEN", full_name="Citizen Incomplete", email_prefix="incomp")
    advocate = await create_user_and_token(async_client, db_session, role="ADVOCATE", full_name="Advocate", email_prefix="adv2")

    for ineligible_status in ["REQUESTED", "SCHEDULED", "CONFIRMED", "CANCELLED", "REJECTED"]:
        booking = await create_appointment(
            db_session,
            client_id=citizen["user"].id,
            advocate_id=advocate["advocate_profile"].id,
            status=ineligible_status,
        )

        res = await async_client.post(
            "/api/v1/reviews",
            headers=citizen["headers"],
            json={"booking_id": str(booking.id), "rating": 5},
        )
        assert res.status_code == 400, f"Expected 400 for status {ineligible_status}, got {res.status_code}"
        assert "concluded" in res.text.lower() or "completed" in res.text.lower()


@pytest.mark.asyncio
async def test_invalid_ratings_rejected(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Ratings outside the 1–5 range must be rejected with 422 Unprocessable Entity."""
    citizen = await create_user_and_token(async_client, db_session, role="CITIZEN", full_name="Citizen Range", email_prefix="range")
    advocate = await create_user_and_token(async_client, db_session, role="ADVOCATE", full_name="Advocate Range", email_prefix="advrange")

    booking = await create_appointment(
        db_session,
        client_id=citizen["user"].id,
        advocate_id=advocate["advocate_profile"].id,
        status="COMPLETED",
    )

    for invalid_rating in [0, 6, -1, 10]:
        res = await async_client.post(
            "/api/v1/reviews",
            headers=citizen["headers"],
            json={"booking_id": str(booking.id), "rating": invalid_rating},
        )
        assert res.status_code == 422, f"Expected 422 for rating {invalid_rating}, got {res.status_code}"


@pytest.mark.asyncio
async def test_unauthorized_edit_and_deletion_rejected(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Only review author or admin can update or delete a review. Unauthorized users receive 403."""
    citizen_author = await create_user_and_token(async_client, db_session, role="CITIZEN", full_name="Author Citizen", email_prefix="author")
    citizen_other = await create_user_and_token(async_client, db_session, role="CITIZEN", full_name="Other Citizen", email_prefix="other")
    advocate = await create_user_and_token(async_client, db_session, role="ADVOCATE", full_name="Advocate Target", email_prefix="advtarget")

    booking = await create_appointment(
        db_session,
        client_id=citizen_author["user"].id,
        advocate_id=advocate["advocate_profile"].id,
        status="COMPLETED",
    )

    create_res = await async_client.post(
        "/api/v1/reviews",
        headers=citizen_author["headers"],
        json={"booking_id": str(booking.id), "rating": 4, "comment": "Initial review."},
    )
    assert create_res.status_code == 201
    review_id = create_res.json()["id"]

    # 1. Other citizen attempts to modify the review -> 403 Forbidden
    edit_res = await async_client.patch(
        f"/api/v1/reviews/{review_id}",
        headers=citizen_other["headers"],
        json={"rating": 1, "comment": "Malicious modification attempt"},
    )
    assert edit_res.status_code == 403

    # 2. Other citizen attempts to delete the review -> 403 Forbidden
    del_res = await async_client.delete(
        f"/api/v1/reviews/{review_id}",
        headers=citizen_other["headers"],
    )
    assert del_res.status_code == 403

    # 3. Author successfully updates review
    author_edit = await async_client.patch(
        f"/api/v1/reviews/{review_id}",
        headers=citizen_author["headers"],
        json={"rating": 5, "comment": "Upgraded review after matter resolution."},
    )
    assert author_edit.status_code == 200
    assert author_edit.json()["rating"] == 5

    # 4. Author successfully deletes review
    author_del = await async_client.delete(
        f"/api/v1/reviews/{review_id}",
        headers=citizen_author["headers"],
    )
    assert author_del.status_code == 204

    # 5. Review no longer exists
    get_res = await async_client.get(
        f"/api/v1/reviews/{review_id}",
        headers=citizen_author["headers"],
    )
    assert get_res.status_code == 404


@pytest.mark.asyncio
async def test_real_advocate_rating_aggregation(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Advocate average ratings and star distributions are accurately computed from persisted reviews."""
    advocate = await create_user_and_token(async_client, db_session, role="ADVOCATE", full_name="Adv. Priya Sharma", email_prefix="priya")
    adv_id = advocate["advocate_profile"].id

    # 1. Initially 0 reviews
    summary_res = await async_client.get(f"/api/v1/reviews/advocates/{adv_id}/summary")
    assert summary_res.status_code == 200
    s_data = summary_res.json()
    assert s_data["average_rating"] == 0.0
    assert s_data["review_count"] == 0

    # 2. Create 3 citizens with completed appointments
    c1 = await create_user_and_token(async_client, db_session, role="CITIZEN", full_name="Client 1", email_prefix="c1")
    c2 = await create_user_and_token(async_client, db_session, role="CITIZEN", full_name="Client 2", email_prefix="c2")
    c3 = await create_user_and_token(async_client, db_session, role="CITIZEN", full_name="Client 3", email_prefix="c3")

    b1 = await create_appointment(db_session, c1["user"].id, adv_id, status="COMPLETED")
    b2 = await create_appointment(db_session, c2["user"].id, adv_id, status="COMPLETED")
    b3 = await create_appointment(db_session, c3["user"].id, adv_id, status="COMPLETED")

    # Client 1 gives 5 stars
    await async_client.post(
        "/api/v1/reviews",
        headers=c1["headers"],
        json={"booking_id": str(b1.id), "rating": 5, "tags": ["Clear communication", "Punctual & prepared"]},
    )
    # Client 2 gives 4 stars
    await async_client.post(
        "/api/v1/reviews",
        headers=c2["headers"],
        json={"booking_id": str(b2.id), "rating": 4, "tags": ["Clear communication", "Fair statutory fee"]},
    )
    # Client 3 gives 5 stars
    await async_client.post(
        "/api/v1/reviews",
        headers=c3["headers"],
        json={"booking_id": str(b3.id), "rating": 5, "tags": ["Punctual & prepared"]},
    )

    # 3. Check aggregate summary: (5 + 4 + 5) / 3 = 14 / 3 = 4.666... -> 4.7
    summary_res2 = await async_client.get(f"/api/v1/reviews/advocates/{adv_id}/summary")
    assert summary_res2.status_code == 200
    s_data2 = summary_res2.json()
    assert s_data2["review_count"] == 3
    assert s_data2["average_rating"] == 4.7
    assert s_data2["star_distribution"]["5"] == 2
    assert s_data2["star_distribution"]["4"] == 1
    assert s_data2["star_distribution"]["3"] == 0
    assert "Clear communication" in s_data2["top_tags"]

    # 4. Check list advocate reviews endpoint
    list_res = await async_client.get(f"/api/v1/reviews/advocates/{adv_id}")
    assert list_res.status_code == 200
    list_data = list_res.json()
    assert list_data["total"] == 3
    assert len(list_data["items"]) == 3
    assert list_data["summary"]["average_rating"] == 4.7


@pytest.mark.asyncio
async def test_admin_review_moderation_flow(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Admin can moderate reviews to HIDDEN or REJECTED, removing them from public ratings."""
    admin = await create_user_and_token(async_client, db_session, role="ADMIN", full_name="Admin Reviewer", email_prefix="admin")
    citizen = await create_user_and_token(async_client, db_session, role="CITIZEN", full_name="Citizen Mod", email_prefix="cmod")
    advocate = await create_user_and_token(async_client, db_session, role="ADVOCATE", full_name="Advocate Mod", email_prefix="advmod")
    adv_id = advocate["advocate_profile"].id

    booking = await create_appointment(db_session, citizen["user"].id, adv_id, status="COMPLETED")

    # Citizen posts review
    res = await async_client.post(
        "/api/v1/reviews",
        headers=citizen["headers"],
        json={"booking_id": str(booking.id), "rating": 1, "comment": "Defamatory claim violating BCI Rule 36."},
    )
    assert res.status_code == 201
    review_id = res.json()["id"]

    # Admin moderates to HIDDEN
    mod_res = await async_client.post(
        f"/api/v1/reviews/{review_id}/moderate",
        headers=admin["headers"],
        json={"status": "HIDDEN", "moderation_reason": "Violates non-disparagement guidelines under BCI regulatory rules."},
    )
    assert mod_res.status_code == 200
    assert mod_res.json()["status"] == "HIDDEN"

    # Public summary excludes HIDDEN review: count drops to 0
    pub_summary = await async_client.get(f"/api/v1/reviews/advocates/{adv_id}/summary")
    assert pub_summary.json()["review_count"] == 0
    assert pub_summary.json()["average_rating"] == 0.0

    # Public review list excludes HIDDEN review
    pub_list = await async_client.get(f"/api/v1/reviews/advocates/{adv_id}")
    assert pub_list.json()["total"] == 0
