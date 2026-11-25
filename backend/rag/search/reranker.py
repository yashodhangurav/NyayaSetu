"""Cross-Encoder / Legal Reranker Module with Statutory Confidence Scoring."""

import re
from typing import List, Dict, Any, Tuple


class LegalReranker:
    """Reranks retrieved candidate chunks based on statutory alignment, section precision,
    and cross-lingual relevance, outputting normalized confidence scores."""

    @classmethod
    def score_candidate(cls, query: str, chunk: Dict[str, Any], initial_rank_score: float) -> float:
        """Scores candidate chunk based on exact section match, statutory title match,
        and query overlap."""
        q_lower = query.lower()
        chunk_text = chunk["chunk_text"].lower()
        act = chunk["act"].lower()
        section = (chunk.get("section") or "").lower()
        heading = (chunk.get("clause_heading") or "").lower()

        # Base score from RRF retrieval rank (normalized)
        score = initial_rank_score * 0.55

        # Exact section number mention in query (e.g. 138, 27, 318, 173, 185)
        clean_sec = section.replace("section", "").replace("article", "").strip()
        if clean_sec and re.search(rf"\b{re.escape(clean_sec)}\b", q_lower):
            score += 0.35

        # Exact Act name or shortcode in query
        short_code = (chunk.get("short_code") or "").lower()
        if short_code and short_code in q_lower:
            score += 0.20
        elif any(part in q_lower for part in act.split() if len(part) > 4):
            score += 0.15

        # Heading keyword alignment with prefix matching
        heading_words = [w for w in re.findall(r"\w+", heading) if len(w) > 3]
        if heading_words:
            matched_heading_words = sum(
                1 for w in heading_words
                if w in q_lower or any(qw.startswith(w[:4]) or w.startswith(qw[:4]) for qw in re.findall(r"\w+", q_lower) if len(qw) > 3)
            )
            score += 0.18 * (matched_heading_words / len(heading_words))

        # Query term density in chunk text with stem/prefix support
        q_words = [w for w in re.findall(r"\w+", q_lower) if len(w) > 3]
        if q_words:
            matched_body_words = sum(
                1 for w in q_words
                if w in chunk_text or (len(w) >= 4 and w[:4] in chunk_text)
            )
            score += 0.18 * min(1.0, matched_body_words / max(3, len(q_words)))

        # Topic tags match
        tags = chunk.get("topic_tags", [])
        if any(tag.lower() in q_lower or any(tw in q_lower for tw in tag.lower().split() if len(tw) > 4) for tag in tags):
            score += 0.18

        return min(round(score, 4), 1.0)

    @classmethod
    def rerank(
        cls,
        query: str,
        candidates: List[Tuple[Dict[str, Any], float]],
        top_n: int = 6,
    ) -> List[Tuple[Dict[str, Any], float]]:
        """Reranks candidate list and returns top_n items sorted by score descending."""
        if not candidates:
            return []

        rescored = []
        for chunk, initial_score in candidates:
            final_score = cls.score_candidate(query, chunk, initial_score)
            rescored.append((chunk, final_score))

        rescored.sort(key=lambda x: x[1], reverse=True)
        return rescored[:top_n]
