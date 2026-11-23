"""Application Entry Point for Local Development."""

import asyncio
import sys
from pathlib import Path

import uvicorn

# Allow `python backend/run.py` from the repository root on macOS and Windows.
BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.core.config import settings


def main() -> None:
    """Launch the Uvicorn ASGI server using configuration settings."""
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG and settings.is_development,
        log_level=settings.LOG_LEVEL.lower(),
    )


if __name__ == "__main__":
    main()
