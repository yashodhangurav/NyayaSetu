"""Synthesized Specialized Legal Domain Chunks for NyayaSetu Canonical Corpus.
Covers Healthcare (KPME, Negligence), Direct/Indirect Tax, MSME Samadhaan, RTI, and Education.
"""

from typing import List
from rag.ingest.chunker import LegalStructureChunker, StandardizedLegalChunk


def get_specialized_domain_chunks() -> List[StandardizedLegalChunk]:
    chunks: List[StandardizedLegalChunk] = []
    sc = LegalStructureChunker

    # 1. Karnataka Private Medical Establishments Act, 2007 (KPME)
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_KAR_KPME_001",
        act="Karnataka Private Medical Establishments Act, 2007",
        short_code="KPME",
        section="Patient Charter & Pricing",
        clause_heading="Patient rights, rate disclosure, and dead body retention prohibition",
        section_text=(
            "Mandates registration and quality standards for all private clinics, diagnostic centres, and hospitals in Karnataka. "
            "Requires prominent display of package rates and medical fee schedules. Explicitly prohibits medical establishments "
            "from detaining the body of a deceased patient on grounds of unpaid hospital charges or outstanding billing disputes. "
            "Establishes District Grievance Redressal Committees to investigate medical complaints."
        ),
        chapter="Patient Charter and Regulation",
        topic_tags=["kpme act", "karnataka hospital rules", "patient rights", "dead body detention ban", "medical grievance"],
    ))

    # 2. Income-tax Act, 1961 - Capital Gains & TDS
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_ITAX_1961",
        act="Income-tax Act, 1961",
        short_code="IT_ACT",
        section="Section 45, 54 & 194-IA",
        clause_heading="Capital gains taxation on property sale and 1% TDS requirement",
        section_text=(
            "Section 45 charges profits from the transfer of a capital asset (such as immovable property) to capital gains tax. "
            "Section 54 provides tax exemption for individuals if long-term capital gains from residential property sale are reinvested "
            "in purchasing or constructing a new residential house within statutory timelines. Section 194-IA mandates the buyer to deduct "
            "1% TDS on the total sale consideration if the property transaction value is fifty lakh rupees or higher."
        ),
        chapter="Chapter IV: Capital Gains & Chapter XVII: Collection and Recovery",
        topic_tags=["income tax", "capital gains property", "section 54 exemption", "194-ia tds 1 percent", "property tax compliance"],
    ))

    # 3. MSMED Act, 2006 - Delayed Payments (Section 15 & 16)
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_MSME_001",
        act="Micro, Small and Medium Enterprises Development Act, 2006",
        short_code="MSMED",
        section="Section 15, 16 & 18",
        clause_heading="Mandatory payment window and compound interest on delayed MSME payments",
        section_text=(
            "Section 15 requires buyers to pay suppliers within agreed timelines not exceeding forty-five days from delivery. "
            "Section 16 penalizes delayed payments with compound interest with monthly rests at three times the RBI bank rate. "
            "Section 18 permits MSMEs to file references before the Micro and Small Enterprises Facilitation Council (MSEFC Samadhaan portal) "
            "for conciliation and binding arbitration. An appeal requires 75% pre-deposit under Section 19."
        ),
        chapter="Chapter V: Delayed Payments to Micro and Small Enterprises",
        topic_tags=["msme samadhaan", "delayed payment 45 days", "three times rbi interest", "msefc arbitration", "msmed act 2006"],
    ))

    # 4. Right to Information Act, 2005 - Section 7
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_RTI_001",
        act="Right to Information Act, 2005",
        short_code="RTI",
        section="Section 7",
        clause_heading="Disposal of requests and emergency life or liberty timeline",
        section_text=(
            "Directs the Public Information Officer (PIO) to provide requested information or reject it with reasons within thirty days "
            "of receipt of application. Where the information sought concerns the life or liberty of a person, it must be provided within "
            "forty-eight hours. Failure to respond within the stipulated period constitutes a deemed refusal, entitling the applicant "
            "to file a First Appeal under Section 19(1)."
        ),
        chapter="Chapter II: Right to Information and Obligations of Public Authorities",
        topic_tags=["rti act 2005", "30 day rti timeline", "48 hour life liberty", "deemed refusal", "pio obligations", "first appeal"],
    ))

    # 5. Right of Children to Free and Compulsory Education Act, 2009 (RTE)
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_RTE_001",
        act="Right of Children to Free and Compulsory Education Act, 2009",
        short_code="RTE",
        section="Section 3, 12 & 13",
        clause_heading="Free compulsory education and 25% quota in private unaided schools",
        section_text=(
            "Section 3 guarantees every child aged six to fourteen years the right to free and compulsory education in a neighborhood school. "
            "Section 12(1)(c) mandates private unaided schools to admit at least twenty-five percent children belonging to economically weaker "
            "and disadvantaged groups in class I. Section 13 strictly prohibits schools from collecting capitation fees or subjecting children "
            "and parents to screening interviews."
        ),
        chapter="Right to Free and Compulsory Education",
        topic_tags=["rte act 2009", "25 percent private school quota", "free education 6 to 14", "capitation fee ban", "child rights"],
    ))

    # 6. Information Technology Act, 2000 - Section 66C & 66D
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_IT_001",
        act="Information Technology Act, 2000",
        short_code="IT_ACT",
        section="Section 66C & 66D",
        clause_heading="Punishment for identity theft and cheating by personation using computer resource",
        section_text=(
            "Section 66C punishes fraudulent or dishonest use of electronic signature, password, or unique identification feature "
            "with imprisonment up to three years and fine. Section 66D penalizes cheating by personation over computer systems or "
            "telecommunication devices (phishing, OTP fraud, spoofing) with imprisonment up to three years and fine."
        ),
        chapter="Chapter XI: Offences",
        topic_tags=["it act 2000", "section 66c", "section 66d", "identity theft", "phishing fraud", "otp scam", "cybercrime"],
    ))

    # 7. Motor Vehicles Act, 1988 (Sec 185) - Driving by a drunken person (Drink and Drive)
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_MVA_1988",
        act="Motor Vehicles Act, 1988",
        short_code="MV_ACT",
        section="Section 185",
        clause_heading="Driving by a drunken person or by a person under the influence of drugs",
        section_text=(
            "Whoever, while driving, or attempting to drive, a motor vehicle—"
            "(a) has, in his blood, alcohol exceeding 30 mg. per 100 ml. of blood detected in a test by a breath analyser, or in any other test including a laboratory test, or "
            "(b) is under the influence of a drug to such an extent as to be incapable of exercising proper control over the vehicle, "
            "shall be punishable for the first offence with imprisonment for a term which may extend to six months, or with fine of ten thousand rupees, or with both; "
            "and for a second or subsequent offence, if committed within three years of the commission of the previous similar offence, with imprisonment for a term which may extend to two years, or with fine of fifteen thousand rupees, or with both. "
            "The driving licence of the offender is also liable to suspension or disqualification by the licensing authority."
        ),
        chapter="Chapter XIII: Offences, Penalties and Procedure",
        topic_tags=["motor vehicles act", "section 185", "drink and drive", "drunk driving", "breath analyser", "traffic fine 10000", "blood alcohol limit", "licence suspension"],
    ))

    # 8. Motor Vehicles Act, 1988 (Sec 194 & Sec 200) - Traffic Violations, Fines, and Compounding
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_MVA_1988",
        act="Motor Vehicles Act, 1988",
        short_code="MV_ACT",
        section="Section 194 & Section 200",
        clause_heading="Penalties for traffic violations, helmet, seatbelt, and compounding of offences",
        section_text=(
            "Section 194B prescribes a penalty of one thousand rupees for driving without wearing a safety belt. "
            "Section 194C and 194D prescribe a penalty of one thousand rupees for riding without protective headgear (helmet) and three months disqualification of licence. "
            "Section 184 penalizes dangerous or rash driving with fines up to five thousand rupees. "
            "Section 200 authorizes designated police and transport officers to compound specified traffic offences on the spot or through electronic virtual courts / e-challan systems. "
            "When compounding a traffic fine, police officers must issue an official electronic or physical printed receipt. "
            "A citizen has the legal right to challenge an erroneous traffic challan before the designated Metropolitan Magistrate or Virtual Court."
        ),
        chapter="Chapter XIII: Offences, Penalties and Procedure",
        topic_tags=["traffic police fine", "challan", "helmet fine 1000", "seatbelt penalty", "section 194", "section 200 compounding", "echallan", "virtual court", "traffic violation"],
    ))

    # 9. Bharatiya Nagarik Suraksha Sanhita, 2023 - Section 63, 64 & Section 35 (Court Summons and Notice of Appearance)
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_BNSS_001",
        act="Bharatiya Nagarik Suraksha Sanhita, 2023",
        short_code="BNSS",
        section="Section 63 & Section 64",
        clause_heading="Form of summons, service of summons on person, and notice of appearance",
        section_text=(
            "Every summons issued by a Court under BNSS shall be in writing, in duplicate, signed by the presiding officer or designated officer, and bear the seal of the Court. "
            "The summons may be served by a police officer, an officer of the court, or electronically via encrypted electronic communication. "
            "Service is effected by tendering or delivering a duplicate copy to the person summoned. "
            "Under Section 35 BNSS, a police officer where arrest is not mandatory may issue a formal written notice of appearance to any person against whom a reasonable complaint has been made. "
            "When a citizen receives a court summons, they must examine whether they are summoned as a witness or as an accused, note the exact court room, case number, and appearance date, and appear in person or through an empanelled advocate to prevent issuance of bailable or non-bailable warrants."
        ),
        chapter="Chapter VI: Processes to Compel Appearance",
        effective_date="2024-07-01",
        topic_tags=["court summons", "legal summon", "service of summons", "section 63 bnss", "section 64 bnss", "section 35 notice of appearance", "warrant prevention", "magistrate court"],
    ))

    # 10. Karnataka Land Revenue Act, 1964 - Section 128 & 129 (Change of Plot Owner, Acquisition of Rights, Mutation)
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_KLRA_001",
        act="Karnataka Land Revenue Act, 1964",
        short_code="KLRA",
        section="Section 128 & Section 129",
        clause_heading="Acquisition of rights, reporting of plot ownership change, and mutation register",
        section_text=(
            "Section 128 requires any person acquiring by succession, survivorship, inheritance, partition, purchase, mortgage, gift or otherwise, any right in any land or plot, "
            "to report orally or in writing his acquisition of such right to the prescribed revenue officer (Village Accountant or Tahsildar / Bhoomi portal) within three months from the date of such acquisition. "
            "Section 129 mandates the revenue officer to enter the acquisition in the Register of Mutations (Form 12) and post a copy at the village chavadi, issuing notice to all persons interested. "
            "If no objection is received within thirty days, the mutation is certified and the RTC / Pahani is updated. "
            "For urban plots under BBMP or municipal corporations, change of plot ownership requires submitting the registered Sale Deed, Encumbrance Certificate, and previous tax receipts to secure an e-Khata or A-Khata transfer under Section 114 of the Karnataka Municipal Corporations Act."
        ),
        chapter="Chapter XI: Record of Rights",
        jurisdiction="Karnataka",
        topic_tags=["change of plot owner", "plot ownership transfer", "mutation", "section 128 klra", "section 129 mutation", "rtc update", "khata transfer", "urban plot title"],
    ))

    # 11. Code of Civil Procedure, 1908 - Order V (Issue and Service of Summons in Civil Matters)
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_CPC_001",
        act="Code of Civil Procedure, 1908",
        short_code="CPC",
        section="Order V Rule 1 & Rule 9",
        clause_heading="Summons to defendant to appear and answer plaint, and 30-day written statement limit",
        section_text=(
            "When a civil suit has been duly instituted, a summons may be issued to the defendant to appear and answer the claim on a day specified therein. "
            "The defendant shall, within thirty days from the date of service of summons on him, present a written statement of his defence. "
            "Such period may be extended up to ninety days by the Court for reasons to be recorded in writing. "
            "Service of civil summons may be made by personal delivery, registered post acknowledgment due (RPAD), speed post, or authorized courier service."
        ),
        chapter="The First Schedule: Order V",
        topic_tags=["cpc summons", "order 5 rule 1", "civil court summons", "30 days written statement", "service by rpad", "defendant appearance"],
    ))

    return chunks
