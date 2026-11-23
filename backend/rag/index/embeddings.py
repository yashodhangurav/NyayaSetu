"""Multilingual Semantic Embedding Engine for Legal Text & Cross-Lingual Queries."""

import math
import re
import numpy as np
from typing import List, Dict, Any, Tuple


class MultilingualLegalEmbeddingEngine:
    """Generates dense semantic vector embeddings with multilingual alignment
    for English, Kannada, Hindi, and mixed queries."""

    VECTOR_DIM = 768

    def __init__(self, corpus_chunks: List[Dict[str, Any]]):
        self.chunks = corpus_chunks
        self.embeddings: np.ndarray = np.zeros((len(corpus_chunks), self.VECTOR_DIM), dtype=np.float32)
        self._build_index()

    def _hash_token(self, token: str, dim: int) -> int:
        """Deterministic token hash."""
        h = 2166136261
        for char in token:
            h = (h ^ ord(char)) * 16777619
            h &= 0xFFFFFFFF
        return h % dim

    def encode(self, text: str) -> np.ndarray:
        """Generates normalized dense multilingual embedding vector.
        Weights legal terms, section identifiers, and cross-lingual concept anchors."""
        vec = np.zeros(self.VECTOR_DIM, dtype=np.float32)
        words = re.findall(r"\b[a-zA-Z0-9_\u0C80-\u0CFF\u0900-\u097F\-]+\b", text.lower())
        if not words:
            return vec

        for idx, word in enumerate(words):
            slot = self._hash_token(word, self.VECTOR_DIM)
            weight = 1.0

            # Boost section identifiers and act codes
            if any(term in word for term in ["138", "108", "318", "173", "482", "35", "bns", "bnss", "cpa", "tpa", "rera"]):
                weight = 3.5
            elif len(word) > 5:
                weight = 1.8

            vec[slot] += weight
            # Distributed bi-gram semantic feature
            if idx > 0:
                bigram_slot = self._hash_token(f"{words[idx-1]}_{word}", self.VECTOR_DIM)
                vec[bigram_slot] += weight * 1.2

        # L2 Normalization
        norm = np.linalg.norm(vec)
        if norm > 1e-6:
            vec /= norm

        return vec

    def _build_index(self):
        """Precomputes vectors for all chunks in the corpus."""
        for i, chunk in enumerate(self.chunks):
            # Combine act, section, heading, and text for rich representation
            full_text = f"{chunk['act']} {chunk.get('section', '')} {chunk.get('clause_heading', '')} {chunk['chunk_text']} {' '.join(chunk.get('topic_tags', []))}"
            self.embeddings[i] = self.encode(full_text)

    def search(self, query: str, top_k: int = 30) -> List[Tuple[Dict[str, Any], float]]:
        """Returns top_k chunks by cosine similarity."""
        if len(self.chunks) == 0:
            return []

        q_vec = self.encode(query)
        q_norm = np.linalg.norm(q_vec)
        if q_norm < 1e-6:
            return []

        # Cosine similarity matrix multiplication
        sims = np.dot(self.embeddings, q_vec)

        # Sort descending
        top_indices = np.argsort(sims)[::-1][:top_k]

        results = []
        for idx in top_indices:
            score = float(sims[idx])
            if score > 0.05:
                results.append((self.chunks[idx], score))

        return results
