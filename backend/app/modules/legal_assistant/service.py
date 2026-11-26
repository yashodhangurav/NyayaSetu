"""Legal AI Assistant Orchestration Service."""

import asyncio
from datetime import datetime, timezone
import re
from typing import Optional

from starlette.concurrency import run_in_threadpool
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logging import logger
from app.modules.admin.models import AuditLog
from app.modules.legal_assistant.citation_validator import CitationValidator
from app.modules.legal_assistant.llm_provider import get_llm_provider
from app.modules.legal_assistant.retrieval import LegalRetrievalEngine
from app.modules.legal_assistant.schemas import LegalAskRequest, LegalAskResponse
from app.modules.users.models import User


from rag.search.hybrid_search import LegalHybridSearchEngine

# Global singleton hybrid search engine
_hybrid_engine: Optional[LegalHybridSearchEngine] = None

def get_hybrid_engine() -> LegalHybridSearchEngine:
    global _hybrid_engine
    if _hybrid_engine is None:
        _hybrid_engine = LegalHybridSearchEngine()
    return _hybrid_engine


class LegalAssistantService:
    """End-to-end RAG orchestrator for grounded legal question answering."""

    @staticmethod
    def detect_language(query: str, preferred: str = "en") -> str:
        """Identify question language: English, Hindi, or Kannada."""
        # Devanagari Unicode block (0900-097F) -> Hindi / Marathi
        if re.search(r"[\u0900-\u097F]", query):
            return "hi"
        # Kannada Unicode block (0C80-0CFF) -> Kannada
        if re.search(r"[\u0C80-\u0CFF]", query):
            return "kn"
        if preferred in ["hi", "kn"]:
            return preferred
        return "en"

    @classmethod
    async def ask(
        cls,
        db: AsyncSession,
        payload: LegalAskRequest,
        current_user: Optional[User] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> LegalAskResponse:
        """Execute grounded legal question answering workflow."""
        detected_lang = cls.detect_language(payload.query, payload.preferred_language)
        greeting = re.sub(r"[.!?,]+$", "", payload.query.casefold()).strip()
        if greeting in {"hi", "hello", "hey", "namaste", "नमस्ते", "ನಮಸ್ಕಾರ"}:
            messages = {
                "en": "Hello! I can help you understand Indian laws and legal procedures. What would you like to ask?",
                "hi": "नमस्ते! मैं भारतीय कानूनों और कानूनी प्रक्रियाओं को समझने में आपकी मदद कर सकता हूँ। आप क्या पूछना चाहेंगे?",
                "kn": "ನಮಸ್ಕಾರ! ಭಾರತೀಯ ಕಾನೂನುಗಳು ಮತ್ತು ಕಾನೂನು ಪ್ರಕ್ರಿಯೆಗಳನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳಲು ನಾನು ಸಹಾಯ ಮಾಡಬಲ್ಲೆ. ನಿಮ್ಮ ಪ್ರಶ್ನೆ ಏನು?",
            }
            return LegalAskResponse(
                query=payload.query,
                kind="greeting",
                detected_language=detected_lang,
                answer=messages[detected_lang],
                sources_found=False,
                retrieved_chunks_count=0,
                assessed_at=datetime.now(timezone.utc),
            )
        database_available = True
        try:
            async with asyncio.timeout(3 if settings.is_development else None):
                retrieved_chunks = await LegalRetrievalEngine.retrieve(
                    db=db,
                    query=payload.query,
                    jurisdiction=payload.jurisdiction,
                    max_sources=payload.max_sources,
                )
        except (OperationalError, TimeoutError):
            if not settings.is_development:
                raise
            await db.rollback()
            logger.warning("Legal database unavailable in development. Searching the bundled corpus.")
            database_available = False
            retrieved_chunks = []
        if not retrieved_chunks:
            search_res = await run_in_threadpool(
                lambda: get_hybrid_engine().search(
                    query=payload.query,
                    filter_in_force_only=True,
                    jurisdiction=payload.jurisdiction,
                    top_k=payload.max_sources,
                )
            )
            if search_res.get("results"):
                for c in search_res.get("results", []):
                    retrieved_chunks.append({
                        "source_title": c.get("act", "Indian Statute"),
                        "source_type": c.get("doc_type", "BARE_ACT"),
                        "act_or_judgment_identifier": c["source_id"],
                        "section_number": c.get("section", ""),
                        "section_or_paragraph": c.get("section", ""),
                        "clause_heading": c.get("clause_heading", ""),
                        "chunk_text": c["chunk_text"],
                        "official_source_url": c.get("source_url", "https://indiacode.nic.in"),
                        "content_checksum": c.get("content_checksum") or c.get("chunk_id", ""),
                        "jurisdiction": c.get("jurisdiction", "India"),
                        "is_verified_in_corpus": True,
                    })

        # 4. Generate structured grounded answer via LLM Provider (Groq in dev/prod, Deterministic in test)
        llm = get_llm_provider()
        llm_output = await run_in_threadpool(
            llm.generate_legal_answer,
            query=payload.query,
            retrieved_chunks=retrieved_chunks,
            language=detected_lang,
        )

        generation_status = str(llm_output.get("generation_status") or "ok")
        generation_error = llm_output.get("generation_error")
        retry_after_seconds = llm_output.get("retry_after_seconds")
        is_retryable = bool(llm_output.get("is_retryable", False))
        provider_name = getattr(llm, "provider_name", llm.__class__.__name__)

        # Provider-transport failures are returned verbatim.
        # Do not duplicate the error string into confidence_note.
        if generation_status in {"rate_limited", "timeout", "provider_unavailable", "generation_error"}:
            safe_answer = str(llm_output.get("answer") or generation_error or generation_status)
            return LegalAskResponse(
                query=payload.query,
                detected_language=detected_lang,
                answer=safe_answer,
                decision_badge="Advocate advised",
                sources_found=False,
                confidence_level="LOW",
                confidence_note=None,
                follow_up_suggestions=[],
                retrieved_chunks_count=len(retrieved_chunks),
                generation_status=generation_status,
                generation_error=safe_answer,
                retry_after_seconds=retry_after_seconds,
                is_retryable=is_retryable,
                provider_name=provider_name,
                assessed_at=datetime.now(timezone.utc),
            )

        # 5. Validate citations strictly against retrieved context
        raw_claimed_refs = llm_output.get("cited_references", [])
        raw_answer = llm_output.get("answer", "")
        verified_citations, unverified_pruned = CitationValidator.validate_and_filter_citations(
            answer_text=raw_answer,
            claimed_references=raw_claimed_refs,
            retrieved_chunks=retrieved_chunks,
        )
        final_answer = CitationValidator.sanitize_answer_prose(raw_answer, unverified_pruned)

        sources_found = (
            llm_output.get("sources_found", False)
            and len(verified_citations) > 0
            and len(retrieved_chunks) > 0
        )

        if not retrieved_chunks:
            sources_found = False

        # 6. Build DeadlineInfo if provided
        deadline_obj = None
        raw_dl = llm_output.get("deadline")
        if raw_dl and isinstance(raw_dl, dict) and raw_dl.get("title"):
            deadline_obj = {
                "title": raw_dl.get("title"),
                "days_remaining": raw_dl.get("days_remaining"),
                "target_date": raw_dl.get("target_date"),
                "statutory_basis": raw_dl.get("statutory_basis"),
                "action_label": "Add to Court Deadlines",
            }

        # 7. Audit Query & Response
        if database_available:
            audit = AuditLog(
                actor_id=current_user.id if current_user else None,
                action="LEGAL_AI_QUERY_ANSWERED",
                entity_type="legal_assistant_rag",
                entity_id=None,
                ip_address=ip_address,
                user_agent=user_agent,
                payload_snapshot={
                    "query": payload.query[:200],
                    "language": detected_lang,
                    "jurisdiction": payload.jurisdiction,
                    "retrieved_count": len(retrieved_chunks),
                    "citations_verified_count": len(verified_citations),
                    "unverified_detected": unverified_pruned,
                    "sources_found": sources_found,
                },
            )
            db.add(audit)
            try:
                await db.commit()
            except Exception:
                await db.rollback()

        next_steps = llm_output.get("next_steps") or llm_output.get("suggested_next_steps") or []
        follow_ups = llm_output.get("follow_up_suggestions") or [
            "What specific documents should I prepare for this matter?",
            "What is the statutory limitation deadline for taking legal action?",
            "Can an empanelled advocate assist in drafting a response or petition?",
        ]

        return LegalAskResponse(
            query=payload.query,
            detected_language=detected_lang,
            answer=final_answer,
            decision_badge=llm_output.get("decision_badge", "Self-help first"),
            sources_found=sources_found,
            citations=verified_citations,
            unverified_citations_detected=unverified_pruned,
            legal_points=llm_output.get("legal_points", []),
            documents_to_gather=llm_output.get("documents_to_gather", []),
            facts_to_confirm=llm_output.get("facts_to_confirm", []),
            suggested_next_steps=next_steps,
            deadline=deadline_obj,
            confidence_level=llm_output.get("confidence_level", "HIGH") if sources_found else "LOW",
            confidence_note=llm_output.get("confidence_note"),
            follow_up_suggestions=follow_ups,
            retrieved_chunks_count=len(retrieved_chunks),
            generation_status=generation_status,
            generation_error=generation_error,
            retry_after_seconds=retry_after_seconds,
            is_retryable=is_retryable,
            provider_name=provider_name,
            assessed_at=datetime.now(timezone.utc),
        )
