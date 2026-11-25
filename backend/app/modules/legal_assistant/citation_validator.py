"""Citation Validation Engine.

Strictly verifies that every cited legal section, Bare Act, or judgment
originates from authentic, retrieved records in the curated knowledge base.
Prunes or flags any attempted hallucinations.
"""

import re
from typing import Any, Dict, List, Optional, Set, Tuple

from app.core.logging import logger
from app.modules.legal_assistant.schemas import CitationItem


# Stop words are ignored only for the claim-support heuristic; they are never used
# to rewrite or weaken retrieved statutory text.
_CLAIM_STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "been", "being", "by", "can", "could",
    "for", "from", "has", "have", "having", "he", "her", "here", "him", "his", "how",
    "in", "into", "is", "it", "its", "may", "might", "more", "must", "of", "on", "or",
    "our", "shall", "she", "should", "that", "the", "their", "them", "there", "these",
    "they", "this", "to", "under", "was", "we", "were", "what", "when", "where", "which",
    "who", "why", "will", "with", "would", "you", "your", "provides", "provides that",
    "law", "law provides", "section", "act", "acts", "legal", "provision", "provisions",
}

_META_CLAIM_MARKERS = (
    "no verified legal sources",
    "consult an empanelled advocate",
    "formal legal advice",
    "advocate-client relationship",
    "does not constitute",
    "high similarity score",
    "informational guidance",
    "provide additional matter facts",
    "please specify",
    "before i can explain",
    "हिंदी सारांश",
    "ಕನ್ನಡ ಸಾರಾಂಶ",
    " परामर्श करें",
    " ಸಂಪರ್ಕಿಸಿ",
)


class CitationValidator:
    """Post-generation statutory and judicial citation validator."""

    @classmethod
    def validate_and_filter_citations(
        cls,
        answer_text: str,
        claimed_references: List[Dict[str, Any]],
        retrieved_chunks: List[Dict[str, Any]],
    ) -> Tuple[List[CitationItem], List[str]]:
        """Cross-check all citations against actual retrieved source chunks.
        
        Returns:
            Tuple of (verified_citations, unverified_citations_detected)
        """
        # 1. Build lookup sets of authentic sections and source titles present in retrieved context
        authentic_sections: Set[str] = set()
        authentic_titles: Set[str] = set()
        chunk_map: Dict[str, Dict[str, Any]] = {}

        for chunk in retrieved_chunks:
            sec = (chunk.get("section_number") or "").strip().lower()
            title = (chunk.get("source_title") or "").strip().lower()
            chunk_body = (chunk.get("chunk_text") or "").lower()
            if sec:
                authentic_sections.add(sec)
                chunk_map[sec] = chunk
            if title:
                authentic_titles.add(title)
                chunk_map[title] = chunk

            # Also register authentic statutory cross-references appearing in the verified Bare Act chunk text
            for cross_ref in re.findall(r"\bsection\s+(\d+[a-z]?)\b", chunk_body):
                authentic_sections.add(f"section {cross_ref}")
                authentic_sections.add(cross_ref)

        verified_citations: List[CitationItem] = []
        unverified_detected: List[str] = []
        seen_citations: Set[str] = set()

        # 2. Validate claimed references provided by LLM provider
        for ref in claimed_references:
            sec = (ref.get("section_or_paragraph") or "").strip()
            sec_lower = sec.lower()
            title = (ref.get("source_title") or "").strip()
            title_lower = title.lower()

            # Check if this section or title was actually present in retrieved chunks
            is_grounded = (sec_lower in authentic_sections) or (title_lower in authentic_titles)

            if is_grounded:
                cit_key = f"{title}_{sec}"
                if cit_key not in seen_citations:
                    seen_citations.add(cit_key)
                    matching_chunk = next(
                        (chunk for chunk in retrieved_chunks
                         if ref.get("content_checksum") and chunk.get("content_checksum") == ref["content_checksum"]
                         and chunk.get("source_title", "").strip().lower() == title_lower
                         and (chunk.get("section_number") or "").strip().lower() == sec_lower),
                        chunk_map.get(sec_lower) or chunk_map.get(title_lower) or {},
                    )
                    raw_text_snippet = matching_chunk.get("relevant_text") or (
                        matching_chunk.get("chunk_text")[:280] + "..."
                        if matching_chunk.get("chunk_text") and len(matching_chunk.get("chunk_text")) > 280
                        else matching_chunk.get("chunk_text")
                    )

                    verified_citations.append(
                        CitationItem(
                            source_title=title or matching_chunk.get("source_title", "Official Bare Act"),
                            source_type=ref.get("source_type") or matching_chunk.get("source_type", "BARE_ACT"),
                            act_or_judgment_identifier=ref.get("act_or_judgment_identifier") or matching_chunk.get("act_or_judgment_identifier"),
                            section_or_paragraph=sec or matching_chunk.get("section_number"),
                            clause_heading=ref.get("clause_heading") or matching_chunk.get("clause_heading"),
                            official_source_url=ref.get("official_source_url") or matching_chunk.get("official_source_url"),
                            jurisdiction=matching_chunk.get("jurisdiction", "Union of India"),
                            document_version=matching_chunk.get("document_version", "1.0"),
                            relevant_text=raw_text_snippet,
                            content_checksum=ref.get("content_checksum") or matching_chunk.get("content_checksum"),
                            is_verified_in_corpus=True,
                        )
                    )
            else:
                unverified_desc = f"{title} ({sec})" if sec else title
                unverified_detected.append(unverified_desc)
                logger.warning(f"Unverified citation detected and pruned: {unverified_desc}")

        # 3. Check for any hallucinated sections in answer text not present in retrieved context
        mentioned_sections = re.findall(r"\bsection\s+(\d+[a-z]?)\b", answer_text, re.IGNORECASE)
        for mention in mentioned_sections:
            formatted_sec = f"section {mention.lower()}"
            if not any(formatted_sec == s or f"section {mention.lower()}" in s for s in authentic_sections):
                unverified_detected.append(f"Section {mention} (Hallucinated / not in retrieved corpus)")
                logger.warning(f"Pruned ungrounded section mention: Section {mention}")

        return verified_citations, list(dict.fromkeys(unverified_detected))

    @classmethod
    def sanitize_answer_prose(cls, answer_text: str, unverified_citations: List[str]) -> str:
        """Sanitizes generated answer prose by neutralising any fabricated or unverified statutory mentions."""
        if not unverified_citations or not answer_text:
            return answer_text

        sanitized = answer_text
        for unverified in unverified_citations:
            match = re.search(r"Section\s+([0-9]+[a-z]?)", unverified, re.IGNORECASE)
            if match:
                sec_num = match.group(1)
                pattern = re.compile(rf"\b(section\s+{sec_num})\b", re.IGNORECASE)
                sanitized = pattern.sub(r"the relevant statutory provision", sanitized)

        return sanitized

    @staticmethod
    def split_claims(answer_text: str) -> List[str]:
        """Split generated prose into checkable claim-sized sentences."""
        if not answer_text:
            return []
        clean = re.sub(r"\*\*|__|`", "", answer_text)
        clean = re.sub(r"\s+", " ", clean)
        parts = re.split(r"(?<=[.!?।])\s+|\n+", clean)
        return [part.strip() for part in parts if part.strip()]

    @staticmethod
    def _content_tokens(text: str) -> Set[str]:
        tokens = re.findall(r"[\w]+", text.casefold(), flags=re.UNICODE)
        return {
            token for token in tokens
            if len(token) > 1
            and (token.isdigit() or token not in _CLAIM_STOP_WORDS)
        }

    @classmethod
    def verify_claim_support(
        cls,
        answer_text: str,
        retrieved_chunks: List[Dict[str, Any]],
        *,
        min_overlap: Optional[float] = None,
    ) -> Tuple[List[str], List[str], Dict[str, Any]]:
        """Check each substantive sentence against the retrieved source text.

        This is a conservative lexical support check, not legal reasoning. It is used
        to flag unsupported generation for review and to trigger abstention only when
        no verified citation exists. Retrieved text is always treated as data.
        """
        threshold = min_overlap if min_overlap is not None else 0.25
        claims = cls.split_claims(answer_text)
        if not claims:
            return [], [], {"claim_count": 0, "support_ratio": 1.0, "threshold": threshold}

        corpus_text = " ".join(
            " ".join(
                str(chunk.get(key) or "")
                for key in ("chunk_text", "relevant_text", "clause_heading", "source_title")
            )
            for chunk in retrieved_chunks
        )
        corpus_tokens = cls._content_tokens(corpus_text)
        supported: List[str] = []
        unsupported: List[str] = []
        for claim in claims:
            lowered = claim.casefold()
            if any(marker in lowered for marker in _META_CLAIM_MARKERS):
                continue
            tokens = cls._content_tokens(claim)
            if len(tokens) < 3:
                # Short transitions and citations carry no independent factual claim.
                continue
            overlap = len(tokens & corpus_tokens) / len(tokens)
            if overlap >= threshold:
                supported.append(claim)
            else:
                unsupported.append(claim)
                logger.warning("Unsupported generated claim flagged: %s", claim[:180])

        substantive = len(supported) + len(unsupported)
        ratio = len(supported) / substantive if substantive else 1.0
        return supported, unsupported, {
            "claim_count": substantive,
            "supported_claims": len(supported),
            "unsupported_claims": len(unsupported),
            "support_ratio": round(ratio, 4),
            "threshold": threshold,
        }
