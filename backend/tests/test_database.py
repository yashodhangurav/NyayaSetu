"""Database column contracts for PostGIS and pgvector."""


from app.core.config import settings
from app.core.models import AdvocateProfile, LegalChunk


def test_advocate_profile_has_postgis_geography():
    """Verify that AdvocateProfile location column is configured with Geography POINT."""
    col = AdvocateProfile.__table__.c.location
    assert col is not None
    # Check type name matches Geography
    assert "GEOGRAPHY" in str(col.type).upper()


def test_legal_chunk_embedding_vector_dimension():
    """Verify that LegalChunk has configurable Vector dimension from settings."""
    col = LegalChunk.__table__.c.embedding
    assert col is not None
    assert "VECTOR" in str(col.type).upper()
    assert col.type.dim == settings.EMBEDDING_VECTOR_DIMENSION
