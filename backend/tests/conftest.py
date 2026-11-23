"""Pytest shared test fixtures with isolated in-memory test database."""

import os
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Set testing environment variables before importing app
os.environ["ENVIRONMENT"] = "testing"
os.environ["DEBUG"] = "true"
os.environ["SECRET_KEY"] = "test-secret-key-32-characters-long-min-jwt-secret-testing"
os.environ["AI_PROVIDER"] = "mock"

from app.core.database import get_db
from app.core.models import Base
from app.main import app
from app.modules.legal_assistant.embedding_provider import reset_embedding_provider

# Isolated SQLite in-memory test database engine
test_engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    echo=False,
)

TestingAsyncSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture
def isolated_embedding_provider():
    reset_embedding_provider()
    yield
    reset_embedding_provider()


@pytest_asyncio.fixture
async def setup_test_database():
    """Only database clients need a schema. Closing the engine discards the in-memory database."""
    try:
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield
    finally:
        await test_engine.dispose()


@pytest_asyncio.fixture
async def db_session(setup_test_database):
    """Yields a dedicated test database session."""
    async with TestingAsyncSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def async_client(setup_test_database):
    """Async test client bound to FastAPI application with test database override."""
    async def override_get_db():
        async with TestingAsyncSessionLocal() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client

    app.dependency_overrides.clear()
