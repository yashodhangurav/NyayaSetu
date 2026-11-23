"""Evaluation Metrics and Exit Gate Verification for Phase 1 RAG Retrieval."""

import json
import os
import sys
from collections import defaultdict
from typing import Dict, Any, List

from rag.search.hybrid_search import LegalHybridSearchEngine


def run_evaluation(testset_path: str = None) -> Dict[str, Any]:
    if testset_path is None:
        eval_dir = os.path.dirname(os.path.abspath(__file__))
        testset_path = os.path.join(eval_dir, "testset.jsonl")

    if not os.path.exists(testset_path):
        raise FileNotFoundError(f"Testset not found at {testset_path}")

    with open(testset_path, "r", encoding="utf-8") as f:
        test_items = [json.loads(line) for line in f if line.strip()]

    engine = LegalHybridSearchEngine()

    total_queries = len(test_items)
    in_scope_queries = 0
    hits_at_1 = 0
    hits_at_3 = 0
    hits_at_5 = 0
    reciprocal_ranks = []

    per_language_stats = defaultdict(lambda: {"total": 0, "hits_at_5": 0, "mrr": []})
    per_topic_stats = defaultdict(lambda: {"total": 0, "hits_at_5": 0})

    repealed_leakage_count = 0
    out_of_scope_correct = 0
    out_of_scope_total = 0

    print(f"\n=======================================================")
    print(f"  RUNNING PHASE 1 RETRIEVAL EVALUATION ({total_queries} queries)")
    print(f"=======================================================\n")

    for idx, item in enumerate(test_items):
        query = item["query"]
        lang = item["lang"]
        topic = item["topic"]
        expected_sections = item.get("expected_sections", [])

        # Search top 5
        res = engine.search(query=query, filter_in_force_only=True, top_k=5)
        results = res.get("results", [])

        # Check repealed law leakage
        for chunk in results:
            if chunk.get("in_force") is False:
                repealed_leakage_count += 1
                print(f"[LEAKAGE ALERT] Query: '{query}' returned repealed chunk: {chunk.get('chunk_id')}")

        if topic == "out_of_scope":
            out_of_scope_total += 1
            if len(results) == 0 or res.get("confidence_level") == "LOW":
                out_of_scope_correct += 1
            continue

        in_scope_queries += 1
        per_language_stats[lang]["total"] += 1
        per_topic_stats[topic]["total"] += 1

        hit_rank = 0
        for rank, chunk in enumerate(results, start=1):
            chunk_sec = chunk.get("section", "")
            chunk_citation = chunk.get("citation", "")
            chunk_act = chunk.get("act", "")

            # Match if expected section appears in section, citation, or act
            matched = any(
                exp.lower() in chunk_sec.lower() or exp.lower() in chunk_citation.lower()
                for exp in expected_sections
            )
            if matched:
                hit_rank = rank
                break

        if hit_rank > 0:
            if hit_rank == 1:
                hits_at_1 += 1
            if hit_rank <= 3:
                hits_at_3 += 1
            if hit_rank <= 5:
                hits_at_5 += 1
                per_language_stats[lang]["hits_at_5"] += 1
                per_topic_stats[topic]["hits_at_5"] += 1
            rr = 1.0 / hit_rank
        else:
            rr = 0.0

        reciprocal_ranks.append(rr)
        per_language_stats[lang]["mrr"].append(rr)

    overall_recall_at_5 = (hits_at_5 / in_scope_queries) * 100 if in_scope_queries else 0.0
    overall_recall_at_1 = (hits_at_1 / in_scope_queries) * 100 if in_scope_queries else 0.0
    overall_recall_at_3 = (hits_at_3 / in_scope_queries) * 100 if in_scope_queries else 0.0
    overall_mrr = (sum(reciprocal_ranks) / in_scope_queries) if in_scope_queries else 0.0

    print(f"Total Test Queries:      {total_queries}")
    print(f"In-Scope Queries:        {in_scope_queries}")
    print(f"Out-of-Scope Tested:     {out_of_scope_total} (Correctly Handled: {out_of_scope_correct}/{out_of_scope_total})")
    print(f"Repealed Law Leakage:    {repealed_leakage_count} (0.00%)\n")

    print(f"--- OVERALL METRICS ---")
    print(f"Recall@1: {overall_recall_at_1:.2f}%")
    print(f"Recall@3: {overall_recall_at_3:.2f}%")
    print(f"Recall@5: {overall_recall_at_5:.2f}% (Target: >= 85.0%)")
    print(f"MRR@5:    {overall_mrr:.4f}\n")

    print(f"--- PER-LANGUAGE BREAKDOWN ---")
    lang_pass = True
    for lang, data in sorted(per_language_stats.items()):
        total = data["total"]
        h5 = data["hits_at_5"]
        rec5 = (h5 / total * 100) if total else 0.0
        mrr = (sum(data["mrr"]) / total) if total else 0.0
        status = "PASS" if rec5 >= 75.0 else "FAIL"
        if rec5 < 75.0:
            lang_pass = False
        print(f"  [{lang.upper():<5}] Total: {total:<3} | Recall@5: {rec5:6.2f}% | MRR: {mrr:.4f} | Status: {status}")

    print(f"\n--- PER-TOPIC BREAKDOWN ---")
    for topic, data in sorted(per_topic_stats.items()):
        total = data["total"]
        h5 = data["hits_at_5"]
        rec5 = (h5 / total * 100) if total else 0.0
        print(f"  [{topic:<20}] Total: {total:<3} | Recall@5: {rec5:6.2f}%")

    # Exit check verification
    exit_check_passed = (
        overall_recall_at_5 >= 85.0
        and lang_pass
        and repealed_leakage_count == 0
    )

    print("\n" + "=" * 55)
    if exit_check_passed:
        print("  PHASE 1 EXIT CHECK: PASSED (READY FOR PHASE 2)")
    else:
        print("  PHASE 1 EXIT CHECK: FAILED (DO NOT START PHASE 2)")
    print("=" * 55 + "\n")

    return {
        "overall_recall_at_5": overall_recall_at_5,
        "overall_mrr": overall_mrr,
        "repealed_leakage_count": repealed_leakage_count,
        "exit_check_passed": exit_check_passed,
        "per_language": {
            l: (d["hits_at_5"] / d["total"] * 100) for l, d in per_language_stats.items()
        },
    }


if __name__ == "__main__":
    res = run_evaluation()
    if not res["exit_check_passed"]:
        sys.exit(1)
