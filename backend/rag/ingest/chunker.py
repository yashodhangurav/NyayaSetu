"""Legal structure-aware chunking engine for Indian statutes, judgments, and guides."""

import hashlib
import uuid
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict

from rag.ingest.cleaner import LegalTextCleaner


@dataclass
class StandardizedLegalChunk:
    chunk_id: str
    source_id: str
    doc_type: str  # STATUTE | PROCEDURE | JUDGMENT | FAQS | GLOSSARY
    act: str
    short_code: Optional[str]
    section: Optional[str]
    clause_heading: Optional[str]
    chapter: Optional[str]
    jurisdiction: str
    language: str
    in_force: bool
    effective_date: Optional[str]
    repealed_by: Optional[str]
    topic_tags: List[str]
    chunk_text: str
    token_count: int
    content_checksum: str
    source_url: str
    version: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class LegalStructureChunker:
    """Implements section-based structural chunking per Section 1.4 specifications."""

    MAX_TOKENS_PER_CHUNK = 800  # Token threshold before splitting

    @classmethod
    def estimate_token_count(cls, text: str) -> int:
        """Heuristic word-based token estimator (~1.3 tokens per word for legal text)."""
        words = len(text.split())
        return int(words * 1.3)

    @classmethod
    def chunk_statute_section(
        cls,
        source_id: str,
        act: str,
        short_code: str,
        section: str,
        clause_heading: str,
        section_text: str,
        chapter: Optional[str] = None,
        jurisdiction: str = "India (Central)",
        language: str = "en",
        in_force: bool = True,
        effective_date: Optional[str] = None,
        repealed_by: Optional[str] = None,
        topic_tags: Optional[List[str]] = None,
        source_url: str = "https://www.indiacode.nic.in",
        version: str = "2024.1",
    ) -> List[StandardizedLegalChunk]:
        """Creates one chunk per section, preserving sub-sections, provisos, and explanations.
        Splits only if >800 tokens, repeating the section heading in each part."""
        cleaned_body = LegalTextCleaner.clean_text(section_text)
        header_prefix = f"{act} · {section} ({clause_heading})\n\n"
        full_content = f"{header_prefix}{cleaned_body}"
        token_count = cls.estimate_token_count(full_content)

        topic_tags = topic_tags or []

        if token_count <= cls.MAX_TOKENS_PER_CHUNK:
            checksum = hashlib.sha256(full_content.encode("utf-8")).hexdigest()
            chunk_id = f"chk_{short_code.lower()}_{section.lower().replace(' ', '_').replace('.', '')}_{checksum[:8]}"
            return [
                StandardizedLegalChunk(
                    chunk_id=chunk_id,
                    source_id=source_id,
                    doc_type="STATUTE",
                    act=act,
                    short_code=short_code,
                    section=section,
                    clause_heading=clause_heading,
                    chapter=chapter,
                    jurisdiction=jurisdiction,
                    language=language,
                    in_force=in_force,
                    effective_date=effective_date,
                    repealed_by=repealed_by,
                    topic_tags=topic_tags,
                    chunk_text=full_content,
                    token_count=token_count,
                    content_checksum=checksum,
                    source_url=source_url,
                    version=version,
                )
            ]

        # Content exceeds 800 tokens: split by paragraphs / subsections and repeat heading prefix
        paragraphs = cleaned_body.split("\n\n")
        chunks: List[StandardizedLegalChunk] = []
        current_part = []
        current_tokens = cls.estimate_token_count(header_prefix)
        part_idx = 1

        for para in paragraphs:
            para_tokens = cls.estimate_token_count(para)
            if current_tokens + para_tokens > cls.MAX_TOKENS_PER_CHUNK and current_part:
                part_text = f"{header_prefix}[Part {part_idx}]\n" + "\n\n".join(current_part)
                chk_sum = hashlib.sha256(part_text.encode("utf-8")).hexdigest()
                chk_id = f"chk_{short_code.lower()}_{section.lower().replace(' ', '_').replace('.', '')}_p{part_idx}_{chk_sum[:8]}"
                chunks.append(
                    StandardizedLegalChunk(
                        chunk_id=chk_id,
                        source_id=source_id,
                        doc_type="STATUTE",
                        act=act,
                        short_code=short_code,
                        section=section,
                        clause_heading=f"{clause_heading} (Part {part_idx})",
                        chapter=chapter,
                        jurisdiction=jurisdiction,
                        language=language,
                        in_force=in_force,
                        effective_date=effective_date,
                        repealed_by=repealed_by,
                        topic_tags=topic_tags,
                        chunk_text=part_text,
                        token_count=current_tokens,
                        content_checksum=chk_sum,
                        source_url=source_url,
                        version=version,
                    )
                )
                part_idx += 1
                current_part = [para]
                current_tokens = cls.estimate_token_count(header_prefix) + para_tokens
            else:
                current_part.append(para)
                current_tokens += para_tokens

        if current_part:
            part_text = f"{header_prefix}[Part {part_idx}]\n" + "\n\n".join(current_part)
            chk_sum = hashlib.sha256(part_text.encode("utf-8")).hexdigest()
            chk_id = f"chk_{short_code.lower()}_{section.lower().replace(' ', '_').replace('.', '')}_p{part_idx}_{chk_sum[:8]}"
            chunks.append(
                StandardizedLegalChunk(
                    chunk_id=chk_id,
                    source_id=source_id,
                    doc_type="STATUTE",
                    act=act,
                    short_code=short_code,
                    section=section,
                    clause_heading=f"{clause_heading} (Part {part_idx})",
                    chapter=chapter,
                    jurisdiction=jurisdiction,
                    language=language,
                    in_force=in_force,
                    effective_date=effective_date,
                    repealed_by=repealed_by,
                    topic_tags=topic_tags,
                    chunk_text=part_text,
                    token_count=current_tokens,
                    content_checksum=chk_sum,
                    source_url=source_url,
                    version=version,
                )
            )

        return chunks

    @classmethod
    def chunk_judgment_summary(
        cls,
        source_id: str,
        case_title: str,
        citation: str,
        court: str,
        judgment_date: str,
        issue: str,
        holding: str,
        ratio_decidendi: str,
        topic_tags: List[str],
        source_url: str = "https://main.sci.gov.in/judgment",
    ) -> StandardizedLegalChunk:
        """Chunks landmark judgment into structured Issue, Holding, and Ratio Decidendi."""
        chunk_text = (
            f"Landmark Judgment: {case_title} · {citation}\n"
            f"Court: {court} | Date of Decision: {judgment_date}\n\n"
            f"ISSUE:\n{issue}\n\n"
            f"HOLDING:\n{holding}\n\n"
            f"RATIO DECIDENDI & BINDING PRINCIPLE:\n{ratio_decidendi}"
        )
        checksum = hashlib.sha256(chunk_text.encode("utf-8")).hexdigest()
        clean_tag = case_title.split()[0].lower()
        chunk_id = f"chk_case_{clean_tag}_{checksum[:8]}"
        tokens = cls.estimate_token_count(chunk_text)

        return StandardizedLegalChunk(
            chunk_id=chunk_id,
            source_id=source_id,
            doc_type="JUDGMENT",
            act=case_title,
            short_code="CASE_LAW",
            section=citation,
            clause_heading=f"Precedent Ratio: {case_title}",
            chapter=court,
            jurisdiction="India (Supreme Court / High Courts)",
            language="en",
            in_force=True,
            effective_date=judgment_date,
            repealed_by=None,
            topic_tags=topic_tags,
            chunk_text=chunk_text,
            token_count=tokens,
            content_checksum=checksum,
            source_url=source_url,
            version="1.0",
        )

    @classmethod
    def chunk_procedure_guide(
        cls,
        source_id: str,
        title: str,
        step_heading: str,
        guide_text: str,
        topic_tags: List[str],
        jurisdiction: str = "India (Central)",
        language: str = "en",
        source_url: str = "https://nalsa.gov.in",
    ) -> StandardizedLegalChunk:
        """Chunks procedural manuals and citizen self-help steps by heading/workflow."""
        chunk_text = f"Citizen Procedural Guide: {title}\nWorkflow Step: {step_heading}\n\n{guide_text}"
        checksum = hashlib.sha256(chunk_text.encode("utf-8")).hexdigest()
        chunk_id = f"chk_proc_{source_id.lower()}_{checksum[:8]}"
        tokens = cls.estimate_token_count(chunk_text)

        return StandardizedLegalChunk(
            chunk_id=chunk_id,
            source_id=source_id,
            doc_type="PROCEDURE",
            act=title,
            short_code="PROC",
            section=step_heading,
            clause_heading=step_heading,
            chapter="Citizen Enforcement & Procedure",
            jurisdiction=jurisdiction,
            language=language,
            in_force=True,
            effective_date="2024-07-01",
            repealed_by=None,
            topic_tags=topic_tags,
            chunk_text=chunk_text,
            token_count=tokens,
            content_checksum=checksum,
            source_url=source_url,
            version="1.0",
        )
