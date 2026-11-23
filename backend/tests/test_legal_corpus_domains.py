"""Cross-domain regression checks against the seeded statutory corpus."""

from app.modules.legal_assistant.retrieval import LegalRetrievalEngine
from app.modules.legal_knowledge.ingestion import LegalIngestionService


async def test_statutory_retrieval_across_domains(db_session, isolated_embedding_provider):
    await LegalIngestionService.seed_curated_corpus(db_session)
    examples = [
        (
            "Do married daughters have equal rights as coparceners in ancestral property under Hindu Succession Act?",
            "Hindu Succession",
            "Section 6",
        ),
        (
            "What certificate is required to submit electronic WhatsApp and computer evidence in court under Bharatiya Sakshya Adhiniyam?",
            "Bharatiya Sakshya",
            None,
        ),
        (
            "What are the requirements for free and informed consent of Data Principal under Digital Personal Data Protection Act?",
            "Digital Personal Data",
            None,
        ),
        (
            "Is an employee who resigned after 5 years of continuous service entitled to payment of gratuity?",
            "Payment of Gratuity",
            "Section 4",
        ),
        (
            "Can a court condone delay in filing an appeal if there was sufficient cause under Limitation Act Section 5?",
            "Limitation Act",
            "Section 5",
        ),
        (
            "What constitutes infringement of a registered trade mark by a deceptively similar mark in trade under Trade Marks Act?",
            "Trade Marks Act",
            "Section 29",
        ),
        (
            "Is an award passed by Lok Adalat appealable and is court fee refunded under Legal Services Authorities Act?",
            "Legal Services Authorities",
            "21",
        ),
    ]
    for query, title, section in examples:
        chunks = await LegalRetrievalEngine.retrieve(
            db=db_session, query=query, jurisdiction="Union of India", max_sources=3,
        )
        assert any(
            title in chunk["source_title"]
            and (section is None or section in chunk["section_number"])
            for chunk in chunks
        ), f"Expected {title} {section or ''} for {query}"
