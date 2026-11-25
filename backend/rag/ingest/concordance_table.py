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
    "IPC:380": ConcordanceEntry(
        "Indian Penal Code, 1860",
        "Section 380",
        "Theft in dwelling house, etc.",
        "Bharatiya Nyaya Sanhita, 2023",
        "Section 305",
        "Theft in dwelling house, etc.",
        "Aggravated theft punishment up to 7 years imprisonment and fine."
    ),
    "IPC:384": ConcordanceEntry(
        "Indian Penal Code, 1860",
        "Section 384",
        "Punishment for extortion",
        "Bharatiya Nyaya Sanhita, 2023",
        "Section 308(2)",
        "Extortion",
        "Punishment up to 3 years imprisonment or fine or both."
    ),
    "IPC:406": ConcordanceEntry(
        "Indian Penal Code, 1860",
        "Section 406",
        "Punishment for criminal breach of trust",
        "Bharatiya Nyaya Sanhita, 2023",
        "Section 316(2)",
        "Criminal breach of trust",
        "Punishment up to 5 years imprisonment or fine or both."
    ),
    "IPC:409": ConcordanceEntry(
        "Indian Penal Code, 1860",
        "Section 409",
        "Criminal breach of trust by public servant, or by banker, merchant or agent",
        "Bharatiya Nyaya Sanhita, 2023",
        "Section 316(5)",
        "Criminal breach of trust by public servant, banker, merchant or agent",
        "Aggravated breach of trust punishable with life imprisonment or up to 10 years."
    ),
    "IPC:468": ConcordanceEntry(
        "Indian Penal Code, 1860",
        "Section 468",
        "Forgery for purpose of cheating",
        "Bharatiya Nyaya Sanhita, 2023",
        "Section 338",
        "Forgery for purpose of cheating",
        "Punishment up to 7 years imprisonment and fine retained."
    ),
    "IPC:471": ConcordanceEntry(
        "Indian Penal Code, 1860",
        "Section 471",
        "Using as genuine a forged document or electronic record",
        "Bharatiya Nyaya Sanhita, 2023",
        "Section 340",
        "Using as genuine a forged document or electronic record",
        "Punished in the same manner as if accused forged such document."
    ),
    "IPC:504": ConcordanceEntry(
        "Indian Penal Code, 1860",
        "Section 504",
        "Intentional insult with intent to provoke breach of the peace",
        "Bharatiya Nyaya Sanhita, 2023",
        "Section 352",
        "Intentional insult with intent to provoke breach of peace",
        "Punishment up to 2 years imprisonment or fine or both."
    ),
    "IPC:509": ConcordanceEntry(
        "Indian Penal Code, 1860",
        "Section 509",
        "Word, gesture or act intended to insult the modesty of a woman",
        "Bharatiya Nyaya Sanhita, 2023",
        "Section 79",
        "Word, gesture or act intended to insult modesty of woman",
        "Simple imprisonment up to 3 years and fine."
    ),
    "IPC:34": ConcordanceEntry(
        "Indian Penal Code, 1860",
        "Section 34",
        "Acts done by several persons in furtherance of common intention",
        "Bharatiya Nyaya Sanhita, 2023",
        "Section 3(5)",
        "Joint liability and common intention",
        "Joint criminal liability principle identical."
    ),
    "IPC:120B": ConcordanceEntry(
        "Indian Penal Code, 1860",
        "Section 120B",
        "Punishment of criminal conspiracy",
        "Bharatiya Nyaya Sanhita, 2023",
        "Section 61(2)",
        "Criminal conspiracy",
        "Conspiracy principles preserved under Chapter IV: Abetment and Criminal Conspiracy."
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
    "CRPC:161": ConcordanceEntry(
        "Code of Criminal Procedure, 1973",
        "Section 161",
        "Examination of witnesses by police",
        "Bharatiya Nagarik Suraksha Sanhita, 2023",
        "Section 180",
        "Examination of witnesses by police",
        "Audio-video electronic means of recording statements introduced."
    ),
    "CRPC:164": ConcordanceEntry(
        "Code of Criminal Procedure, 1973",
        "Section 164",
        "Recording of confessions and statements",
        "Bharatiya Nagarik Suraksha Sanhita, 2023",
        "Section 183",
        "Recording of confessions and statements",
        "Audio-video electronic recording of victim statement in sexual offences mandatory."
    ),
    "CRPC:173": ConcordanceEntry(
        "Code of Criminal Procedure, 1973",
        "Section 173",
        "Report of police officer on completion of investigation (Charge Sheet)",
        "Bharatiya Nagarik Suraksha Sanhita, 2023",
        "Section 193",
        "Report of police officer on completion of investigation",
        "Mandatory 90-day progress reporting to informant and electronic submission of police report."
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
    "IEA:27": ConcordanceEntry(
        "Indian Evidence Act, 1872",
        "Section 27",
        "How much of information received from accused may be proved",
        "Bharatiya Sakshya Adhiniyam, 2023",
        "Section 23",
        "Discovery statement of accused",
        "Fact discovered in consequence of information received from person in police custody may be proved."
    ),
    "IEA:114A": ConcordanceEntry(
        "Indian Evidence Act, 1872",
        "Section 114A",
        "Presumption as to absence of consent in certain prosecution for rape",
        "Bharatiya Sakshya Adhiniyam, 2023",
        "Section 119",
        "Presumption as to absence of consent in certain prosecutions for rape",
        "Statutory presumption of absence of consent maintained."
    ),

    # ── ADDITIONAL COMPREHENSIVE IPC -> BNS CONCORDANCE ──
    "IPC:304B": ConcordanceEntry(
        "Indian Penal Code, 1860", "Section 304B", "Dowry death",
        "Bharatiya Nyaya Sanhita, 2023", "Section 80", "Dowry death",
        "Re-enacted with identical 7-year minimum and life maximum imprisonment."
    ),
    "IPC:307": ConcordanceEntry(
        "Indian Penal Code, 1860", "Section 307", "Attempt to murder",
        "Bharatiya Nyaya Sanhita, 2023", "Section 109", "Attempt to murder",
        "Re-enacted with imprisonment up to 10 years or life if hurt caused."
    ),
    "IPC:323": ConcordanceEntry(
        "Indian Penal Code, 1860", "Section 323", "Voluntarily causing hurt",
        "Bharatiya Nyaya Sanhita, 2023", "Section 115(2)", "Voluntarily causing hurt",
        "Re-enacted with community service option added."
    ),
    "IPC:325": ConcordanceEntry(
        "Indian Penal Code, 1860", "Section 325", "Voluntarily causing grievous hurt",
        "Bharatiya Nyaya Sanhita, 2023", "Section 116(2)", "Voluntarily causing grievous hurt",
        "Re-enacted with up to 7 years imprisonment."
    ),
    "IPC:354A": ConcordanceEntry(
        "Indian Penal Code, 1860", "Section 354A", "Sexual harassment",
        "Bharatiya Nyaya Sanhita, 2023", "Section 75", "Sexual harassment",
        "Re-enacted under Chapter V Crimes Against Women."
    ),
    "IPC:354C": ConcordanceEntry(
        "Indian Penal Code, 1860", "Section 354C", "Voyeurism",
        "Bharatiya Nyaya Sanhita, 2023", "Section 77", "Voyeurism",
        "Re-enacted with electronic media dissemination explicitly covered."
    ),
    "IPC:354D": ConcordanceEntry(
        "Indian Penal Code, 1860", "Section 354D", "Stalking",
        "Bharatiya Nyaya Sanhita, 2023", "Section 78", "Stalking",
        "Re-enacted with electronic/internet monitoring explicitly covered."
    ),
    "IPC:376": ConcordanceEntry(
        "Indian Penal Code, 1860", "Section 376", "Rape",
        "Bharatiya Nyaya Sanhita, 2023", "Section 64", "Rape",
        "Re-enacted under Chapter V Crimes Against Women."
    ),
    "IPC:379": ConcordanceEntry(
        "Indian Penal Code, 1860", "Section 379", "Theft",
        "Bharatiya Nyaya Sanhita, 2023", "Section 303(2)", "Theft",
        "Re-enacted with community service for petty theft first offence."
    ),
    "IPC:392": ConcordanceEntry(
        "Indian Penal Code, 1860", "Section 392", "Robbery",
        "Bharatiya Nyaya Sanhita, 2023", "Section 309(4)", "Robbery",
        "Re-enacted with rigorous imprisonment up to 10 years."
    ),
    "IPC:395": ConcordanceEntry(
        "Indian Penal Code, 1860", "Section 395", "Dacoity",
        "Bharatiya Nyaya Sanhita, 2023", "Section 310(2)", "Dacoity",
        "Re-enacted with life imprisonment or rigorous imprisonment up to 10 years."
    ),
    "IPC:406": ConcordanceEntry(
        "Indian Penal Code, 1860", "Section 406", "Criminal breach of trust",
        "Bharatiya Nyaya Sanhita, 2023", "Section 316(2)", "Criminal breach of trust",
        "Re-enacted with imprisonment up to 5 years (enhanced from 3 years)."
    ),
    "IPC:468": ConcordanceEntry(
        "Indian Penal Code, 1860", "Section 468", "Forgery for purpose of cheating",
        "Bharatiya Nyaya Sanhita, 2023", "Section 336(3)", "Forgery for purpose of cheating",
        "Re-enacted with imprisonment up to 7 years and fine."
    ),
    "IPC:471": ConcordanceEntry(
        "Indian Penal Code, 1860", "Section 471", "Using as genuine a forged document",
        "Bharatiya Nyaya Sanhita, 2023", "Section 340(2)", "Using forged document as genuine",
        "Re-enacted punishable in same manner as if accused forged document."
    ),
    "IPC:504": ConcordanceEntry(
        "Indian Penal Code, 1860", "Section 504", "Intentional insult with intent to provoke breach of peace",
        "Bharatiya Nyaya Sanhita, 2023", "Section 352", "Intentional insult to provoke breach of peace",
        "Re-enacted with up to 2 years imprisonment or community service."
    ),
    "IPC:506": ConcordanceEntry(
        "Indian Penal Code, 1860", "Section 506", "Criminal intimidation",
        "Bharatiya Nyaya Sanhita, 2023", "Section 351(2)", "Criminal intimidation",
        "Re-enacted with up to 2 years or 7 years if threat to cause death."
    ),
    "IPC:279": ConcordanceEntry(
        "Indian Penal Code, 1860", "Section 279", "Rash driving or riding on a public way",
        "Bharatiya Nyaya Sanhita, 2023", "Section 281", "Rash driving on public way",
        "Re-enacted with imprisonment up to 6 months and fine up to Rs 1,000."
    ),
    "IPC:304A": ConcordanceEntry(
        "Indian Penal Code, 1860", "Section 304A", "Causing death by negligence",
        "Bharatiya Nyaya Sanhita, 2023", "Section 106(1)", "Causing death by negligence",
        "Re-enacted with imprisonment up to 5 years (2 years for medical practitioners)."
    ),

    # ── ADDITIONAL COMPREHENSIVE CRPC -> BNSS CONCORDANCE ──
    "CRPC:41A": ConcordanceEntry(
        "Code of Criminal Procedure, 1973", "Section 41A", "Notice of appearance before police",
        "Bharatiya Nagarik Suraksha Sanhita, 2023", "Section 35(3)", "Notice of appearance before police",
        "Mandatory written notice prior to arrest in offences up to 7 years imprisonment."
    ),
    "CRPC:82": ConcordanceEntry(
        "Code of Criminal Procedure, 1973", "Section 82", "Proclamation for person absconding",
        "Bharatiya Nagarik Suraksha Sanhita, 2023", "Section 84", "Proclamation for person absconding",
        "Re-enacted with 30-day notice requirement for absconding accused."
    ),
    "CRPC:83": ConcordanceEntry(
        "Code of Criminal Procedure, 1973", "Section 83", "Attachment of property of person absconding",
        "Bharatiya Nagarik Suraksha Sanhita, 2023", "Section 85", "Attachment of property of absconder",
        "Re-enacted with attachment of movable and immovable properties."
    ),
    "CRPC:91": ConcordanceEntry(
        "Code of Criminal Procedure, 1973", "Section 91", "Summons to produce document or other thing",
        "Bharatiya Nagarik Suraksha Sanhita, 2023", "Section 94", "Summons to produce document or thing",
        "Re-enacted with digital and electronic records explicitly included."
    ),
    "CRPC:161": ConcordanceEntry(
        "Code of Criminal Procedure, 1973", "Section 161", "Examination of witnesses by police",
        "Bharatiya Nagarik Suraksha Sanhita, 2023", "Section 180", "Examination of witnesses by police",
        "Re-enacted with permission for audio-video electronic recording."
    ),
    "CRPC:164": ConcordanceEntry(
        "Code of Criminal Procedure, 1973", "Section 164", "Recording of confessions and statements",
        "Bharatiya Nagarik Suraksha Sanhita, 2023", "Section 183", "Recording of confessions and statements",
        "Re-enacted with mandatory audio-video recording for sexual assault victims."
    ),
    "CRPC:167": ConcordanceEntry(
        "Code of Criminal Procedure, 1973", "Section 167", "Remand and default bail",
        "Bharatiya Nagarik Suraksha Sanhita, 2023", "Section 187", "Remand and detention in custody",
        "Police custody up to 15 days in whole or in parts during first 40 or 60 days."
    ),
    "CRPC:173": ConcordanceEntry(
        "Code of Criminal Procedure, 1973", "Section 173", "Report of police officer on completion of investigation",
        "Bharatiya Nagarik Suraksha Sanhita, 2023", "Section 193", "Police report on completion of investigation",
        "Chargesheet filing with mandatory progress update to victim within 90 days."
    ),
    "CRPC:320": ConcordanceEntry(
        "Code of Criminal Procedure, 1973", "Section 320", "Compounding of offences",
        "Bharatiya Nagarik Suraksha Sanhita, 2023", "Section 359", "Compounding of offences",
        "Re-enacted with revised schedule of compoundable offences."
    ),
    "CRPC:437": ConcordanceEntry(
        "Code of Criminal Procedure, 1973", "Section 437", "When bail may be taken in non-bailable offence",
        "Bharatiya Nagarik Suraksha Sanhita, 2023", "Section 480", "Bail in non-bailable offences by Magistrate",
        "Re-enacted with liberal release for women, sick, infirm, or under-16 accused."
    ),
    "CRPC:439": ConcordanceEntry(
        "Code of Criminal Procedure, 1973", "Section 439", "Special powers of High Court or Sessions Court regarding bail",
        "Bharatiya Nagarik Suraksha Sanhita, 2023", "Section 483", "Special powers of High Court or Sessions regarding bail",
        "Re-enacted preserving inherent discretionary jurisdiction over regular and anticipatory bail."
    ),

    # ── ADDITIONAL COMPREHENSIVE IEA -> BSA CONCORDANCE ──
    "IEA:25": ConcordanceEntry(
        "Indian Evidence Act, 1872", "Section 25", "Confession to police officer not to be proved",
        "Bharatiya Sakshya Adhiniyam, 2023", "Section 23(1)", "Confession to police officer inadmissible",
        "Re-enacted barring admission of confession made to police officer."
    ),
    "IEA:45": ConcordanceEntry(
        "Indian Evidence Act, 1872", "Section 45", "Opinions of experts",
        "Bharatiya Sakshya Adhiniyam, 2023", "Section 39", "Opinions of experts",
        "Re-enacted with digital forensic and cyber experts explicitly recognized."
    ),
    "IEA:113A": ConcordanceEntry(
        "Indian Evidence Act, 1872", "Section 113A", "Presumption as to abetment of suicide by married woman",
        "Bharatiya Sakshya Adhiniyam, 2023", "Section 116", "Presumption as to abetment of suicide by married woman",
        "Re-enacted within 7 years of marriage if cruelty proven."
    ),
    "IEA:113B": ConcordanceEntry(
        "Indian Evidence Act, 1872", "Section 113B", "Presumption as to dowry death",
        "Bharatiya Sakshya Adhiniyam, 2023", "Section 117", "Presumption as to dowry death",
        "Re-enacted: court shall presume dowry death if woman subjected to cruelty soon before death."
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
