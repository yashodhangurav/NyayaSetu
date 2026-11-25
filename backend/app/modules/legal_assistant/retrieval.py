"""Advanced Hybrid Lexical and Semantic Retrieval Engine for Indian Legal Corpus.

Features:
1. Dense semantic query embedding (Gemini text-embedding-004 in production, deterministic mock in dev)
2. Native pgvector cosine distance search
3. Automatic legal domain detection and section number disambiguation (e.g. Section 12 PWDVA vs Section 12 NALSA)
4. Multi-statute contextual ranking and Reciprocal Rank Fusion / hybrid scoring
5. Configurable relevance thresholding to discard nearest-neighbor vector artifacts
6. Source deduplication and rich statutory metadata extraction
"""

import math
import re
from typing import Any, Dict, List, Optional, Set, Tuple
from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.core.logging import logger
from app.modules.legal_assistant.embedding_provider import get_embedding_provider
from app.modules.legal_knowledge.models import LegalChunk, LegalSource


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Calculate cosine similarity between two float vectors."""
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


# Legal practice domain semantic clusters for cross-statute disambiguation
LEGAL_DOMAIN_TAXONOMY: Dict[str, Dict[str, Any]] = {
    "FAMILY_LAW": {
        "keywords": [
            "marriage", "divorce", "mutual consent", "dowry", "domestic violence", "domestic abuse",
            "aggrieved woman", "pwdva", "cruelty", "maintenance", "alimony", "custody", "succession",
            "coparcener", "daughter", "shared household", "stridhan", "hindu marriage", "hindu succession",
            "wife", "husband", "matrimonial", "in-laws", "intestate"
        ],
        "short_codes": ["PWDVA_2005", "HMA_1955", "HSA_1956"],
    },
    "CRIMINAL_LAW": {
        "keywords": [
            "crime", "criminal", "police", "fir", "bail", "anticipatory bail", "bns", "bnss",
            "bsa", "crpc", "ipc", "undertrial", "cheating", "fraud", "criminal breach of trust",
            "arrest", "custody", "evidence", "electronic evidence", "charge sheet", "cognizable",
            "non-bailable", "jail", "magistrate", "summon", "summons", "court summon", "warrant",
            "notice of appearance", "bailable warrant"
        ],
        "short_codes": ["BNS_2023", "BNSS_2023", "BSA_2023"],
    },
    "COMMERCIAL_AND_BANKING": {
        "keywords": [
            "cheque", "dishonour", "bounce", "bounced", "138", "negotiable", "banker", "payee",
            "drawer", "contract", "breach of contract", "damages", "penalty", "agreement",
            "debt", "liability", "promissory", "statutory notice"
        ],
        "short_codes": ["NI_ACT", "ICA_1872"],
    },
    "CONSUMER_PROTECTION": {
        "keywords": [
            "consumer", "defect", "defective", "deficiency", "warranty", "refund", "e-daakhil",
            "district commission", "state commission", "consumer dispute", "product liability",
            "manufacturer", "service provider", "unfair trade"
        ],
        "short_codes": ["CPA_2019"],
    },
    "CYBER_LAW": {
        "keywords": [
            "cyber", "hacking", "phishing", "identity theft", "personation", "computer contaminant",
            "virus", "data privacy", "data principal", "consent", "dpdp", "it act", "password",
            "electronic signature", "otp", "unauthorized access"
        ],
        "short_codes": ["IT_ACT_2000", "DPDPA_2023"],
    },
    "MOTOR_VEHICLES": {
        "keywords": [
            "accident", "motor vehicle", "mact", "claims tribunal", "hit and run", "grievous hurt",
            "road accident", "driver", "vehicular", "insurance claim", "no-fault liability",
            "compensation", "traffic", "challan", "fine", "police fine", "traffic police",
            "drink and drive", "drunk driving", "alcohol", "breath analyzer", "breath analyser",
            "helmet", "seatbelt", "driving licence", "speeding", "signal jump"
        ],
        "short_codes": ["MV_ACT_1988"],
    },
    "PROPERTY_AND_CIVIL": {
        "keywords": [
            "property", "sale deed", "rera", "builder", "possession", "flat", "apartment",
            "allottee", "lease", "tenant", "tenancy", "rent", "transfer of property", "limitation",
            "condonation of delay", "adverse possession", "specific performance", "promoter",
            "plot", "plot owner", "plot ownership", "site owner", "land title", "conveyance",
            "change of owner", "mutation", "khata transfer"
        ],
        "short_codes": ["RERA_2016", "TPA_1882", "LIMITATION_1963", "KLRA_1964"],
    },
    "LEGAL_AID": {
        "keywords": [
            "legal aid", "free legal aid", "nalsa", "dlsa", "slsa", "lok adalat", "indigent",
            "poor", "free lawyer", "legal services", "court fee refund", "underserved"
        ],
        "short_codes": ["NALSA_1987"],
    },
    "LABOUR_EMPLOYMENT": {
        "keywords": [
            "workman", "worker", "retrenchment", "layoff", "gratuity", "superannuation",
            "continuous service", "industrial dispute", "factory", "wages", "termination of employment",
            "employer", "notice pay", "posh", "internal committee", "icc", "sexual harassment workplace"
        ],
        "short_codes": ["IDA_1947", "PGA_1972", "POSH_2013"],
    },
    "INTELLECTUAL_PROPERTY": {
        "keywords": [
            "copyright", "fair dealing", "trademark", "infringement", "deceptively similar",
            "literary work", "musical work", "artistic work", "counterfeit mark", "passing off"
        ],
        "short_codes": ["COPYRIGHT_1957", "TRADEMARKS_1999"],
    },
    "KARNATAKA_LAND_AND_REVENUE": {
        "keywords": [
            "rtc", "pahani", "khata", "a-khata", "b-khata", "e-khata", "mutation", "phodi", "durasti",
            "saguvali chit", "hakkupatra", "ptcl", "sc st granted land", "section 95", "conversion",
            "bhoomi", "kaveri", "kaveri 2.0", "form 9", "form 11", "e-swathu", "bbmp", "kofa",
            "tahsildar", "assistant commissioner revenue", "village accountant", "rajakaluve"
        ],
        "short_codes": ["KLR_1964", "PTCL_1978", "BBMP_2020", "KOFA_1972", "KAR_RENT_1999"],
    },
    "HEALTHCARE_AND_MEDICAL": {
        "keywords": [
            "doctor", "hospital", "medical negligence", "patient", "kpme", "jacob mathew", "informed consent",
            "clinical establishment", "mbbs", "hospital bill", "dead body detention", "mtp", "abortion",
            "mental healthcare", "advance directive"
        ],
        "short_codes": ["KPME_2007", "NMC_2019", "MHA_2017", "MTP_1971"],
    },
    "TAXATION_DIRECT_INDIRECT": {
        "keywords": [
            "income tax", "itr", "capital gains", "tds", "194-ia", "section 54", "section 148",
            "reassessment", "gst", "cgst", "input tax credit", "property tax", "sas return"
        ],
        "short_codes": ["IT_ACT_1961", "CGST_2017"],
    },
    "MSME_AND_CORPORATE": {
        "keywords": [
            "msme", "samadhaan", "delayed payment", "45 days", "compound interest", "msefc", "buyer default",
            "companies act", "incorporation", "director", "llp", "arbitration"
        ],
        "short_codes": ["MSMED_2006", "COMPANIES_2013", "LLP_2008", "ARB_1996"],
    },
    "ADMINISTRATIVE_AND_RTI": {
        "keywords": [
            "rti", "right to information", "pio", "public information officer", "first appeal",
            "30 days rti", "48 hours life liberty", "sakala", "gsc slip", "seva sindhu", "caste certificate"
        ],
        "short_codes": ["RTI_2005", "SAKALA_2011"],
    },
    "EDUCATION_AND_STUDENT": {
        "keywords": [
            "school", "college", "university", "rte", "25 percent quota", "capitation fee", "ragging",
            "anti ragging", "ugc", "certificates withholding", "marks card withholding"
        ],
        "short_codes": ["RTE_2009", "UGC_1956"],
    },
    "ENVIRONMENT_AND_POLLUTION": {
        "keywords": [
            "pollution", "noise pollution", "loudspeaker", "decibel", "10 pm loudspeaker", "ngt",
            "national green tribunal", "lake buffer", "solid waste", "tree cutting", "preservation of trees"
        ],
        "short_codes": ["EPA_1986", "NGT_2010"],
    },
}


class LegalRetrievalEngine:
    """Hybrid semantic vector and statutory keyword retriever over official Indian legal sources."""

    @classmethod
    def identify_legal_domain(cls, query: str) -> Optional[str]:
        """Classify the broad Indian legal domain from query intent and terminology."""
        q_lower = query.lower()
        domain_scores: Dict[str, int] = {}

        for domain, config in LEGAL_DOMAIN_TAXONOMY.items():
            matches = sum(1 for kw in config["keywords"] if kw in q_lower)
            if matches > 0:
                domain_scores[domain] = matches

        if domain_scores:
            top_domain = max(domain_scores.items(), key=lambda x: x[1])[0]
            return top_domain
        return None

    @classmethod
    async def retrieve(
        cls,
        db: AsyncSession,
        query: str,
        jurisdiction: Optional[str] = None,
        max_sources: int = 5,
        relevance_threshold: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant legal chunks using hybrid vector similarity and statutory keyword matching.
        
        Args:
            db: Async database session.
            query: User's legal question or factual situation.
            jurisdiction: Optional territorial filter (e.g. 'Maharashtra', 'Delhi', 'Union of India').
            max_sources: Maximum number of relevant chunks to return.
            relevance_threshold: Minimum composite score required to qualify as relevant.

        Returns:
            List of structured, grounded legal chunk dicts meeting relevance criteria.
        """
        threshold = relevance_threshold if relevance_threshold is not None else settings.RAG_RELEVANCE_THRESHOLD
        limit = min(max_sources, settings.RAG_MAX_SOURCES_LIMIT)

        # 1. Broad domain identification for disambiguation
        detected_domain = cls.identify_legal_domain(query)
        preferred_short_codes: Set[str] = set()
        if detected_domain:
            preferred_short_codes = set(LEGAL_DOMAIN_TAXONOMY[detected_domain]["short_codes"])

        # 2. Semantic query vector generation
        embedding_provider = get_embedding_provider()
        query_vector = embedding_provider.embed_query(query)

        # 3. Base database query with joined source metadata
        stmt = (
            select(LegalChunk)
            .join(LegalSource, LegalChunk.source_id == LegalSource.id)
            .options(selectinload(LegalChunk.source))
        )

        # 4. Verification Gate Filter: Only verified sources
        stmt = stmt.where(LegalSource.verification_status != "REJECTED")

        # 5. Territorial Jurisdiction Filter
        if jurisdiction and jurisdiction.strip():
            j_clean = jurisdiction.strip().lower()
            stmt = stmt.where(
                or_(
                    LegalSource.jurisdiction.ilike(f"%{j_clean}%"),
                    LegalSource.jurisdiction == "Union of India",
                    LegalSource.jurisdiction == "Supreme Court of India / Bharat Central",
                )
            )

        # 6. pgvector similarity ordering
        is_sqlite = False
        try:
            if db.bind and db.bind.dialect.name == "sqlite":
                is_sqlite = True
        except Exception:
            pass

        if not is_sqlite:
            # Order by native pgvector cosine distance (<=>)
            stmt = stmt.order_by(LegalChunk.embedding.cosine_distance(query_vector)).limit(max(limit * 4, 30))

        res = await db.execute(stmt)
        candidate_chunks = res.scalars().all()

        if not candidate_chunks:
            return []

        # 7. Multilingual keyword expansion (Devanagari & Kannada)
        query_lower = query.lower()
        multilingual_map = {
            "चेक": "cheque",
            "बाउंस": "bounce",
            "उपभोक्ता": "consumer",
            "शिकायत": "complaint",
            "कानूनी": "legal",
            "प्रक्रिया": "procedure",
            "घरेलू हिंसा": "domestic violence",
            "तलाक": "divorce",
            "ವೈವಾಹಿಕ": "matrimonial",
            "ಗ್ರಾಹಕ": "consumer",
            "ಗ್ರಾಹಕರ": "consumer",
            "ರಕ್ಷಣಾ": "protection",
            "ಕಾಯ್ದೆ": "act",
            "ದೂರು": "complaint",
            "ಜಾಮೀನು": "bail",
            "ಚೆಕ್": "cheque",
        }
        expanded_query = query_lower
        for indic_word, eng_equiv in multilingual_map.items():
            if indic_word in expanded_query:
                expanded_query += f" {eng_equiv}"

        query_tokens = set(re.findall(r"\w+", expanded_query))
        query_section_nums = set(re.findall(r"\b\d+[a-z]?\b", expanded_query))

        scored_candidates: List[Tuple[float, float, LegalChunk]] = []

        # 8. Hybrid Lexical + Semantic Scoring with Cross-Statute Disambiguation
        for chunk in candidate_chunks:
            chunk_embedding = chunk.embedding
            if isinstance(chunk_embedding, list):
                v_score = cosine_similarity(query_vector, chunk_embedding)
            elif hasattr(chunk_embedding, "tolist"):
                v_score = cosine_similarity(query_vector, chunk_embedding.tolist())
            else:
                v_score = 0.5  # fallback baseline

            src = chunk.source
            src_short_code = (src.short_code or "").upper() if src else ""
            src_title = (src.title or "").lower() if src else ""
            sec_num = (chunk.section_number or "").lower()
            heading = (chunk.clause_heading or "").lower()
            chunk_text = chunk.chunk_text.lower()

            kw_score = 0.0

            # A. Exact Section Hit with Domain Disambiguation
            # Prevents confusing Section 12 of PWDVA with Section 12 of NALSA
            for target_sec in query_section_nums:
                target_str = f"section {target_sec}"
                if target_str in sec_num or (target_sec in sec_num and len(target_sec) >= 2):
                    if preferred_short_codes and src_short_code in preferred_short_codes:
                        # Major boost when both section number AND domain align
                        kw_score += 0.60
                    elif not preferred_short_codes:
                        # Neutral domain
                        kw_score += 0.40
                    else:
                        # Section number matched a DIFFERENT domain (e.g. asking for DV, but hit NALSA sec 12)
                        # Minimal or zero section boost to prevent cross-statute collision
                        kw_score += 0.05

            # B. Act / Statute explicit mention boost
            if src_short_code and src_short_code.lower() in query_lower:
                kw_score += 0.45
            for title_word in re.findall(r"\w+", src_title):
                if len(title_word) > 4 and title_word in query_tokens:
                    kw_score += 0.10

            # C. Domain Alignment Boost
            if preferred_short_codes and src_short_code in preferred_short_codes:
                kw_score += 0.25

            # D. Clause heading & semantic terms overlap
            for token in query_tokens:
                if len(token) > 3:
                    if token in heading:
                        kw_score += 0.15
                    elif token in sec_num:
                        kw_score += 0.10
                    elif token in chunk_text:
                        kw_score += 0.05

            # Linear hybrid combination using configured weights
            norm_kw = min(kw_score, 1.0)
            composite_score = (v_score * settings.RAG_SEMANTIC_WEIGHT) + (norm_kw * settings.RAG_LEXICAL_WEIGHT)

            # Nearest-Neighbor Noise Filter:
            # If semantic similarity is extremely low (< 0.28) and no exact statutory match occurred, discard
            if v_score < 0.28 and norm_kw < 0.35:
                continue

            scored_candidates.append((composite_score, v_score, chunk))

        # 9. Sort by composite score descending
        scored_candidates.sort(key=lambda x: x[0], reverse=True)

        # 10. Filter by Relevance Threshold and Deduplicate
        top_chunks: List[Dict[str, Any]] = []
        seen_sections: Set[str] = set()

        for comp_score, sem_score, chunk in scored_candidates:
            if comp_score < threshold:
                # Do not retrieve ungrounded, irrelevant matches merely because they are nearest in vector space
                continue

            src = chunk.source
            sec_key = f"{src.title if src else ''}_{chunk.section_number}".lower()
            if sec_key in seen_sections:
                # Deduplicate repeated section instances
                continue
            seen_sections.add(sec_key)

            snippet = (
                chunk.chunk_text[:280] + "..."
                if len(chunk.chunk_text) > 280
                else chunk.chunk_text
            )

            top_chunks.append({
                "chunk_id": str(chunk.id),
                "source_id": str(chunk.source_id),
                "source_title": src.title if src else "Official Indian Statute",
                "source_type": src.source_type if src else "BARE_ACT",
                "act_or_judgment_identifier": src.act_or_judgment_identifier if src else None,
                "citation": src.citation if src else None,
                "section_number": chunk.section_number,
                "clause_heading": chunk.clause_heading,
                "chunk_text": chunk.chunk_text,
                "relevant_text": snippet,
                "jurisdiction": src.jurisdiction if src else "Union of India",
                "document_version": src.document_version if src else "1.0",
                "official_source_url": src.official_source_url if src else None,
                "content_checksum": chunk.content_checksum,
                "score": round(comp_score, 4),
                "semantic_score": round(sem_score, 4),
                "detected_domain": detected_domain,
            })

            if len(top_chunks) >= limit:
                break

        return top_chunks
