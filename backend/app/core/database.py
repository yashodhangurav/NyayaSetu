"""Database Configuration, Declarative Base, and Session Management using SQLAlchemy 2.

Development defaults to SQLite (`sqlite+aiosqlite`) so the API runs without an
external database server. Point `DATABASE_URL` at PostgreSQL/Psycopg 3 to use
PostGIS and pgvector in production.
"""

import asyncio
import sys
import time
import uuid

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any, AsyncGenerator, Dict, Optional

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import DBAPIError, OperationalError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import text

from app.core.config import settings
from app.core.logging import logger


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy 2 ORM models in NyayaSetu."""

    def to_dict(self) -> Dict[str, Any]:
        """Convert model instance attributes to a serializable dictionary."""
        result = {}
        for key in self.__mapper__.c.keys():
            val = getattr(self, key)
            if isinstance(val, (datetime, uuid.UUID)):
                result[key] = str(val)
            else:
                result[key] = val
        return result

    def __repr__(self) -> str:
        ident = getattr(self, "id", None)
        return f"<{self.__class__.__name__}(id={ident})>"


class TimestampMixin:
    """Standard audit timestamps mixin applied across models."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


# Async database engine. SQLite (development default) and PostgreSQL are both supported.
_engine_kwargs: Dict[str, Any] = {"echo": settings.DB_ECHO}
if not settings.is_sqlite:
    # PostgreSQL connection pool tuning (SQLite ignores/does not support these).
    _engine_kwargs.update(
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
        pool_timeout=settings.DB_POOL_TIMEOUT,
        pool_pre_ping=True,
    )

engine = create_async_engine(settings.DATABASE_URL, **_engine_kwargs)

# Centralized session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI route dependency yielding an isolated async database session with automatic commit & rollback."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as err:
            await session.rollback()
            logger.error(f"Database transaction error: {str(err)}", exc_info=True)
            raise
        except Exception as err:
            await session.rollback()
            logger.error(f"Unexpected error inside DB session: {str(err)}", exc_info=True)
            raise
        finally:
            await session.close()


@asynccontextmanager
async def get_db_context() -> AsyncGenerator[AsyncSession, None]:
    """Context manager for standalone scripts, background tasks, and migrations."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def initialize_database() -> None:
    """Create the schema when running on SQLite.

    Alembic revisions in this repository target PostgreSQL (PostGIS/pgvector),
    so a local SQLite database is initialised directly from ORM metadata.
    PostgreSQL deployments continue to use `alembic upgrade head`.
    """
    if not settings.is_sqlite:
        return

    # Imported lazily so every model is registered on Base.metadata first.
    from app.core.models import Base as ModelsBase

    async with engine.begin() as conn:
        await conn.run_sync(ModelsBase.metadata.create_all)

    logger.info(f"SQLite schema ready at {settings.DATABASE_URL}")


async def check_db_health() -> Dict[str, Any]:
    """Execute a health check against the configured database."""
    start_time = time.perf_counter()
    database_dialect = engine.dialect.name
    health_status: Dict[str, Any] = {
        "status": "disconnected",
        "latency_ms": None,
        "dialect": "sqlite" if settings.is_sqlite else "psycopg3",
        "extensions": {},
        "error": None,
    }

    try:
        async with AsyncSessionLocal() as session:
            # 1. Basic ping with timeout
            await asyncio.wait_for(session.execute(text("SELECT 1")), timeout=1.5)
            latency = (time.perf_counter() - start_time) * 1000
            health_status["status"] = "connected"
            health_status["latency_ms"] = round(latency, 2)

            if database_dialect == "postgresql":
                # 2. Check for required extensions (PostGIS, pgvector, uuid-ossp)
                ext_query = text(
                    "SELECT extname, extversion FROM pg_extension "
                    "WHERE extname IN ('postgis', 'vector', 'uuid-ossp');"
                )
                result = await asyncio.wait_for(session.execute(ext_query), timeout=1.5)
                ext_map = {row[0]: row[1] for row in result.fetchall()}
                health_status["extensions"] = {
                    "postgis": ext_map.get("postgis", "not_installed"),
                    "vector": ext_map.get("vector", "not_installed"),
                    "uuid-ossp": ext_map.get("uuid-ossp", "not_installed"),
                }
            else:
                health_status["extensions"] = {
                    "postgis": "not_applicable",
                    "vector": "not_applicable",
                    "uuid-ossp": "not_applicable",
                }
    except (asyncio.TimeoutError, TimeoutError):
        health_status["status"] = "unreachable"
        health_status["error"] = "Database connection timed out"
    except OperationalError as op_err:
        health_status["status"] = "unreachable"
        health_status["error"] = "Connection refused or host unreachable"
        logger.debug(f"Database operational probe notice: {op_err}")
    except DBAPIError as db_err:
        health_status["status"] = "error"
        health_status["error"] = str(db_err.orig) if hasattr(db_err, "orig") else str(db_err)
        logger.debug(f"Database probe DBAPI error: {db_err}")
    except Exception as exc:
        health_status["status"] = "error"
        health_status["error"] = str(exc)
        logger.debug(f"Database probe general exception: {exc}")

    return health_status
