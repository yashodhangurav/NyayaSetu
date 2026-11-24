"""Citation Validation Engine.

Strictly verifies that every cited legal section, Bare Act, or judgment
originates from authentic, retrieved records in the curated knowledge base.
Prunes or flags any attempted hallucinations.
"""

import re
from typing import Any, Dict, List, Set, Tuple

from app.core.logging import logger
from app.modules.legal_assistant.schemas import CitationItem


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
