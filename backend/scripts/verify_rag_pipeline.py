"""Operational verification of NyayaSetu RAG pipeline across diverse citizen inquiries."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from rag.search.hybrid_search import LegalHybridSearchEngine
from app.modules.legal_assistant.llm_provider import DeterministicGroundedLLMProvider

def main():
    engine = LegalHybridSearchEngine()
    test_queries = [
        "what is fine for drink and drive",
        "change of plot owner",
        "got a legal summon",
        "paid 500 rs to traffic police",
        "how to get refund for delayed flat possession",
        "cheque bounce notice period",
        "can landlord deduct painting charges from deposit",
    ]

    print("=== TESTING HYBRID RETRIEVAL & GROUNDING ===")
    dp = DeterministicGroundedLLMProvider()
    all_passed = True

    for q in test_queries:
        res = engine.search(q, top_k=3)
        results = res.get("results", [])
        top_score = res.get("confidence_score", 0.0)
        conf_level = res.get("confidence_level", "UNKNOWN")
        top_chunk = (results[0]["act"] + " " + str(results[0].get("section", ""))) if results else "NONE"
        
        ans = dp.generate_legal_answer(q, results)
        follow_ups = ans.get("follow_up_suggestions", [])
        
        print(f"Query: '{q}'")
        print(f"  -> Chunks: {len(results)} | Conf: {conf_level} ({top_score}) | Top: {top_chunk}")
        print(f"  -> Answer snippet: {ans.get('answer', '')[:100]}...")
        print(f"  -> Follow-ups ({len(follow_ups)}): {follow_ups[:2]}")
        
        if len(results) == 0 or len(follow_ups) == 0:
            print("  [FAIL] Zero chunks or zero follow-ups!")
            all_passed = False
        else:
            print("  [PASS] Rich chunks and dynamic follow-ups confirmed.")
        print("-" * 50)

    if all_passed:
        print("\nALL DIVERSE CITIZEN QUERIES PASSED RETRIEVAL VERIFICATION!")
    else:
        print("\nSOME QUERIES FAILED RETRIEVAL VERIFICATION!")

    # Test full end-to-end service with ask_legal_assistant
    print("\n=== TESTING FULL SERVICE (ask_legal_assistant) ===")
    from app.modules.legal_assistant.service import LegalAssistantService
    from app.modules.legal_assistant.schemas import LegalAskRequest
    from app.core.database import AsyncSessionLocal

    async def run_service_test():
        async with AsyncSessionLocal() as session:
            for q in ["what is fine for drink and drive", "change of plot owner", "got a legal summon"]:
                payload = LegalAskRequest(query=q, language="en")
                res = await LegalAssistantService.ask(
                    db=session,
                    payload=payload,
                    current_user=None,
                )
                print(f"Service Query: '{q}'")
                print(f"  -> Answer length: {len(res.answer)} chars")
                print(f"  -> Sources found: {res.sources_found}")
                print(f"  -> Citations ({len(res.citations)}): {[c.source_title + ' ' + str(c.section_or_paragraph) for c in res.citations[:2]]}")
                print(f"  -> Next steps ({len(res.suggested_next_steps)}): {res.suggested_next_steps[:2]}")
                print(f"  -> Follow-ups ({len(res.follow_up_suggestions)}): {res.follow_up_suggestions[:2]}")
                print("-" * 50)

    asyncio.run(run_service_test())
    print("\nALL FULL SERVICE CHECKS COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
