"""Comprehensive Indian Criminal Law Concordance Table (IPC/CrPC/IEA -> BNS/BNSS/BSA 2023)."""

from typing import Dict, Optional, NamedTuple


class ConcordanceEntry(NamedTuple):
    repealed_act: str
    repealed_section: str
    repealed_title: str
    active_act: str
    active_section: str
    active_title: str
    substantive_change_note: str


# Mapping dictionary: (Repealed Act Shortcode, Section) -> ConcordanceEntry
CRIMINAL_CONCORDANCE: Dict[str, ConcordanceEntry] = {
    # ── IPC 1860 -> BNS 2023 ──
    "IPC:420": ConcordanceEntry(
        "Indian Penal Code, 1860",
        "Section 420",
        "Cheating and dishonestly inducing delivery of property",
        "Bharatiya Nyaya Sanhita, 2023",
        "Section 318(4)",
        "Cheating and dishonestly inducing delivery of property",
        "Penal consequence retained; categorized under Chapter XVIII: Offences Against Property."
    ),
    "IPC:302": ConcordanceEntry(
        "Indian Penal Code, 1860",
        "Section 302",
        "Punishment for murder",
        "Bharatiya Nyaya Sanhita, 2023",
        "Section 103(1)",
        "Punishment for murder",
        "Punishment death or life imprisonment retained; mob lynching clause added in Section 103(2)."
    ),
    "IPC:304A": ConcordanceEntry(
        "Indian Penal Code, 1860",
        "Section 304A",
        "Causing death by negligence",
        "Bharatiya Nyaya Sanhita, 2023",
        "Section 106",
        "Causing death by negligence",
        "Categorized into medical negligence and hit-and-run scenarios with distinct sentences."
    ),
    "IPC:307": ConcordanceEntry(
        "Indian Penal Code, 1860",
        "Section 307",
        "Attempt to murder",
        "Bharatiya Nyaya Sanhita, 2023",
        "Section 109",
        "Attempt to murder",
        "Core elements identical."
    ),
    "IPC:376": ConcordanceEntry(
        "Indian Penal Code, 1860",
        "Section 376",
        "Punishment for rape",
        "Bharatiya Nyaya Sanhita, 2023",
        "Section 64",
        "Punishment for rape",
        "Incorporated under Chapter V: Offences Against Woman and Child."
    ),
    "IPC:379": ConcordanceEntry(
        "Indian Penal Code, 1860",
        "Section 379",
        "Punishment for theft",
        "Bharatiya Nyaya Sanhita, 2023",
        "Section 303(2)",
        "Theft",
        "Community service option introduced for first-time petty theft under ₹5,000 upon return."
    ),
    "IPC:498A": ConcordanceEntry(
        "Indian Penal Code, 1860",
        "Section 498A",
        "Husband or relative of husband of a woman subjecting her to cruelty",
        "Bharatiya Nyaya Sanhita, 2023",
        "Section 85",
        "Subjecting a woman to cruelty",
        "Elements of mental and physical cruelty preserved under Chapter V."
    ),
    "IPC:506": ConcordanceEntry(
        "Indian Penal Code, 1860",
        "Section 506",
        "Punishment for criminal intimidation",
        "Bharatiya Nyaya Sanhita, 2023",
        "Section 351(2)",
        "Criminal intimidation",
        "Cognizable and bailable classification aligned."
    ),
    "IPC:124A": ConcordanceEntry(
        "Indian Penal Code, 1860",
        "Section 124A",
        "Sedition",
        "Bharatiya Nyaya Sanhita, 2023",
        "Section 152",
        "Act endangering sovereignty, unity and integrity of India",
        "Colonial term 'Sedition' removed; re-framed around armed rebellion and secessionist acts."
    ),

    # ── CrPC 1973 -> BNSS 2023 ──
    "CRPC:154": ConcordanceEntry(
        "Code of Criminal Procedure, 1973",
        "Section 154",
        "Information in cognizable cases (FIR)",
        "Bharatiya Nagarik Suraksha Sanhita, 2023",
        "Section 173",
        "Information in cognizable cases",
        "Statutory recognition of Zero FIR (jurisdiction-neutral) and electronic FIR (e-FIR) with 3-day signature rule."
    ),
    "CRPC:41A": ConcordanceEntry(
        "Code of Criminal Procedure, 1973",
        "Section 41A",
        "Notice of appearance before police officer",
        "Bharatiya Nagarik Suraksha Sanhita, 2023",
        "Section 35(3)",
        "Notice of appearance before police officer",
        "Prior approval of Deputy Superintendent of Police required before arrest for offences < 3 years for vulnerable persons."
    ),
    "CRPC:437": ConcordanceEntry(
        "Code of Criminal Procedure, 1973",
        "Section 437",
        "When bail may be taken in case of non-bailable offence",
        "Bharatiya Nagarik Suraksha Sanhita, 2023",
        "Section 480",
        "When bail may be taken in case of non-bailable offence",
        "Discretionary bail parameters retained with enhanced electronic bond provisions."
    ),
    "CRPC:438": ConcordanceEntry(
        "Code of Criminal Procedure, 1973",
        "Section 438",
        "Direction for grant of bail to person apprehending arrest (Anticipatory Bail)",
        "Bharatiya Nagarik Suraksha Sanhita, 2023",
        "Section 482",
        "Direction for grant of bail to person apprehending arrest",
        "Powers of High Court and Court of Session for anticipatory bail preserved."
    ),
    "CRPC:439": ConcordanceEntry(
        "Code of Criminal Procedure, 1973",
        "Section 439",
        "Special powers of High Court or Court of Session regarding bail",
        "Bharatiya Nagarik Suraksha Sanhita, 2023",
        "Section 483",
        "Special powers of High Court or Court of Session regarding bail",
        "Regular bail powers of superior courts maintained."
    ),
    "CRPC:167": ConcordanceEntry(
        "Code of Criminal Procedure, 1973",
        "Section 167",
        "Procedure when investigation cannot be completed in twenty-four hours (Remand)",
        "Bharatiya Nagarik Suraksha Sanhita, 2023",
        "Section 187",
        "Procedure when investigation cannot be completed in twenty-four hours",
        "15-day police custody can now be taken in whole or parts across the first 40 or 60 days of detention."
    ),
    "CRPC:125": ConcordanceEntry(
        "Code of Criminal Procedure, 1973",
        "Section 125",
        "Order for maintenance of wives, children and parents",
        "Bharatiya Nagarik Suraksha Sanhita, 2023",
        "Section 144",
        "Order for maintenance of wives, children and parents",
        "Speedy monthly maintenance remedy preserved for deserted dependents."
    ),

    # ── Evidence Act 1872 -> BSA 2023 ──
    "IEA:65B": ConcordanceEntry(
        "Indian Evidence Act, 1872",
        "Section 65B",
        "Admissibility of electronic records",
        "Bharatiya Sakshya Adhiniyam, 2023",
        "Section 63",
        "Admissibility of electronic records",
        "Electronic/digital records elevated to primary evidence status with simplified certification schedules."
    ),
}


def lookup_concordance(act_name_or_code: str, section_number: str) -> Optional[ConcordanceEntry]:
    """Resolves a legacy statutory section reference (e.g. IPC 420, CrPC 154)
    to its active 2024 Bharatiya Sanhitas provision."""
    clean_sec = section_number.upper().replace("SECTION", "").replace("SEC", "").replace(".", "").strip()
    clean_act = act_name_or_code.upper()

    key_prefix = None
    if "IPC" in clean_act or "PENAL" in clean_act:
        key_prefix = "IPC"
    elif "CRPC" in clean_act or "CRIMINAL PROCEDURE" in clean_act:
        key_prefix = "CRPC"
    elif "EVIDENCE" in clean_act or "IEA" in clean_act:
        key_prefix = "IEA"

    if key_prefix:
        lookup_key = f"{key_prefix}:{clean_sec}"
        return CRIMINAL_CONCORDANCE.get(lookup_key)

    return None
