"""Hybrid Legal Search Engine combining BM25, Multilingual Vector, RRF, and Reranking."""

import json
import os
from typing import List, Dict, Any, Optional, Tuple

from rag.search.query_rewriter import LegalQueryRewriter, RewrittenQuery
from rag.index.bm25_index import LegalBM25Index
from rag.index.embeddings import MultilingualLegalEmbeddingEngine
from rag.search.reranker import LegalReranker


class LegalHybridSearchEngine:
    """Production Hybrid Search Engine for NyayaSetu RAG."""

    # Normalized rank alone contributes up to 0.50, so require relevance evidence.
    CONFIDENCE_THRESHOLD = 0.60

    def __init__(self, corpus_path: Optional[str] = None):
        if corpus_path is None:
            # Resolve relative to backend
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            corpus_path = os.path.join(base_dir, "data", "processed", "canonical_corpus.json")

        self.corpus_path = corpus_path
        self.chunks: List[Dict[str, Any]] = []
        self._load_corpus()

        self.bm25_index = LegalBM25Index(self.chunks)
        self.vector_engine = MultilingualLegalEmbeddingEngine(self.chunks)

    def _load_corpus(self):
        """Loads canonical legal corpus from JSON."""
        if not os.path.exists(self.corpus_path):
            raise FileNotFoundError(f"Canonical corpus not found at {self.corpus_path}. Run corpus_builder first.")
        with open(self.corpus_path, "r", encoding="utf-8") as f:
            self.chunks = json.load(f)

    def search(
        self,
        query: str,
        filter_in_force_only: bool = True,
        jurisdiction: Optional[str] = None,
        doc_type: Optional[str] = None,
        top_k: int = 6,
    ) -> Dict[str, Any]:
        """Executes full hybrid search pipeline:
        Query Rewrite -> BM25 + Vector Retrieval -> RRF Fusion (top 30) ->
        Metadata Filter -> Rerank (top 6-8) -> Confidence Gating.
        """
        rewritten: RewrittenQuery = LegalQueryRewriter.rewrite(query)

        # Immediate out-of-scope gate
        if rewritten.is_out_of_scope:
            return {
                "query": query,
                "rewritten_query": rewritten.expanded_query,
                "detected_language": rewritten.detected_language,
                "legacy_concordance_detected": rewritten.legacy_concordance_detected,
                "total_results": 0,
                "confidence_score": 0.0,
                "confidence_level": "NO_MATCH",
                "results": [],
                "message": "Query is out of scope of Indian statutory and civil law.",
            }

        search_query = rewritten.expanded_query

        # 1. BM25 Retrieval (top 30)
        bm25_results = self.bm25_index.search(search_query, top_k=30)

        # 2. Vector Semantic Retrieval (top 30)
        vector_results = self.vector_engine.search(search_query, top_k=30)

        # 3. Reciprocal Rank Fusion (RRF with k=60)
        RRF_K = 60
        rrf_scores: Dict[str, float] = {}
        chunk_map: Dict[str, Dict[str, Any]] = {}

        for rank, (chunk, score) in enumerate(bm25_results):
            cid = chunk["chunk_id"]
            chunk_map[cid] = chunk
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (1.0 / (RRF_K + rank + 1))

        for rank, (chunk, score) in enumerate(vector_results):
            cid = chunk["chunk_id"]
            chunk_map[cid] = chunk
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (1.0 / (RRF_K + rank + 1))

        requested_jurisdiction = (jurisdiction or "").strip().lower()
        national_jurisdictions = {"india", "union of india", "india (central)"}

        # 4. Apply Metadata Filters (in_force, jurisdiction, doc_type)
        filtered_candidates: List[Tuple[Dict[str, Any], float]] = []
        for cid, score in rrf_scores.items():
            chunk = chunk_map[cid]

            # 0% Repealed-law leakage filter: enforce in_force=True unless explicitly overridden
            if filter_in_force_only and not chunk.get("in_force", True):
                continue

            chunk_jurisdiction = (chunk.get("jurisdiction") or "").lower()
            if requested_jurisdiction:
                is_national = chunk_jurisdiction.startswith("india")
                matches = requested_jurisdiction in chunk_jurisdiction
                if not is_national and (requested_jurisdiction in national_jurisdictions or not matches):
                    continue

            if doc_type and doc_type.upper() != chunk.get("doc_type", "").upper():
                continue

            filtered_candidates.append((chunk, score))

        # Sort by RRF score descending
        filtered_candidates.sort(key=lambda x: x[1], reverse=True)
        top_candidates = filtered_candidates[:30]

        # Normalize RRF scores so top candidates receive balanced initial weights
        max_rrf = top_candidates[0][1] if top_candidates else 1.0
        normalized_candidates = [(chunk, (score / max_rrf) if max_rrf > 0 else score) for chunk, score in top_candidates]

        # 5. Rerank top candidates using LegalReranker
        reranked = LegalReranker.rerank(search_query, normalized_candidates, top_n=top_k)

        if not reranked:
            return {
                "query": query,
                "rewritten_query": rewritten.expanded_query,
                "detected_language": rewritten.detected_language,
                "legacy_concordance_detected": rewritten.legacy_concordance_detected,
                "total_results": 0,
                "confidence_score": 0.0,
                "confidence_level": "NO_MATCH",
                "results": [],
                "message": "No confident statutory match found.",
            }

        top_score = reranked[0][1]

        # 6. Confidence Gating
        if top_score < self.CONFIDENCE_THRESHOLD:
            return {
                "query": query,
                "rewritten_query": rewritten.expanded_query,
                "detected_language": rewritten.detected_language,
                "legacy_concordance_detected": rewritten.legacy_concordance_detected,
                "total_results": 0,
                "confidence_score": top_score,
                "confidence_level": "LOW_CONFIDENCE",
                "results": [],
                "message": "No confident statutory match found for your inquiry.",
            }

        confidence_level = "HIGH" if top_score >= 0.65 else ("MEDIUM" if top_score >= 0.45 else "LOW")

        results_payload = []
        for chunk, score in reranked:
            if score < self.CONFIDENCE_THRESHOLD:
                continue
            results_payload.append({
                "chunk_id": chunk["chunk_id"],
                "source_id": chunk["source_id"],
                "doc_type": chunk["doc_type"],
                "act": chunk["act"],
                "section": chunk.get("section"),
                "clause_heading": chunk.get("clause_heading"),
                "chapter": chunk.get("chapter"),
                "jurisdiction": chunk.get("jurisdiction"),
                "language": chunk.get("language"),
                "in_force": chunk.get("in_force"),
                "effective_date": chunk.get("effective_date"),
                "content_checksum": chunk.get("content_checksum"),
                "source_url": chunk.get("source_url"),
                "topic_tags": chunk.get("topic_tags", []),
                "chunk_text": chunk["chunk_text"],
                "relevance_score": score,
            })

        return {
            "query": query,
            "rewritten_query": rewritten.expanded_query,
            "detected_language": rewritten.detected_language,
            "legacy_concordance_detected": rewritten.legacy_concordance_detected,
            "total_results": len(results_payload),
            "confidence_score": top_score,
            "confidence_level": confidence_level,
            "results": results_payload,
        }
