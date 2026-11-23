"""Exact Keyword Index using BM25Okapi for Statutory Legal Provisions."""

import re
from typing import List, Dict, Any, Tuple
from rank_bm25 import BM25Okapi


class LegalBM25Index:
    """Provides exact keyword retrieval over sections, acts, and statutory definitions."""

    def __init__(self, corpus_chunks: List[Dict[str, Any]]):
        self.chunks = corpus_chunks
        self.corpus_size = len(corpus_chunks)
        self.tokenized_corpus = [self._tokenize(c["chunk_text"]) for c in corpus_chunks]
        self.bm25 = BM25Okapi(self.tokenized_corpus)

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        """Tokenizes text preserving section numbers, act acronyms, and alphanumeric codes."""
        # Lowercase, retain alphanumeric tokens and hyphenated terms
        tokens = re.findall(r"\b[a-zA-Z0-9_\u0C80-\u0CFF\u0900-\u097F\-]+\b", text.lower())
        return tokens

    def search(self, query: str, top_k: int = 30) -> List[Tuple[Dict[str, Any], float]]:
        """Returns top_k chunks scored by BM25 relevance."""
        query_tokens = self._tokenize(query)
        if not query_tokens or self.corpus_size == 0:
            return []

        doc_scores = self.bm25.get_scores(query_tokens)

        # Sort indices by score descending
        scored_indices = sorted(
            range(len(doc_scores)),
            key=lambda i: doc_scores[i],
            reverse=True,
        )

        results = []
        for idx in scored_indices[:top_k]:
            score = float(doc_scores[idx])
            if score > 0.0:
                results.append((self.chunks[idx], score))

        return results
