"""Centralized Application Configuration Module."""

from pathlib import Path
from typing import List, Optional, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file."""

    model_config = SettingsConfigDict(
        # Resolve relative to this file, not the current working directory, so
        # `python backend/run.py` from the repo root loads the same .env as
        # `python run.py` from backend/ on both macOS and Windows.
        env_file=str(Path(__file__).resolve().parents[2] / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application Meta
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    APP_NAME: str = "NyayaSetu Backend API"
    APP_VERSION: str = "0.1.0"
    API_V1_PREFIX: str = "/api/v1"

    # Server Bindings
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Cross-Origin Resource Sharing (CORS)
    CORS_ORIGINS: Union[str, List[str]] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, value: Union[str, List[str]]) -> List[str]:
        if isinstance(value, str):
            if not value.strip():
                return ["*"]
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        elif isinstance(value, list):
            return value
        return ["*"]

    # Database Configuration (PostgreSQL with Psycopg 3)
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5432/nyayasetu"
    DATABASE_URL_SYNC: Optional[str] = None
    TEST_DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_database_url(cls, value: str) -> str:
        """Ensure the async URL uses the psycopg dialect if postgresql:// is provided."""
        if not value:
            return "postgresql+psycopg://postgres:postgres@localhost:5432/nyayasetu"
        if value.startswith("postgresql://"):
            return value.replace("postgresql://", "postgresql+psycopg://", 1)
        if value.startswith("postgres://"):
            return value.replace("postgres://", "postgresql+psycopg://", 1)
        if value.startswith("postgresql+asyncpg://"):
            return value.replace("postgresql+asyncpg://", "postgresql+psycopg://", 1)
        return value

    @property
    def sync_database_url(self) -> str:
        """Derive synchronous URL for Alembic migrations using psycopg."""
        if self.DATABASE_URL_SYNC and self.DATABASE_URL_SYNC.strip():
            url = self.DATABASE_URL_SYNC
            if url.startswith("postgresql+asyncpg://"):
                return url.replace("postgresql+asyncpg://", "postgresql+psycopg://", 1)
            if url.startswith("postgresql://"):
                return url.replace("postgresql://", "postgresql+psycopg://", 1)
            return url
        return self.DATABASE_URL.replace("postgresql+psycopg://", "postgresql+psycopg://", 1)

    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_TIMEOUT: int = 30
    DB_ECHO: bool = False

    # Supabase Integration
    SUPABASE_URL: str = ""
    SUPABASE_PUBLISHABLE_KEY: str = "sb_publishable_AghcSMNgQd1JlABKevbIGA_wROA32fu"

    # AI & Legal Embeddings Configuration
    AI_PROVIDER: str = "mock"  # "groq", "gemini" or "mock"
    GROQ_API_KEY: Optional[str] = None
    GROQ_LLM_MODEL: str = "qwen/qwen3.8-27b"
    GEMINI_API_KEY: str = ""
    GEMINI_LLM_MODEL: str = "gemini-2.5-flash"
    GEMINI_EMBEDDING_MODEL: str = "text-embedding-004"
    EMBEDDING_VECTOR_DIMENSION: int = 768

    # Grounded RAG Retrieval Parameters
    RAG_RELEVANCE_THRESHOLD: float = 0.45
    RAG_SEMANTIC_WEIGHT: float = 0.70
    RAG_LEXICAL_WEIGHT: float = 0.30
    RAG_MAX_SOURCES_LIMIT: int = 10

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    # Security, JWT & Authentication Tokens
    SECRET_KEY: str = "local-dev-secret-key-nyayasetu-2026-development-only-min32"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Advocate Matching Engine Configurable Weights
    MATCHING_WEIGHT_PRACTICE: float = 0.35
    MATCHING_WEIGHT_JURISDICTION: float = 0.25
    MATCHING_WEIGHT_LANGUAGE: float = 0.20
    MATCHING_WEIGHT_PROXIMITY: float = 0.10
    MATCHING_WEIGHT_AVAILABILITY: float = 0.10

    # Document Vault Storage Configuration (Cloudflare R2 / S3-Compatible)
    # Read exclusively from environment variables:
    # STORAGE_PROVIDER: "local" (default for development/tests) or "r2" (production)
    STORAGE_PROVIDER: str = "local"
    STORAGE_BUCKET: str = ""
    STORAGE_ENDPOINT_URL: Optional[str] = None
    STORAGE_REGION: str = "auto"
    STORAGE_ACCESS_KEY_ID: str = ""
    STORAGE_SECRET_ACCESS_KEY: str = ""
    STORAGE_PRESIGNED_EXPIRY_SECONDS: int = 900

    # Storage Capacity, Quotas and Rate Limits (Application-level limits)
    STORAGE_MAX_FILE_SIZE_BYTES: int = 10 * 1024 * 1024  # 10 MB per individual upload
    STORAGE_TOTAL_CAPACITY_BYTES: int = 8 * 1024 * 1024 * 1024  # 8 GB total application vault capacity
    STORAGE_USER_QUOTA_BYTES: int = 500 * 1024 * 1024  # 500 MB per user quota
    STORAGE_USER_MAX_DOCUMENTS: int = 50  # Max 50 documents per user
    STORAGE_USER_UPLOAD_RATE_LIMIT_PER_HOUR: int = 30  # Max 30 uploads per hour per user

    # Backward compatibility fields for legacy configuration/tests
    STORAGE_BACKEND: Optional[str] = None
    R2_ACCOUNT_ID: Optional[str] = None
    R2_ACCESS_KEY_ID: Optional[str] = None
    R2_SECRET_ACCESS_KEY: Optional[str] = None
    R2_BUCKET_NAME: Optional[str] = None
    R2_ENDPOINT_URL: Optional[str] = None
    R2_PRESIGNED_EXPIRY_SECONDS: Optional[int] = None

    @property
    def effective_storage_provider(self) -> str:
        """Resolve active storage provider identifier ('local' or 'r2')."""
        if self.STORAGE_PROVIDER and self.STORAGE_PROVIDER.strip().lower() != "local":
            return self.STORAGE_PROVIDER.strip().lower()
        if self.STORAGE_BACKEND and self.STORAGE_BACKEND.strip():
            return self.STORAGE_BACKEND.strip().lower()
        return (self.STORAGE_PROVIDER or "local").strip().lower()

    @property
    def effective_storage_bucket(self) -> str:
        """Resolve active bucket name."""
        if self.STORAGE_BUCKET and self.STORAGE_BUCKET.strip():
            return self.STORAGE_BUCKET.strip()
        if self.R2_BUCKET_NAME and self.R2_BUCKET_NAME.strip():
            return self.R2_BUCKET_NAME.strip()
        return ""

    @property
    def effective_storage_access_key_id(self) -> str:
        """Resolve S3 / R2 access key ID."""
        return (self.STORAGE_ACCESS_KEY_ID or self.R2_ACCESS_KEY_ID or "").strip()

    @property
    def effective_storage_secret_access_key(self) -> str:
        """Resolve S3 / R2 secret access key."""
        return (self.STORAGE_SECRET_ACCESS_KEY or self.R2_SECRET_ACCESS_KEY or "").strip()

    @property
    def effective_storage_region(self) -> str:
        """Resolve S3 / R2 region ('auto' for Cloudflare R2)."""
        return (self.STORAGE_REGION or "auto").strip()

    @property
    def effective_storage_endpoint_url(self) -> Optional[str]:
        """Derive full S3 endpoint URL for Cloudflare R2 if set."""
        if self.STORAGE_ENDPOINT_URL and self.STORAGE_ENDPOINT_URL.strip():
            return self.STORAGE_ENDPOINT_URL.strip()
        if self.R2_ENDPOINT_URL and self.R2_ENDPOINT_URL.strip():
            return self.R2_ENDPOINT_URL.strip()
        if self.R2_ACCOUNT_ID and self.R2_ACCOUNT_ID.strip():
            return f"https://{self.R2_ACCOUNT_ID.strip()}.r2.cloudflarestorage.com"
        return None

    @property
    def effective_r2_endpoint_url(self) -> Optional[str]:
        """Backward-compatible alias for effective_storage_endpoint_url."""
        return self.effective_storage_endpoint_url

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"

    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT.lower() == "development"

    @property
    def is_testing(self) -> bool:
        return self.ENVIRONMENT.lower() in ("test", "testing")


def validate_ai_configuration(settings_obj: Optional[Settings] = None) -> None:
    """Validate the selected AI provider at startup."""
    cfg = settings_obj or settings
    provider = (cfg.AI_PROVIDER or "mock").lower().strip()

    if provider == "groq":
        if not (cfg.GROQ_API_KEY or "").strip() or not cfg.GROQ_LLM_MODEL.strip():
            raise RuntimeError("AI_PROVIDER=groq requires GROQ_API_KEY and GROQ_LLM_MODEL.")
        return

    if cfg.is_production:
        if provider == "mock":
            raise RuntimeError(
                "Production startup failed: AI_PROVIDER cannot be 'mock' in production. "
                "Configure AI_PROVIDER='groq' or AI_PROVIDER='gemini' with its API key."
            )
        if provider != "gemini":
            raise ValueError(
                f"Production startup failed: Unsupported AI_PROVIDER '{cfg.AI_PROVIDER}'. "
                f"Supported production providers are 'groq' and 'gemini'."
            )
        if not cfg.GEMINI_API_KEY or not cfg.GEMINI_API_KEY.strip():
            raise RuntimeError(
                "Production startup failed: GEMINI_API_KEY is required in production when AI_PROVIDER='gemini'. "
                "Please set GEMINI_API_KEY in your environment variables or production secrets."
            )
        try:
            from google import genai  # noqa: F401
        except ImportError as exc:
            raise RuntimeError(
                "Production startup failed: Required SDK 'google-genai' is not installed. "
                "Please run 'pip install google-genai' or 'pip install -r requirements.txt'."
            ) from exc
    else:
        # Development / Test mode validations
        if provider not in ("gemini", "mock"):
            import logging
            logging.getLogger("uvicorn.error").warning(
                f"Unknown AI_PROVIDER '{cfg.AI_PROVIDER}' in development. Falling back to deterministic mock."
            )


def validate_storage_configuration(settings_obj: Optional[Settings] = None) -> None:
    """Validate storage provider configuration for the current environment.

    Enforces strict production safety without leaking credentials:
    1. Production mode MUST NOT silently use or fall back to local filesystem storage.
    2. In production, STORAGE_PROVIDER must be 'r2'.
    3. In production, STORAGE_ACCESS_KEY_ID, STORAGE_SECRET_ACCESS_KEY, STORAGE_BUCKET,
       and STORAGE_ENDPOINT_URL must be configured and non-empty.
    4. Required SDK ('boto3' and 'botocore') must be installed.
    5. In development/testing, 'local' storage is allowed.
    """
    cfg = settings_obj or settings
    provider = cfg.effective_storage_provider

    if cfg.is_production:
        if provider == "local":
            raise RuntimeError(
                "Production startup failed: STORAGE_PROVIDER cannot be 'local' in production. "
                "Local filesystem storage is prohibited in production to prevent ephemeral data loss. "
                "Set STORAGE_PROVIDER='r2' and configure Cloudflare R2 credentials."
            )
        if provider != "r2":
            raise ValueError(
                f"Production startup failed: Unsupported STORAGE_PROVIDER '{provider}'. "
                f"Supported production storage provider is 'r2'."
            )
        if not cfg.effective_storage_access_key_id:
            raise RuntimeError(
                "Production startup failed: STORAGE_ACCESS_KEY_ID is required in production when STORAGE_PROVIDER='r2'."
            )
        if not cfg.effective_storage_secret_access_key:
            raise RuntimeError(
                "Production startup failed: STORAGE_SECRET_ACCESS_KEY is required in production when STORAGE_PROVIDER='r2'."
            )
        if not cfg.effective_storage_bucket:
            raise RuntimeError(
                "Production startup failed: STORAGE_BUCKET is required in production when STORAGE_PROVIDER='r2'."
            )
        if not cfg.effective_storage_endpoint_url:
            raise RuntimeError(
                "Production startup failed: STORAGE_ENDPOINT_URL must be configured for Cloudflare R2 in production."
            )
        try:
            import boto3  # noqa: F401
            import botocore  # noqa: F401
        except ImportError as exc:
            raise RuntimeError(
                "Production startup failed: Required SDK 'boto3'/'botocore' is not installed. "
                "Please run 'pip install -r requirements.txt'."
            ) from exc
    else:
        if provider not in ("local", "r2"):
            import logging
            logging.getLogger("uvicorn.error").warning(
                f"Unknown STORAGE_PROVIDER '{provider}' in development. Falling back to local filesystem."
            )


settings = Settings()
