"""Lightweight RAG observability without transmitting user content.

Events contain request identifiers, hashes, counts, and configuration state only.
No query text, user identity, private document, or retrieved legal text is logged
to the optional JSONL sink or exposed by the summary endpoint.
"""

from __future__ import annotations

import hashlib
import json
import threading
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from app.core.config import settings
from app.core.logging import logger


class RagObservability:
    """In-process counters plus an optional local JSONL event sink."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._events: list[Dict[str, Any]] = []
        self._counts: Counter[str] = Counter()
        self._by_source: Dict[str, Counter[str]] = defaultdict(Counter)

    @staticmethod
    def content_fingerprint(text: str) -> str:
        """Return a non-reversible fingerprint for correlating events."""
        return hashlib.sha256(text.strip().casefold().encode("utf-8")).hexdigest()[:16]

    def record(self, event: Dict[str, Any]) -> None:
        if not settings.RAG_OBSERVABILITY_ENABLED:
            return
        safe_event = dict(event)
        safe_event.setdefault("recorded_at", datetime.now(timezone.utc).isoformat())
        query = safe_event.pop("query", None)
        if query and not safe_event.get("query_fingerprint"):
            safe_event["query_fingerprint"] = RagObservability.content_fingerprint(str(query))
        safe_event.pop("answer", None)
        safe_event.pop("user_id", None)

        with self._lock:
            self._events.append(safe_event)
            if len(self._events) > 1000:
                self._events.pop(0)
            self._counts["events"] += 1
            source = str(safe_event.get("retrieval_source") or "UNKNOWN")
            self._by_source[source]["events"] += 1
            if safe_event.get("sources_found"):
                self._by_source[source]["with_sources"] += 1
            if safe_event.get("retrieval_sufficient") is True:
                self._by_source[source]["sufficient"] += 1
            if safe_event.get("unsupported_claims"):
                self._counts["responses_with_unsupported_claims"] += 1
            if safe_event.get("official_fallback_queued"):
                self._counts["official_fallbacks_queued"] += 1

        self._append_to_file(safe_event)

    def _append_to_file(self, event: Dict[str, Any]) -> None:
        path = (settings.RAG_OBSERVABILITY_LOG_PATH or "").strip()
        if not path:
            return
        try:
            target = Path(path)
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(event, ensure_ascii=False, default=str) + "\n")
        except OSError as exc:
            logger.warning("Could not write RAG observability event: %s", exc)

    def summary(self, *, limit: int = 20) -> Dict[str, Any]:
        with self._lock:
            return {
                "enabled": settings.RAG_OBSERVABILITY_ENABLED,
                "counts": dict(self._counts),
                "by_retrieval_source": {
                    source: dict(counters) for source, counters in self._by_source.items()
                },
                "recent_events": list(self._events[-limit:]),
                "note": (
                    "Events contain hashes and counts only. This is an operational signal, "
                    "not a legal-quality benchmark."
                ),
            }

    def reset(self) -> None:
        with self._lock:
            self._events.clear()
            self._counts.clear()
            self._by_source.clear()


rag_observability = RagObservability()


def record_answer_event(
    *,
    request_id: str,
    query: str,
    detected_language: str,
    retrieval: Any,
    sources_found: bool,
    citation_count: int,
    unverified_count: int,
    claim_diagnostics: Optional[Dict[str, Any]] = None,
    provider_name: str = "",
) -> None:
    """Record a single grounded-answer event with no user or document content."""
    claim_diagnostics = claim_diagnostics or {}
    rag_observability.record(
        {
            "event_type": "LEGAL_ANSWER_GENERATED",
            "request_id": request_id,
            "query_fingerprint": RagObservability.content_fingerprint(query),
            "detected_language": detected_language,
            "retrieval_source": getattr(retrieval, "source", "UNKNOWN"),
            "retrieval_sufficient": bool(getattr(retrieval, "sufficient", False)),
            "retrieved_chunks": len(getattr(retrieval, "chunks", []) or []),
            "sources_found": bool(sources_found),
            "citation_count": citation_count,
            "unverified_citation_count": unverified_count,
            "unsupported_claims": int(claim_diagnostics.get("unsupported_claims") or 0),
            "claim_support_ratio": claim_diagnostics.get("support_ratio"),
            "provider_name": provider_name,
        }
    )
