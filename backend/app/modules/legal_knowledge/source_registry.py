"""Persistent, auditable registry of candidate official Indian legal sources.

The CSV registry is declarative only. Every row loaded from it starts as
``PENDING`` and disabled; no URL, checksum, or verification claim from the CSV
is trusted until :mod:`legal_knowledge.fetcher` performs a live, policy-compliant
request and :mod:`legal_knowledge.sync_service` hashes the returned bytes.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
from urllib.parse import urlparse

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logging import logger
from app.modules.legal_knowledge.models import LegalSourceRegistry

DEFAULT_REGISTRY_PATH = Path(__file__).resolve().parents[4] / "docs" / "source_registry.csv"

_OFFICIAL_SUFFIXES = (".gov.in", ".nic.in", ".gov.in.", ".nic.in.")
_OFFICIAL_HOSTS = {
    "indiacode.nic.in",
    "egazette.gov.in",
    "sci.gov.in",
    "main.sci.gov.in",
    "legislative.gov.in",
}


@dataclass(frozen=True)
class SourceCandidate:
    """A single discovered official-source configuration."""

    registry_key: str
    name: str
    official_domain: str
    base_url: str
    source_category: str
    jurisdiction: str
    legal_domains: List[str]
    document_types: List[str]
    fetch_strategy: str
    parser_strategy: str
    authority_level: str
    supported_languages: List[str]
    update_frequency_hours: int
    source_config: Dict[str, Any] = field(default_factory=dict)


def is_official_indian_domain(url: str) -> bool:
    """Return True only for HTTPS URLs on Indian government/public legal domains."""
    try:
        parsed = urlparse(url)
    except Exception:
        return False
    if parsed.scheme.lower() != "https":
        return False
    host = (parsed.hostname or "").lower().rstrip(".")
    if not host:
        return False
    if host in _OFFICIAL_HOSTS:
        return True
    return any(host.endswith(suffix.rstrip(".")) for suffix in _OFFICIAL_SUFFIXES)


def _split(value: Optional[str]) -> List[str]:
    if not value:
        return []
    return [item.strip() for item in value.replace("|", ";").split(";") if item.strip()]


def _first_valid_url(*values: Optional[str]) -> str:
    for value in values:
        if value and is_official_indian_domain(value):
            return value.strip()
    return ""


def _parser_strategy(fmt: Optional[str], url: str) -> str:
    fmt_upper = (fmt or "").upper()
    if "PDF" in fmt_upper or url.lower().split("?")[0].endswith(".pdf"):
        return "PDF"
    if "XML" in fmt_upper or url.lower().split("?")[0].endswith(".xml"):
        return "XML"
    if "DOC" in fmt_upper:
        return "DOCX"
    if "HTML" in fmt_upper:
        return "HTML"
    return "TXT"


def load_source_candidates(path: Optional[Path] = None) -> List[SourceCandidate]:
    """Read declared source rows without treating any of them as verified."""
    csv_path = Path(path) if path else Path(settings.LEGAL_SOURCE_REGISTRY_CSV or DEFAULT_REGISTRY_PATH)
    if not csv_path.exists():
        logger.warning("Legal source registry CSV not found at %s", csv_path)
        return []

    candidates: List[SourceCandidate] = []
    seen: set[str] = set()
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            key = (row.get("source_id") or "").strip()
            if not key or key in seen:
                continue

            document_url = _first_valid_url(row.get("exact_document_url"), row.get("url"))
            base_url = _first_valid_url(row.get("official_url"), document_url)
            if not base_url:
                # Keep the candidate for auditability, but disabled and unverified.
                base_url = (row.get("official_url") or "").strip()
            if not base_url:
                continue

            official_domain = (urlparse(base_url).hostname or "unknown").lower()
            fetch_strategy = "STATIC_DOCUMENT" if document_url else "DISCOVERY"
            declared_checksum = (row.get("content_checksum") or "").strip() or None

            source_config: Dict[str, Any] = {
                "declared_checksum": declared_checksum,
                "declared_checksum_is_content_hash": False,
                "document_urls": [document_url] if document_url else [],
                "base_url": base_url,
                "document_id": (row.get("document_id") or "").strip() or None,
                "act_number": (row.get("act_number") or "").strip() or None,
                "act_year": (row.get("act_year") or "").strip() or None,
                "legal_intents": _split(row.get("legal_intents")),
                "commencement_status": (row.get("commencement_status") or "").strip() or None,
                "applicability_conditions": (row.get("applicability_conditions") or "").strip() or None,
                "original_language": (row.get("original_language") or "English").strip(),
            }

            candidates.append(
                SourceCandidate(
                    registry_key=key,
                    name=(row.get("title") or row.get("name") or key).strip(),
                    official_domain=official_domain,
                    base_url=base_url,
                    source_category=(row.get("source_type") or "OTHER").strip().upper(),
                    jurisdiction=(row.get("jurisdiction") or "Union of India").strip(),
                    legal_domains=_split(row.get("legal_domains")),
                    document_types=_split(row.get("source_type")) or [row.get("source_type") or "OTHER"],
                    fetch_strategy=fetch_strategy,
                    parser_strategy=_parser_strategy(row.get("format"), document_url or base_url),
                    authority_level=(row.get("tier") or "Tier 2").strip().upper(),
                    supported_languages=[(row.get("language") or "English").strip()],
                    update_frequency_hours=168,
                    source_config=source_config,
                )
            )
            seen.add(key)

    logger.info("Loaded %s declared legal source candidates from %s", len(candidates), csv_path)
    return candidates


async def upsert_source_registry(
    db: AsyncSession,
    candidates: Iterable[SourceCandidate],
    *,
    enable_verified: bool = False,
) -> List[LegalSourceRegistry]:
    """Insert or refresh registry rows without downgrading verification state."""
    existing_result = await db.execute(select(LegalSourceRegistry))
    existing = {row.registry_key: row for row in existing_result.scalars().all()}

    rows: List[LegalSourceRegistry] = []
    for candidate in candidates:
        row = existing.get(candidate.registry_key)
        if row is None:
            row = LegalSourceRegistry(registry_key=candidate.registry_key)
            db.add(row)

        row.name = candidate.name
        row.official_domain = candidate.official_domain
        row.base_url = candidate.base_url
        row.source_category = candidate.source_category
        row.jurisdiction = candidate.jurisdiction
        row.legal_domains = candidate.legal_domains
        row.document_types = candidate.document_types
        row.fetch_strategy = candidate.fetch_strategy
        row.parser_strategy = candidate.parser_strategy
        row.authority_level = candidate.authority_level
        row.supported_languages = candidate.supported_languages
        row.update_frequency_hours = candidate.update_frequency_hours
        row.source_config = candidate.source_config
        if row.verification_status not in {"VERIFIED", "REJECTED"}:
            row.verification_status = "PENDING"
        if enable_verified and row.verification_status == "VERIFIED":
            row.enabled = True
        rows.append(row)

    await db.commit()
    for row in rows:
        await db.refresh(row)
    return rows


async def bootstrap_source_registry(
    db: AsyncSession,
    *,
    path: Optional[Path] = None,
    enable_verified: bool = False,
) -> List[LegalSourceRegistry]:
    """Load the declared registry into persistent storage."""
    return await upsert_source_registry(
        db, load_source_candidates(path), enable_verified=enable_verified
    )


def utcnow() -> datetime:
    return datetime.now(timezone.utc)
