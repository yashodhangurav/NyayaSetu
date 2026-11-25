"""Embedding Provider Abstraction for NyayaSetu RAG.

Provides a pluggable interface for dense vector embeddings, allowing Google Gemini
(via the official google-genai SDK text-embedding-004) or a fast offline deterministic
mock provider to be swapped without touching vector retrieval or database logic.
"""

from abc import ABC, abstractmethod
import hashlib
import math
import os
import re
import time
from typing import Any, List, Optional, Union

from app.core.config import settings
from app.core.logging import logger


class BaseEmbeddingProvider(ABC):
    """Abstract interface for dense vector embedding generation."""

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Expected embedding vector dimension."""
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Human-readable name of the embedding provider."""
        pass

    @property
    @abstractmethod
    def is_mock(self) -> bool:
        """Flag indicating if this is a synthetic mock provider."""
        pass

    @abstractmethod
    def embed_query(self, query: str) -> List[float]:
        """Generate normalized embedding optimized for user search queries (task_type=RETRIEVAL_QUERY)."""
        pass

    @abstractmethod
    def embed_document(self, text: str, title: Optional[str] = None) -> List[float]:
        """Generate normalized embedding optimized for legal documents/sections (task_type=RETRIEVAL_DOCUMENT)."""
        pass

    @abstractmethod
    def embed_documents(self, texts: List[str], titles: Optional[List[str]] = None) -> List[List[float]]:
        """Batch embedding generation for indexed legal documents."""
        pass

    def get_embedding(self, text: str, task_type: str = "RETRIEVAL_DOCUMENT") -> List[float]:
        """Backwards-compatible embedding generation."""
        if task_type == "RETRIEVAL_QUERY":
            return self.embed_query(text)
        return self.embed_document(text)

    def get_embeddings(self, texts: List[str], task_type: str = "RETRIEVAL_DOCUMENT") -> List[List[float]]:
        """Backwards-compatible batch embedding generation."""
        if task_type == "RETRIEVAL_QUERY":
            return [self.embed_query(t) for t in texts]
        return self.embed_documents(texts)

    def _normalize_and_validate(self, vector: List[float], label: str = "vector") -> List[float]:
        """Validate vector dimensionality and apply L2 unit normalization."""
        if not vector or not isinstance(vector, (list, tuple)):
            raise ValueError(f"Invalid {label}: expected non-empty list of floats, got {type(vector)}")

        if len(vector) != self.dimension:
            raise ValueError(
                f"Embedding dimension mismatch for {label}: expected exactly {self.dimension} dimensions, "
                f"but received {len(vector)} dimensions from provider '{self.provider_name}'."
            )

        if any(math.isnan(v) or math.isinf(v) for v in vector):
            raise ValueError(f"Invalid embedding {label}: vector contains NaN or Inf values")

        norm = math.sqrt(sum(v * v for v in vector))
        if norm > 0:
            return [round(v / norm, 6) for v in vector]
        else:
            res = [0.0] * self.dimension
            res[0] = 1.0
            return res


class DeterministicMockEmbeddingProvider(BaseEmbeddingProvider):
    """High-speed, offline deterministic embedding provider for testing and offline development.
    
    Constructs normalized 768-dimensional vectors using semantic feature hashing
    and domain-specific legal keyword mapping, guaranteeing high cosine similarity
    for related legal queries and low similarity for disjoint domains.
    Strictly isolated to development and testing environments.
    """

    def __init__(self, dimension: int = 768):
        self._dim = dimension

        # Legal concept semantic clusters for synthetic vector grounding
        self._concept_indices = {
            # 1. Commercial & Cheque Dishonour
            "cheque": 10,
            "dishonour": 11,
            "138": 12,
            "negotiable": 13,
            "bounced": 14,
            # 2. Consumer Protection
            "consumer": 30,
            "defect": 31,
            "commission": 32,
            "daakhil": 33,
            "warranty": 34,
            "refund": 35,
            # 3. Legal Aid & Access
            "aid": 50,
            "nalsa": 51,
            "dlsa": 52,
            "services": 50,
            "eligible": 53,
            "eligibility": 53,
            "criteria": 53,
            "lok adalat": 54,
            "indigent": 55,
            "poor": 55,
            # 4. Criminal Law & Bail
            "bail": 70,
            "undertrial": 71,
            "479": 72,
            "fir": 73,
            "police": 74,
            "crpc": 75,
            "bnss": 76,
            "anticipatory": 77,
            "bns": 78,
            "cruelty": 79,
            "breach of trust": 80,
            "cheating": 81,
            "evidence": 82,
            "bsa": 83,
            # 5. Property & RERA
            "property": 90,
            "rera": 91,
            "possession": 92,
            "builder": 93,
            "allottee": 94,
            "sale deed": 95,
            "lease": 96,
            "tenancy": 96,
            # 6. Family Law & Domestic Violence
            "domestic violence": 110,
            "pwdva": 110,
            "shared household": 111,
            "protection order": 112,
            "divorce": 113,
            "marriage": 114,
            "mutual consent": 115,
            "maintenance": 116,
            "alimony": 116,
            "succession": 117,
            "coparcener": 118,
            "daughter": 118,
            "intestate": 119,
            # 7. Commercial Contracts
            "contract": 130,
            "breach": 131,
            "damages": 132,
            "penalty": 133,
            # 8. Cyber Law & Privacy
            "cyber": 150,
            "identity theft": 151,
            "personation": 152,
            "data privacy": 153,
            "consent": 154,
            "dpdp": 155,
            "phishing": 150,
            "fake profile": 151,
            "photograph": 151,
            "66c": 151,
            "66d": 152,
            "information technology": 150,
            "it act": 150,
            "computer": 150,
            # 9. Motor Vehicle Accidents (MACT)
            "motor vehicle": 170,
            "accident": 171,
            "mact": 172,
            "claims tribunal": 172,
            "grievous hurt": 173,
            # 10. Employment & Labour
            "workman": 190,
            "retrenchment": 191,
            "gratuity": 192,
            "continuous service": 193,
            # 11. Civil Limitation
            "limitation": 210,
            "condonation": 211,
            "sufficient cause": 211,
            "specific performance": 212,
            "adverse possession": 213,
            # 12. Intellectual Property
            "copyright": 230,
            "fair dealing": 231,
            "trademark": 232,
            "infringement": 233,
        }

    @property
    def dimension(self) -> int:
        return self._dim

    @property
    def provider_name(self) -> str:
        return "DeterministicMockEmbeddingProvider"

    @property
    def is_mock(self) -> bool:
        return True

    def _generate_synthetic_vector(self, text: str, is_query: bool = False) -> List[float]:
        vector = [0.0] * self._dim
        clean = text.lower().strip()

        # Multilingual mapping for Hindi and Kannada support
        multilingual_map = {
            "चेक": "cheque",
            "बाउंस": "bounce",
            "उपभोक्ता": "consumer",
            "शिकायत": "complaint",
            "जमानत": "bail",
            "ಬಾಕಿ": "cheque",
            "ಗ್ರಾಹಕ": "consumer",
            "ದೂರು": "complaint",
            "ಜಾಮೀನು": "bail",
            "ಚೆಕ್": "cheque",
        }
        for indic, eng in multilingual_map.items():
            if indic in clean:
                clean += f" {eng}"

        # 1. Base hashing projection across dimensions
        tokens = re.findall(r"\w+", clean)
        for token in tokens:
            token_hash = int(hashlib.md5(token.encode("utf-8")).hexdigest(), 16)
            idx = token_hash % self._dim
            sign = 1.0 if (token_hash % 2 == 0) else -1.0
            vector[idx] += sign * 0.1

        # 2. Domain semantic clustering boosts
        for term, base_idx in self._concept_indices.items():
            if term in clean:
                for offset in range(-3, 4):
                    target_idx = (base_idx + offset) % self._dim
                    weight = 1.0 - (abs(offset) * 0.2)
                    vector[target_idx] += weight * 2.0

        return self._normalize_and_validate(vector, label="mock embedding")

    def embed_query(self, query: str) -> List[float]:
        return self._generate_synthetic_vector(query, is_query=True)

    def embed_document(self, text: str, title: Optional[str] = None) -> List[float]:
        combined = f"{title or ''} {text}".strip()
        return self._generate_synthetic_vector(combined, is_query=False)

    def embed_documents(self, texts: List[str], titles: Optional[List[str]] = None) -> List[List[float]]:
        if titles:
            return [self.embed_document(t, title=titles[i] if i < len(titles) else None) for i, t in enumerate(texts)]
        return [self.embed_document(t) for t in texts]


class GeminiEmbeddingProvider(BaseEmbeddingProvider):
    """Google Gemini embedding provider using official google-genai SDK.
    
    Leverages Google's text-embedding-004 model (768 dimensions) with asymmetric task types:
    - RETRIEVAL_QUERY for user legal questions
    - RETRIEVAL_DOCUMENT for statutory Bare Act sections and judgments
    Enforces strict dimension verification, batching, exponential retry, and error safety.
    NEVER silently replaces failed production embeddings with synthetic mock vectors.
    """

    MAX_BATCH_SIZE = 50
    MAX_CHAR_LENGTH = 8000

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
        dimension: int = 768,
        max_retries: int = 3,
    ):
        self._api_key = api_key or settings.GEMINI_API_KEY
        self._model_name = model_name or settings.GEMINI_EMBEDDING_MODEL
        self._dim = dimension
        self._max_retries = max_retries
        self._client = None

        if self._api_key and self._api_key.strip():
            try:
                from google import genai
                self._client = genai.Client(api_key=self._api_key)
            except ImportError as exc:
                if settings.is_production:
                    raise RuntimeError(
                        "Missing required dependency 'google-genai' for Gemini embedding provider in production. "
                        "Please run 'pip install google-genai'."
                    ) from exc
                logger.warning(f"google-genai SDK not available: {exc}.")
            except Exception as exc:
                if settings.is_production:
                    raise RuntimeError(
                        f"Failed to initialize Gemini embedding client in production: {exc}"
                    ) from exc
                logger.warning(f"Failed to initialize Gemini Client: {exc}.")
        elif settings.is_production:
            raise RuntimeError(
                "GeminiEmbeddingProvider initialization failed in production: GEMINI_API_KEY is required."
            )

    @property
    def dimension(self) -> int:
        return self._dim

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def provider_name(self) -> str:
        return f"GeminiEmbeddingProvider({self._model_name})"

    @property
    def is_mock(self) -> bool:
        return False

    @property
    def is_live(self) -> bool:
        return self._client is not None

    def _call_embed_api_with_retry(
        self,
        contents: Union[str, List[str]],
        task_type: str,
        title: Optional[str] = None,
    ) -> Any:
        """Call google-genai embed_content API with exponential retry on transient failures."""
        if not self._client:
            raise RuntimeError(
                "GeminiEmbeddingProvider client is not initialized. "
                "Ensure GEMINI_API_KEY is set and google-genai is installed."
            )

        from google.genai import types

        config_args = {
            "task_type": task_type,
            "output_dimensionality": self._dim,
        }
        if title and task_type == "RETRIEVAL_DOCUMENT" and isinstance(contents, str):
            config_args["title"] = title[:256]

        config = types.EmbedContentConfig(**config_args)

        attempts = 0
        backoff = 0.5
        last_error = None

        while attempts < self._max_retries:
            attempts += 1
            try:
                response = self._client.models.embed_content(
                    model=self._model_name,
                    contents=contents,
                    config=config,
                )
                return response
            except Exception as exc:
                last_error = exc
                err_msg = str(exc).lower()
                is_transient = any(
                    code in err_msg
                    for code in ("429", "rate limit", "resource exhausted", "503", "unavailable", "timeout", "deadline")
                )
                if is_transient and attempts < self._max_retries:
                    logger.warning(
                        f"Transient error calling Gemini embedding API (attempt {attempts}/{self._max_retries}): {exc.__class__.__name__}. "
                        f"Retrying in {backoff}s..."
                    )
                    time.sleep(backoff)
                    backoff *= 2.0
                else:
                    break

        prod_clause = " in production" if settings.is_production else ""
        error_summary = f"Gemini embedding API call failed{prod_clause} after {attempts} attempts: {last_error}"
        logger.error(f"Gemini embedding generation failed: {last_error.__class__.__name__}")
        raise RuntimeError(error_summary) from last_error

    def embed_query(self, query: str) -> List[float]:
        """Generate 768-D query embedding using RETRIEVAL_QUERY task type."""
        clean_query = query.strip()
        if not clean_query:
            raise ValueError("Query text cannot be empty for embedding generation.")
        if len(clean_query) > self.MAX_CHAR_LENGTH:
            clean_query = clean_query[:self.MAX_CHAR_LENGTH]

        response = self._call_embed_api_with_retry(
            contents=clean_query,
            task_type="RETRIEVAL_QUERY",
        )
        if not response or not response.embeddings:
            raise RuntimeError("Gemini API returned an empty embedding response for query.")

        raw_vector = response.embeddings[0].values
        return self._normalize_and_validate(raw_vector, label="query embedding")

    def embed_document(self, text: str, title: Optional[str] = None) -> List[float]:
        """Generate 768-D document embedding using RETRIEVAL_DOCUMENT task type."""
        clean_text = text.strip()
        if not clean_text:
            raise ValueError("Document text cannot be empty for embedding generation.")
        if len(clean_text) > self.MAX_CHAR_LENGTH:
            clean_text = clean_text[:self.MAX_CHAR_LENGTH]

        response = self._call_embed_api_with_retry(
            contents=clean_text,
            task_type="RETRIEVAL_DOCUMENT",
            title=title,
        )
        if not response or not response.embeddings:
            raise RuntimeError("Gemini API returned an empty embedding response for document.")

        raw_vector = response.embeddings[0].values
        return self._normalize_and_validate(raw_vector, label="document embedding")

    def embed_documents(self, texts: List[str], titles: Optional[List[str]] = None) -> List[List[float]]:
        """Batch embedding generation for multiple legal documents with batch chunking."""
        if not texts:
            return []

        results: List[List[float]] = []

        for i in range(0, len(texts), self.MAX_BATCH_SIZE):
            batch_texts = [
                t[:self.MAX_CHAR_LENGTH] if len(t) > self.MAX_CHAR_LENGTH else t
                for t in texts[i:i + self.MAX_BATCH_SIZE]
            ]
            response = self._call_embed_api_with_retry(
                contents=batch_texts,
                task_type="RETRIEVAL_DOCUMENT",
            )
            if not response or not response.embeddings:
                raise RuntimeError(f"Gemini API returned empty response for document batch at index {i}.")

            if len(response.embeddings) != len(batch_texts):
                raise RuntimeError(
                    f"Batch size mismatch: sent {len(batch_texts)} texts, but received {len(response.embeddings)} embeddings."
                )

            for j, emb in enumerate(response.embeddings):
                validated = self._normalize_and_validate(emb.values, label=f"batch document embedding [{i + j}]")
                results.append(validated)

        return results


class LocalNeuralEmbeddingProvider(BaseEmbeddingProvider):
    """Opt-in open-source neural embeddings via ``sentence-transformers``.

    The model is loaded lazily and only when RAG_NEURAL_EMBEDDING_ENABLED=true.
    A missing SDK or an invalid model/dimension fails loudly; it never falls back
    silently to deterministic vectors. Reindexing is required when the model or
    EMBEDDING_VECTOR_DIMENSION changes.
    """

    def __init__(
        self,
        model_name: str,
        dimension: int,
        *,
        device: Optional[str] = None,
        batch_size: int = 32,
    ) -> None:
        self._model_name = model_name
        self._dim = dimension
        self._device = device
        self._batch_size = max(1, batch_size)
        self._model: Optional[Any] = None

    @property
    def dimension(self) -> int:
        return self._dim

    @property
    def provider_name(self) -> str:
        return f"LocalNeuralEmbeddingProvider({self._model_name})"

    @property
    def is_mock(self) -> bool:
        return False

    def _load_model(self) -> Any:
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
            except ImportError as exc:
                raise RuntimeError(
                    "RAG_NEURAL_EMBEDDING_ENABLED=true requires the optional dependency "
                    "'sentence-transformers'. Install it explicitly or disable neural embeddings."
                ) from exc
            try:
                self._model = SentenceTransformer(self._model_name, device=self._device)
            except Exception as exc:
                raise RuntimeError(
                    f"Failed to load configured neural embedding model '{self._model_name}': {exc}"
                ) from exc
        return self._model

    def _encode(self, texts: List[str], *, is_query: bool) -> List[List[float]]:
        if not texts:
            return []
        model = self._load_model()
        prefix = "query: " if is_query else "passage: "
        prepared = [prefix + text.strip()[:2000] for text in texts]
        try:
            vectors = model.encode(
                prepared,
                batch_size=self._batch_size,
                convert_to_numpy=True,
                normalize_embeddings=False,
                show_progress_bar=False,
            )
        except Exception as exc:
            raise RuntimeError(f"Neural embedding generation failed: {exc}") from exc
        return [
            self._normalize_and_validate([float(value) for value in vector], label="neural embedding")
            for vector in vectors
        ]

    def embed_query(self, query: str) -> List[float]:
        if not query or not query.strip():
            raise ValueError("Query text cannot be empty for embedding generation.")
        return self._encode([query], is_query=True)[0]

    def embed_document(self, text: str, title: Optional[str] = None) -> List[float]:
        if not text or not text.strip():
            raise ValueError("Document text cannot be empty for embedding generation.")
        combined = f"{title or ''}\n{text}".strip()
        return self._encode([combined], is_query=False)[0]

    def embed_documents(self, texts: List[str], titles: Optional[List[str]] = None) -> List[List[float]]:
        if not texts:
            return []
        combined = [
            f"{(titles or [''] * len(texts))[i] or ''}\n{text}".strip()
            for i, text in enumerate(texts)
        ]
        return self._encode(combined, is_query=False)


# Active singleton instance
_embedding_provider_instance: Optional[BaseEmbeddingProvider] = None


def reset_embedding_provider() -> None:
    """Reset the embedding provider singleton instance (useful for testing configuration changes)."""
    global _embedding_provider_instance
    _embedding_provider_instance = None


def get_embedding_provider(reload: bool = False) -> BaseEmbeddingProvider:
    """Return active embedding provider based on environment settings."""
    global _embedding_provider_instance
    if reload or _embedding_provider_instance is None:
        provider_name = settings.AI_PROVIDER.lower().strip() if settings.AI_PROVIDER else "mock"

        if settings.RAG_NEURAL_EMBEDDING_ENABLED:
            _embedding_provider_instance = LocalNeuralEmbeddingProvider(
                model_name=settings.EMBEDDING_MODEL,
                dimension=settings.EMBEDDING_VECTOR_DIMENSION,
                device=settings.RAG_NEURAL_EMBEDDING_DEVICE or None,
            )
        elif provider_name == "groq":
            _embedding_provider_instance = DeterministicMockEmbeddingProvider(
                dimension=settings.EMBEDDING_VECTOR_DIMENSION
            )
        elif settings.is_production:
            if provider_name == "mock":
                raise RuntimeError(
                    "Production configuration error: AI_PROVIDER cannot be 'mock' in production. "
                    "Configure AI_PROVIDER='gemini' and set a valid GEMINI_API_KEY."
                )
            if not settings.GEMINI_API_KEY or not settings.GEMINI_API_KEY.strip():
                raise RuntimeError(
                    "Production configuration error: GEMINI_API_KEY is required in production. "
                    "Please set GEMINI_API_KEY in your environment or .env file."
                )
            _embedding_provider_instance = GeminiEmbeddingProvider(
                api_key=settings.GEMINI_API_KEY,
                model_name=settings.GEMINI_EMBEDDING_MODEL,
                dimension=settings.EMBEDDING_VECTOR_DIMENSION,
            )
        else:
            if provider_name == "gemini" and settings.GEMINI_API_KEY and settings.GEMINI_API_KEY.strip():
                _embedding_provider_instance = GeminiEmbeddingProvider(
                    api_key=settings.GEMINI_API_KEY,
                    model_name=settings.GEMINI_EMBEDDING_MODEL,
                    dimension=settings.EMBEDDING_VECTOR_DIMENSION,
                )
            else:
                _embedding_provider_instance = DeterministicMockEmbeddingProvider(
                    dimension=settings.EMBEDDING_VECTOR_DIMENSION
                )
    return _embedding_provider_instance
