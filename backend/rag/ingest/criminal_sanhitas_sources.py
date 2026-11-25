"""Synthesized Criminal Law & Sanhitas 2023 Chunks for NyayaSetu Canonical Corpus.
Provides structured summaries of BNS, BNSS, BSA, NDPS, POCSO, and Victim Rights.
"""

from typing import List
from rag.ingest.chunker import LegalStructureChunker, StandardizedLegalChunk


def get_criminal_sanhitas_chunks() -> List[StandardizedLegalChunk]:
    chunks: List[StandardizedLegalChunk] = []
    sc = LegalStructureChunker

    # 1. BNS 2023 - Section 318 (Cheating)
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_BNS_001",
        act="Bharatiya Nyaya Sanhita, 2023",
        short_code="BNS",
        section="Section 318",
        clause_heading="Cheating and dishonestly inducing delivery of property",
        section_text=(
            "Defines cheating as fraudulently or dishonestly deceiving any person to deliver property or consent "
            "to retain property. Sub-section (4) covers cheating with dishonest inducement to deliver property or alter "
            "valuable securities, punishable with imprisonment up to seven years and fine (formerly Section 420 IPC)."
        ),
        chapter="Chapter XVII: Offences Against Property",
        topic_tags=["bns 318", "cheating", "fraudulent inducement", "ipc 420 replacement", "property offences"],
    ))

    # 2. BNS 2023 - Section 303 (Theft)
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_BNS_001",
        act="Bharatiya Nyaya Sanhita, 2023",
        short_code="BNS",
        section="Section 303",
        clause_heading="Theft and community service for petty theft",
        section_text=(
            "Defines theft as dishonestly taking movable property out of the possession of any person without consent. "
            "Sub-section (2) provides punishment of imprisonment up to three years, fine, or both. For first-time petty theft "
            "involving stolen property valued below five thousand rupees upon return, community service may be ordered."
        ),
        chapter="Chapter XVII: Offences Against Property",
        topic_tags=["bns 303", "theft", "community service", "ipc 379 replacement"],
    ))

    # 3. BNS 2023 - Section 85 & 86 (Cruelty by Husband or Relatives)
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_BNS_001",
        act="Bharatiya Nyaya Sanhita, 2023",
        short_code="BNS",
        section="Section 85 & 86",
        clause_heading="Cruelty to a woman by husband or relatives",
        section_text=(
            "Section 85 penalizes a husband or his relative who subjects a woman to cruelty with imprisonment up to three years and fine. "
            "Section 86 defines cruelty as conduct likely to drive the woman to suicide or cause grave injury, or harassment to coerce "
            "her or her relatives into meeting unlawful property demands (formerly Section 498A IPC)."
        ),
        chapter="Chapter V: Offences Against Women and Children",
        topic_tags=["bns 85", "bns 86", "dowry harassment", "cruelty to wife", "ipc 498a replacement"],
    ))

    # 4. BNSS 2023 - Section 173 (FIR and Zero FIR)
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_BNSS_001",
        act="Bharatiya Nagarik Suraksha Sanhita, 2023",
        short_code="BNSS",
        section="Section 173",
        clause_heading="Information in cognizable cases and Zero FIR procedure",
        section_text=(
            "Mandates registration of an FIR for any cognizable offence, irrespective of jurisdictional area (Zero FIR). "
            "Permits electronic communication of information, requiring informant signature within three days. "
            "In offences punishable with three to seven years imprisonment, preliminary inquiry may be conducted within fourteen days "
            "with prior permission of a Deputy Superintendent of Police before proceeding."
        ),
        chapter="Chapter XIII: Information to the Police and Powers to Investigate",
        topic_tags=["bnss 173", "fir", "zero fir", "electronic fir", "preliminary inquiry", "crpc 154 replacement"],
    ))

    # 5. BNSS 2023 - Section 35 (Arrest Safeguards and Notice)
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_BNSS_001",
        act="Bharatiya Nagarik Suraksha Sanhita, 2023",
        short_code="BNSS",
        section="Section 35",
        clause_heading="Procedure and limits on police arrest",
        section_text=(
            "Specifies when police may arrest without warrant. For offences punishable with up to seven years imprisonment, "
            "arrest requires recorded satisfaction of necessity grounds (preventing tampering, absconding, further offences). "
            "Sub-section (3) mandates issuance of a notice of appearance where arrest is not deemed necessary (formerly Section 41A CrPC)."
        ),
        chapter="Chapter V: Arrest of Persons",
        topic_tags=["bnss 35", "arrest safeguards", "notice of appearance", "crpc 41a replacement", "arnesh kumar guidelines"],
    ))

    # 6. BNSS 2023 - Section 482 (Anticipatory Bail)
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_BNSS_001",
        act="Bharatiya Nagarik Suraksha Sanhita, 2023",
        short_code="BNSS",
        section="Section 482",
        clause_heading="Direction for grant of bail to person apprehending arrest",
        section_text=(
            "Empowers the High Court and Sessions Court to grant anticipatory bail to any person apprehending arrest "
            "in non-bailable offences. Evaluates nature and gravity of accusation, criminal antecedents, possibility of fleeing justice, "
            "and whether accusations appear motivated to humiliate the applicant (formerly Section 438 CrPC)."
        ),
        chapter="Chapter XXXV: Provisions as to Bail and Bonds",
        topic_tags=["bnss 482", "anticipatory bail", "pre-arrest bail", "sessions court", "crpc 438 replacement"],
    ))

    # 7. BSA 2023 - Section 63 (Admissibility of Electronic Records)
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_BSA_001",
        act="Bharatiya Sakshya Adhiniyam, 2023",
        short_code="BSA",
        section="Section 63",
        clause_heading="Admissibility of electronic records and certification",
        section_text=(
            "Provides that information contained in an electronic record printed, stored, or copied in optical/magnetic media "
            "shall be deemed an admissible document without proof of original, provided statutory conditions of system integrity are met. "
            "Requires an accompanying certificate signed by the person in lawful management or an authorized official (formerly Section 65B IEA)."
        ),
        chapter="Chapter V: Documentary and Electronic Evidence",
        topic_tags=["bsa 63", "electronic evidence", "digital certificate", "whatsapp chat admissibility", "iea 65b replacement"],
    ))

    # 8. BNSS 2023 - Section 396 (Victim Compensation Scheme)
    chunks.extend(sc.chunk_statute_section(
        source_id="SRC_BNSS_001",
        act="Bharatiya Nagarik Suraksha Sanhita, 2023",
        short_code="BNSS",
        section="Section 396",
        clause_heading="Victim compensation scheme and legal services authority awards",
        section_text=(
            "Directs State Governments in coordination with Central Government to maintain victim compensation funds. "
            "The trial court may recommend compensation to District Legal Services Authority (DLSA) or State Legal Services Authority (SLSA). "
            "Enables award of interim medical and rehabilitative relief to victims of rape, acid attack, and severe trauma, "
            "even where the offender is not identified or convicted (formerly Section 357A CrPC)."
        ),
        chapter="Chapter XXIX: Judgment and Victim Rights",
        topic_tags=["victim compensation", "bnss 396", "dlsa compensation", "interim relief", "crpc 357a replacement"],
    ))

    return chunks
