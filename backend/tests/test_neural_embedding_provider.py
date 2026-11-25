"""Tests for opt-in neural embedding provider configuration."""

import sys
import types

import pytest

from app.core.config import settings
from app.modules.legal_assistant.embedding_provider import (
    LocalNeuralEmbeddingProvider,
    get_embedding_provider,
    reset_embedding_provider,
)


class _FakeModel:
    def __init__(self, dimension: int = 3):
        self.dimension = dimension
        self.calls = []

    def encode(self, texts, **kwargs):
        self.calls.append(list(texts))
        return [[0.6, 0.8] + [0.0] * (self.dimension - 2) for _ in texts]


def _install_fake_model(monkeypatch, model):
    module = types.ModuleType("sentence_transformers")

    class SentenceTransformer:
        def __init__(self, model_name, device=None):
            self.model_name = model_name
            self.device = device

        def encode(self, texts, **kwargs):
            return model.encode(texts, **kwargs)

    module.SentenceTransformer = SentenceTransformer
    monkeypatch.setitem(sys.modules, "sentence_transformers", module)


def test_neural_provider_uses_query_and_passage_prefixes(monkeypatch):
    model = _FakeModel()
    _install_fake_model(monkeypatch, model)
    provider = LocalNeuralEmbeddingProvider("fake/model", dimension=3)

    assert provider.is_mock is False
    assert provider.embed_query("cheque bounce")[0] > 0
    provider.embed_documents(["Section 138", "Consumer complaint"], titles=["NI Act", "CPA"])
    assert model.calls[0][0].startswith("query: ")
    assert all(text.startswith("passage: ") for text in model.calls[1])


def test_neural_provider_rejects_dimension_mismatch(monkeypatch):
    model = _FakeModel(dimension=2)
    _install_fake_model(monkeypatch, model)
    provider = LocalNeuralEmbeddingProvider("fake/model", dimension=3)
    with pytest.raises(ValueError, match="dimension mismatch"):
        provider.embed_query("test query")


def test_factory_honors_neural_opt_in(monkeypatch):
    model = _FakeModel()
    _install_fake_model(monkeypatch, model)
    monkeypatch.setattr(settings, "RAG_NEURAL_EMBEDDING_ENABLED", True)
    monkeypatch.setattr(settings, "EMBEDDING_MODEL", "fake/model")
    monkeypatch.setattr(settings, "EMBEDDING_VECTOR_DIMENSION", 3)
    reset_embedding_provider()
    try:
        provider = get_embedding_provider()
        assert isinstance(provider, LocalNeuralEmbeddingProvider)
        assert provider.provider_name == "LocalNeuralEmbeddingProvider(fake/model)"
    finally:
        reset_embedding_provider()
