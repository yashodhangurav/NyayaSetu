"""FastAPI health response contract."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check_endpoint(async_client: AsyncClient):
    """Verify that GET /api/v1/health returns HTTP 200 and expected schema including database diagnostic."""
    response = await async_client.get("/api/v1/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert "app_name" in data
    assert "version" in data
    assert "environment" in data
    assert "timestamp" in data
    assert "database" in data
    assert "status" in data["database"]
    assert "dialect" in data["database"]
    # The configured database may be the SQLite development default or PostgreSQL.
    assert data["database"]["dialect"] in ("psycopg3", "sqlite")
