"""Synthesized Banking, Consumer Protection & Labour Law Chunks for NyayaSetu RAG.
Covers Cheque Dishonour (NI Act), SARFAESI, Digital Lending, CPA 2019, Gratuity, and POSH.
"""

from typing import List
from rag.ingest.chunker import LegalStructureChunker, StandardizedLegalChunk


def get_banking_consumer_labour_chunks() -> List[StandardizedLegalChunk]:
    chunks: List[StandardizedLegalChunk] = []
    sc = LegalStructureChunker

    # 1. Negotiable Instruments Act, 1881 - Section 138 & 142
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_NIA_001",
        act="Negotiable Instruments Act, 1881",
        short_code="NI_ACT",
        section="Section 138 & 142",
        clause_heading="Dishonour of cheque for insufficiency of funds and procedure",
        section_text=(
            "Penalizes dishonour of a cheque drawn for discharge of legally enforceable debt with imprisonment up to two years, "
            "fine up to twice the cheque amount, or both. Prescribes strict timelines: statutory written demand notice must be dispatched "
            "within thirty days of cheque return memo; the drawer has fifteen days to settle payment; failing which a complaint must be filed "
            "before the Judicial Magistrate First Class within thirty days under Section 142."
        ),
        chapter="Chapter XVII: Penalties in Case of Dishonour of Cheques",
        topic_tags=["cheque bounce", "section 138", "demand notice 30 days", "15 days payment", "section 142 complaint", "jmfc"],
    ))

    # 2. SARFAESI Act, 2002 - Section 13
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_SARFAESI_001",
        act="SARFAESI Act, 2002",
        short_code="SARFAESI",
        section="Section 13",
        clause_heading="Enforcement of security interest without court intervention",
        section_text=(
            "Allows secured creditor banks to enforce security interests upon Non-Performing Asset (NPA) classification. "
            "Section 13(2) mandates sixty days notice to discharge liabilities in full. Under Section 13(3A), the borrower may submit "
            "representations which the creditor must decide within fifteen days. Upon default, Section 13(4) empowers the bank to take "
            "symbolic or physical possession of the secured asset, challengeable before the DRT under Section 17 within forty-five days."
        ),
        chapter="Chapter III: Enforcement of Security Interest",
        topic_tags=["sarfaesi", "section 13(2) notice", "section 13(4) possession", "drt appeal section 17", "npa debt recovery"],
    ))

    # 3. RBI Guidelines on Digital Lending, 2022
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_RBI_LENDING_001",
        act="RBI Guidelines on Digital Lending, 2022",
        short_code="RBI_LENDING",
        section="Regulatory Directions",
        clause_heading="Borrower safeguards, KFS, and prohibition on recovery harassment",
        section_text=(
            "Mandates direct loan disbursement and repayment between borrower bank account and Regulated Entity without third-party pooling. "
            "Requires delivery of a standardized Key Fact Statement (KFS) stating All-Inclusive Annual Percentage Rate (APR). "
            "Enforces a look-up/cooling-off exit window without prepayment penalties. Strictly forbids loan recovery agents from accessing "
            "borrower contacts, location, media files, or making threatening and unauthorized communication."
        ),
        chapter="Digital Lending Regulations",
        topic_tags=["digital lending", "rbi guidelines", "key fact statement", "harassment ban", "recovery agent code"],
    ))

    # 4. Consumer Protection Act, 2019 - Section 2(7), 35 & 69
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_CPA_001",
        act="Consumer Protection Act, 2019",
        short_code="CPA_2019",
        section="Section 2(7), 35 & 69",
        clause_heading="Consumer rights, electronic e-Daakhil filing, and two-year limitation",
        section_text=(
            "Defines a consumer as any person who buys goods or hires services for consideration, excluding commercial resale. "
            "Section 35 enables filing complaints before the District Consumer Commission online through e-Daakhil. "
            "Section 69 prescribes a two-year limitation period from the date of the cause of action. Provides remedies including refund, "
            "replacement, removal of defects, and compensation for deficiency in service or product liability."
        ),
        chapter="Chapter IV: Consumer Disputes Redressal Commission",
        topic_tags=["consumer protection", "cpa 2019", "e-daakhil", "2 year limitation", "deficiency in service", "refund"],
    ))

    # 5. CCPA Dark Patterns Guidelines, 2023
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_CCPA_DARK_001",
        act="CCPA Guidelines for Prevention and Regulation of Dark Patterns, 2023",
        short_code="CCPA_DARK",
        section="Guidelines 4 & 5",
        clause_heading="Prohibited deceptive digital interface practices in e-commerce",
        section_text=(
            "Prohibits thirteen specified dark pattern techniques used on platforms, including False Urgency (fabricated countdown timers), "
            "Basket Sneaking (adding unselected items or donations into cart), Subscription Traps (deliberately obstructing cancellation "
            "of recurring memberships), and Drip Pricing (revealing mandatory fees only at final checkout). Actionable as unfair trade practices."
        ),
        chapter="E-Commerce Consumer Safeguards",
        topic_tags=["dark patterns", "ccpa guidelines 2023", "drip pricing", "basket sneaking", "subscription trap", "e-commerce"],
    ))

    # 6. Payment of Gratuity Act, 1972 - Section 4 & 7
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_GRATUITY_001",
        act="Payment of Gratuity Act, 1972",
        short_code="PGA_1972",
        section="Section 4 & 7",
        clause_heading="Gratuity eligibility, computation formula, and payment timeline",
        section_text=(
            "Section 4 grants gratuity to an employee upon termination after completing five years of continuous service "
            "(waived on death or disablement). Calculated at fifteen days wages per completed service year based on last drawn basic and DA. "
            "Section 7 requires the employer to disburse gratuity within thirty days of it becoming payable, failing which simple interest "
            "at the notified rate is mandatory."
        ),
        chapter="Gratuity Entitlement",
        topic_tags=["payment of gratuity", "5 years continuous service", "gratuity formula", "30 days payment", "pga 1972"],
    ))

    # 7. POSH Act, 2013 - Section 4 & 9
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_POSH_001",
        act="Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013",
        short_code="POSH",
        section="Section 4 & 9",
        clause_heading="Mandatory Internal Committee and complaint procedure",
        section_text=(
            "Section 4 mandates constitution of an Internal Committee (IC) in every workplace employing ten or more persons, "
            "headed by a senior woman employee with an external NGO member. Section 9 permits aggrieved women to file a complaint "
            "within three months of incident (extendable by three months). Inquiries must be completed within ninety days with interim protections."
        ),
        chapter="Workplace Protection for Women",
        topic_tags=["posh act 2013", "internal committee", "icc", "sexual harassment workplace", "3 month complaint timeline"],
    ))

    return chunks
