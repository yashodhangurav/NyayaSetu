"""Synthesized Landmark Judicial Precedent Chunks for NyayaSetu RAG.
Covers leading Supreme Court rulings across all major practice areas.
"""

from typing import List
from rag.ingest.chunker import LegalStructureChunker, StandardizedLegalChunk


def get_expanded_precedents_chunks() -> List[StandardizedLegalChunk]:
    chunks: List[StandardizedLegalChunk] = []
    sc = LegalStructureChunker

    # 1. Danial Latifi v. Union of India (2001) 7 SCC 740
    chunks.append(sc.chunk_judgment_summary(
        source_id="SRC_CASE_DANIAL_001",
        case_title="Danial Latifi v. Union of India",
        citation="(2001) 7 SCC 740",
        court="Supreme Court of India (Constitution Bench)",
        judgment_date="2001-09-28",
        issue="Does a Muslim husband liability to maintain his divorced wife terminate at the end of the iddat period under the 1986 Act?",
        holding="A Muslim husband must make reasonable and fair provision within the iddat period that contemplates maintenance for the woman entire lifetime until remarriage.",
        ratio_decidendi="Interpreting Section 3(1)(a) of the 1986 Act to conform with Articles 14 and 21, the liability is not limited to iddat period expenses; reasonable provision must be made to sustain the woman throughout her life.",
        topic_tags=["danial latifi", "muslim women maintenance", "iddat provision", "lifetime support", "fair provision"],
    ))

    # 2. Jacob Mathew v. State of Punjab (2005) 6 SCC 1
    chunks.append(sc.chunk_judgment_summary(
        source_id="SRC_CASE_JACOBMATHEW_001",
        case_title="Jacob Mathew v. State of Punjab",
        citation="(2005) 6 SCC 1",
        court="Supreme Court of India",
        judgment_date="2005-08-05",
        issue="What standard of negligence is required to sustain a criminal prosecution against a medical professional?",
        holding="Criminal liability requires proof of gross negligence or recklessness. An FIR should not be registered against a doctor without obtaining an independent qualified medical opinion.",
        ratio_decidendi="A simple lack of care or error of judgment does not constitute criminal rashness under Section 304A IPC / Section 106 BNS; the degree of negligence must be gross and accompanied by reckless disregard for patient safety.",
        topic_tags=["jacob mathew", "medical negligence", "gross negligence test", "doctor criminal prosecution", "expert medical opinion"],
    ))

    # 3. Imperia Structures Ltd. v. Anil Patni (2020) 10 SCC 783
    chunks.append(sc.chunk_judgment_summary(
        source_id="SRC_CASE_IMPERIA_001",
        case_title="Imperia Structures Ltd. v. Anil Patni",
        citation="(2020) 10 SCC 783",
        court="Supreme Court of India",
        judgment_date="2020-11-02",
        issue="Does the enactment of RERA bar a homebuyer from approaching the Consumer Disputes Redressal Commission?",
        holding="Remedies under the Consumer Protection Act and RERA are concurrent; a homebuyer may initiate proceedings before Consumer Forums notwithstanding RERA.",
        ratio_decidendi="Section 79 RERA bars civil courts, but Consumer Commissions are not civil courts. The remedies are cumulative, giving homebuyers freedom of forum choice for delayed project possession.",
        topic_tags=["imperia structures", "rera vs consumer protection", "concurrent remedy", "builder delay", "flat possession refund"],
    ))

    # 4. Arnesh Kumar v. State of Bihar (2014) 8 SCC 273
    chunks.append(sc.chunk_judgment_summary(
        source_id="SRC_CASE_ARNESH_001",
        case_title="Arnesh Kumar v. State of Bihar",
        citation="(2014) 8 SCC 273",
        court="Supreme Court of India",
        judgment_date="2014-07-02",
        issue="Are police authorized to make automatic arrests in dowry harassment and offences punishable with up to seven years imprisonment?",
        holding="Police shall not automatically arrest accused persons in offences punishable with imprisonment up to seven years without complying with statutory checklists.",
        ratio_decidendi="Arrest must not be made merely on the registration of a cognizable case. The investigating officer must issue a notice of appearance unless necessity grounds under Section 41 CrPC / Section 35 BNSS are satisfied and recorded.",
        topic_tags=["arnesh kumar", "arrest safeguards", "no automatic arrest", "section 41a notice", "bnss 35 checklist"],
    ))

    # 5. Jitendra Singh v. State of Madhya Pradesh (2021) SCC OnLine SC 802
    chunks.append(sc.chunk_judgment_summary(
        source_id="SRC_CASE_JITENDRA_001",
        case_title="Jitendra Singh v. State of Madhya Pradesh",
        citation="2021 SCC OnLine SC 802",
        court="Supreme Court of India",
        judgment_date="2021-09-06",
        issue="Does a mutation entry in revenue records confer or extinguish legal title to immovable property?",
        holding="Mutation of property in revenue records neither creates nor extinguishes title, nor does it have any presumptive value on title.",
        ratio_decidendi="Revenue records (Khata, RTC, Pahani) are maintained solely for fiscal collection purposes. If there is a dispute regarding title, the parties must seek relief before the competent Civil Court.",
        topic_tags=["jitendra singh", "mutation is not title", "revenue records fiscal nature", "khata not ownership", "civil court title"],
    ))

    # 6. Manchegowda v. State of Karnataka (1984) 3 SCC 301
    chunks.append(sc.chunk_judgment_summary(
        source_id="SRC_CASE_MANCHEGOWDA_001",
        case_title="Manchegowda v. State of Karnataka",
        citation="(1984) 3 SCC 301",
        court="Supreme Court of India (Constitution Bench)",
        judgment_date="1984-04-17",
        issue="Is the Karnataka PTCL Act prohibiting alienation of granted land to SC/ST persons constitutionally valid?",
        holding="Upheld the constitutional validity of the PTCL Act as reasonable state affirmative action protecting vulnerable landless grantees.",
        ratio_decidendi="Transfers of granted lands made in violation of grant conditions or statutory non-alienation clauses are void ab initio, and the State is empowered to resume and restore such lands without compensation to unauthorized purchasers.",
        topic_tags=["manchegowda", "ptcl act validity", "sc st granted land", "resumption of land", "void alienation"],
    ))

    # 7. Nekkanti Rama Lakshmi v. State of Karnataka (2020) 14 SCC 232
    chunks.append(sc.chunk_judgment_summary(
        source_id="SRC_CASE_NEKKANTI_001",
        case_title="Nekkanti Rama Lakshmi v. State of Karnataka",
        citation="(2020) 14 SCC 232",
        court="Supreme Court of India",
        judgment_date="2017-10-26",
        issue="Can an application for resumption of granted land under Section 5 PTCL Act be entertained after an inordinate delay of several decades?",
        holding="Applications for resumption of land under the PTCL Act must be filed within a reasonable period; an unexplained delay of 25 years bars statutory relief.",
        ratio_decidendi="Where no period of limitation is prescribed by statute, power must be exercised within a reasonable time. Rights settled over decades cannot be reopened arbitrarily to prejudice established possessory interests.",
        topic_tags=["nekkanti rama lakshmi", "ptcl limitation", "reasonable period doctrine", "delay bars resumption", "karnataka granted land"],
    ))

    # 8. Rangappa v. Sri Mohan (2010) 11 SCC 441
    chunks.append(sc.chunk_judgment_summary(
        source_id="SRC_CASE_RANGAPPA_001",
        case_title="Rangappa v. Sri Mohan",
        citation="(2010) 11 SCC 441",
        court="Supreme Court of India (3-Judge Bench)",
        judgment_date="2010-05-07",
        issue="Does the statutory presumption under Section 139 NI Act include the existence of a legally enforceable debt?",
        holding="The presumption mandated by Section 139 NI Act includes the existence of a legally enforceable debt or liability.",
        ratio_decidendi="The burden rests on the accused drawer to rebut the presumption by raising a probable defence on the standard of preponderance of probabilities; bare denial is insufficient.",
        topic_tags=["rangappa v sri mohan", "section 139 ni act", "cheque bounce presumption", "legally enforceable debt", "preponderance of probabilities"],
    ))

    return chunks
