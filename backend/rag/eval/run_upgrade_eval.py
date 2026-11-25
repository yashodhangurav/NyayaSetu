"""Deterministic, offline evaluation harness for the upgraded RAG pipeline.

The harness runs the generated (non-human-verified) test set through the immutable
bundled corpus and the deterministic grounded provider. It records reproducible
operational metrics and explicitly labels the evidence set as unverified. No live
LLM, search engine, or official website is contacted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.core.config import settings
from app.modules.legal_assistant.citation_validator import CitationValidator
from app.modules.legal_assistant.embedding_provider import get_embedding_provider
from app.modules.legal_assistant.llm_provider import DeterministicGroundedLLMProvider
from rag.search.hybrid_search import LegalHybridSearchEngine

DEFAULT_TESTSET = Path(__file__).with_name("testset.jsonl")
DEFAULT_REPORT = Path(__file__).with_name("latest_upgrade_report.json")


def _corpus_fingerprint(path: Path) -> str:
    if not path.exists():
        return "MISSING"
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_items(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _expected_hit(item: Dict[str, Any], results: List[Dict[str, Any]]) -> int:
    expected = [str(section).casefold() for section in item.get("expected_sections", [])]
    if not expected:
        return 0
    for rank, chunk in enumerate(results, start=1):
        haystack = " ".join(
            str(chunk.get(key) or "").casefold() for key in ("section", "citation", "act")
        )
        if any(section in haystack for section in expected):
            return rank
    return 0


def _as_generation_chunks(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        {
            "source_title": c.get("act", "Indian Statute"),
            "source_type": c.get("doc_type", "BARE_ACT"),
            "act_or_judgment_identifier": c.get("source_id"),
            "section_number": c.get("section", ""),
            "clause_heading": c.get("clause_heading", ""),
            "chunk_text": c.get("chunk_text", ""),
            "relevant_text": (c.get("chunk_text") or "")[:280],
            "official_source_url": c.get("source_url"),
            "content_checksum": c.get("content_checksum") or c.get("chunk_id"),
            "jurisdiction": c.get("jurisdiction", "Union of India"),
        }
        for c in results
    ]


def evaluate(
    testset_path: Path = DEFAULT_TESTSET,
    report_path: Optional[Path] = None,
    *,
    top_k: int = 5,
    limit: Optional[int] = None,
) -> Dict[str, Any]:
    items = _load_items(Path(testset_path))
    if limit:
        items = items[:limit]

    engine = LegalHybridSearchEngine()
    provider = DeterministicGroundedLLMProvider()
    corpus_path = Path("rag/data/processed/canonical_corpus.json")
    embedding = get_embedding_provider()

    hits_at_1 = hits_at_3 = hits_at_5 = in_scope = 0
    reciprocal_ranks: List[float] = []
    out_of_scope_total = out_of_scope_correct = 0
    repealed_leakage = 0
    verified_citations = unverified_citations = 0
    supported_claims = unsupported_claims = 0
    answers_with_sources = 0
    per_language: Dict[str, Dict[str, float]] = defaultdict(
        lambda: {"total": 0, "hits_at_5": 0, "mrr": 0.0}
    )

    for item in items:
        search = engine.search(
            query=item["query"], filter_in_force_only=True, top_k=top_k
        )
        results = search.get("results", []) or []
        repealed_leakage += sum(1 for c in results if c.get("in_force") is False)
        lang = str(item.get("lang", "unknown"))

        if item.get("topic") == "out_of_scope":
            out_of_scope_total += 1
            if not results or search.get("confidence_level") in {"LOW", "NO_MATCH"}:
                out_of_scope_correct += 1
            continue

        in_scope += 1
        per_language[lang]["total"] += 1
        hit = _expected_hit(item, results)
        if hit:
            hits_at_1 += int(hit == 1)
            hits_at_3 += int(hit <= 3)
            hits_at_5 += int(hit <= 5)
            per_language[lang]["hits_at_5"] += 1
        rr = 1.0 / hit if hit else 0.0
        reciprocal_ranks.append(rr)
        per_language[lang]["mrr"] += rr

        chunks = _as_generation_chunks(results)
        llm_output = provider.generate_legal_answer(item["query"], chunks)
        citations, pruned = CitationValidator.validate_and_filter_citations(
            answer_text=llm_output.get("answer", ""),
            claimed_references=llm_output.get("cited_references", []),
            retrieved_chunks=chunks,
        )
        verified_citations += len(citations)
        unverified_citations += len(pruned)
        supported, unsupported, _ = CitationValidator.verify_claim_support(
            llm_output.get("answer", ""), chunks
        )
        supported_claims += len(supported)
        unsupported_claims += len(unsupported)
        answers_with_sources += int(bool(chunks and citations))

    def recall(n: int) -> float:
        hit_count = {1: hits_at_1, 3: hits_at_3, 5: hits_at_5}.get(n, 0)
        return hit_count / in_scope if in_scope else 0.0

    report: Dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "evidence_set": {
            "path": str(testset_path),
            "items": len(items),
            "human_verified": False,
            "warning": (
                "This generated set is a regression signal only. It is not legal "
                "ground truth and cannot establish legal answer accuracy."
            ),
        },
        "configuration": {
            "corpus_path": str(corpus_path),
            "corpus_sha256": _corpus_fingerprint(corpus_path),
            "embedding_provider": getattr(embedding, "provider_name", type(embedding).__name__),
            "embedding_dimension": getattr(embedding, "dimension", None),
            "generation_provider": provider.provider_name,
            "top_k": top_k,
            "environment": settings.ENVIRONMENT,
            "neural_embedding_enabled": settings.RAG_NEURAL_EMBEDDING_ENABLED,
            "source_fetch_enabled": settings.RAG_SOURCE_FETCH_ENABLED,
            "official_fallback_enabled": settings.RAG_OFFICIAL_FALLBACK_ENABLED,
            "evidence_min_score": settings.RAG_EVIDENCE_MIN_SCORE,
            "evidence_min_chunks": settings.RAG_EVIDENCE_MIN_CHUNKS,
        },
        "retrieval": {
            "in_scope_queries": in_scope,
            "recall_at_1": round(recall(1), 4),
            "recall_at_3": round(recall(3), 4),
            "recall_at_5": round(recall(5), 4),
            "mrr_at_5": round(sum(reciprocal_ranks) / in_scope if in_scope else 0.0, 4),
            "out_of_scope_total": out_of_scope_total,
            "out_of_scope_correct": out_of_scope_correct,
            "repealed_leakage_count": repealed_leakage,
        },
        "grounding": {
            "verified_citations": verified_citations,
            "unverified_citations_pruned": unverified_citations,
            "supported_claims": supported_claims,
            "unsupported_claims": unsupported_claims,
            "claim_support_ratio": round(
                supported_claims / (supported_claims + unsupported_claims)
                if supported_claims + unsupported_claims else 1.0,
                4,
            ),
            "answers_with_sources": answers_with_sources,
        },
        "per_language": {
            lang: {
                "total": int(data["total"]),
                "recall_at_5": round(data["hits_at_5"] / data["total"], 4) if data["total"] else 0.0,
                "mrr_at_5": round(data["mrr"] / data["total"], 4) if data["total"] else 0.0,
            }
            for lang, data in sorted(per_language.items())
        },
        "quality_gate": {
            "passed": False,
            "reason": (
                "No human-verified legal ground truth is available; this harness does "
                "not certify legal accuracy. Numeric results are regression evidence only."
            ),
        },
    }

    target = Path(report_path) if report_path else DEFAULT_REPORT
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Run offline RAG regression evaluation")
    parser.add_argument("--testset", type=Path, default=DEFAULT_TESTSET)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    report = evaluate(args.testset, args.report, top_k=args.top_k, limit=args.limit)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"\nReport written to {args.report}")


if __name__ == "__main__":
    main()
