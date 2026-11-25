"""Multilingual Legal Query Rewriting, Normalization & Concordance Expansion Module."""

import re
from typing import Dict, List, Optional, Tuple, NamedTuple, Set

from rag.ingest.concordance_table import lookup_concordance


class RewrittenQuery(NamedTuple):
    original_query: str
    normalized_query: str
    expanded_query: str
    detected_language: str  # en | kn | hi | mixed
    legacy_concordance_detected: Optional[str]  # e.g. "IPC 420 -> BNS Section 318(4)"
    is_out_of_scope: bool
    domain_tags: List[str]


# ── Complete 37 Hierarchical Legal Domains ──
LEGAL_DOMAINS: List[str] = [
    "CONSTITUTIONAL_LAW",
    "CRIMINAL_LAW",
    "CRIMINAL_PROCEDURE",
    "EVIDENCE_LAW",
    "CIVIL_LAW",
    "CIVIL_PROCEDURE",
    "PROPERTY_LAW",
    "LAND_REVENUE",
    "LAND_REGISTRATION",
    "REAL_ESTATE",
    "TENANCY",
    "INHERITANCE",
    "FAMILY_LAW",
    "WOMEN_AND_CHILD_RIGHTS",
    "CONSUMER_PROTECTION",
    "LABOUR_EMPLOYMENT",
    "BANKING_FINANCE",
    "INSURANCE",
    "CYBERCRIME",
    "DATA_PRIVACY",
    "CORPORATE_LAW",
    "COMMERCIAL_LAW",
    "CONTRACT_LAW",
    "INTELLECTUAL_PROPERTY",
    "MOTOR_VEHICLE_LAW",
    "MEDICAL_LAW",
    "ENVIRONMENTAL_LAW",
    "AGRICULTURAL_LAW",
    "TAXATION",
    "IMMIGRATION",
    "ADMINISTRATIVE_LAW",
    "GOVERNMENT_SERVICES",
    "EDUCATION_LAW",
    "SOCIAL_WELFARE",
    "LEGAL_AID",
    "DISPUTE_RESOLUTION",
    "LOCAL_MUNICIPAL_LAW",
]


# ── Domain synonym expansions for Indian law ──
SYNONYM_EXPANSIONS: Dict[str, List[str]] = {
    # ── Property, Land, Titles & Revenue ──
    "khata": ["khata transfer", "e-Khata", "A-Khata", "B-Khata", "Section 114 KMC Act", "property tax register", "revenue assessment", "BBMP e-aasti"],
    "a-khata": ["A-Khata", "sanctioned plan", "occupancy certificate", "authorized layout", "BDA layout", "KMC Act 1976"],
    "b-khata": ["B-Khata", "revenue land tax register", "Form B", "unapproved layout", "Section 108A KMC Act", "Akrama Sakrama"],
    "e-khata": ["e-Khata", "e-Aasthi", "Bhoomi e-Pattadar", "digital property certificate", "GPS property mapping"],
    "pahani": ["RTC", "Pahani", "Form 16", "Record of Rights Tenancy and Crop Inspection", "Section 133 Karnataka Land Revenue Act", "presumption of truth"],
    "rtc": ["RTC", "Pahani", "Karnataka Land Revenue Act Section 133", "Bhoomi online", "revenue record", "land possession column"],
    "mutation": ["mutation extract", "Form 12", "J-Slip", "Section 128 Karnataka Land Revenue Act", "Section 129", "acquisition of rights", "Pouthi mutation"],
    "pouthi": ["Pouthi mutation", "inheritance mutation", "Vamshavruksha", "legal heir certificate", "Section 128 KLRA"],
    "phodi": ["Phodi", "land subdivision", "Durasti", "Survey 11E sketch", "Bhoomi Phodi Muktha", "Bhoomi Mojini", "Section 106 KLRA"],
    "durasti": ["Durasti", "survey boundary rectification", "Tippani", "Akarband", "Bhoomi survey", "Tahsildar survey"],
    "patta": ["Patta", "Title deed", "Record of Rights", "land grant", "revenue assignment"],
    "encumbrance": ["encumbrance certificate", "Form 15", "Form 16", "Nil Encumbrance", "Kaveri 2.0", "registered transactions search", "mortgage search"],
    "ec": ["Encumbrance Certificate", "Form 15", "Form 16", "Kaveri portal", "Inspector General of Registration"],
    "sale deed": ["Sale deed", "conveyance deed", "Section 54 Transfer of Property Act", "mandatory registration Section 17 Registration Act", "stamp duty"],
    "agreement to sell": ["agreement to sell", "Section 53A Transfer of Property Act", "part performance", "specific performance Section 10 SRA"],
    "gift deed": ["Gift deed", "Section 122 Transfer of Property Act", "Section 123 TPA", "acceptance during lifetime", "registered gift"],
    "release deed": ["Release deed", "Relinquishment deed", "coparcenary relinquishment", "Article 44 Karnataka Stamp Act", "family settlement"],
    "partition": ["Partition deed", "Partition suit", "Section 6 Hindu Succession Act", "coparcenary property", "preliminary decree", "final decree", "Order 20 Rule 18 CPC"],
    "ancestral": ["ancestral property", "coparcenary", "Section 6 Hindu Succession Act", "partition suit", "daughters rights in property", "Vamshavruksha", "Vineeta Sharma"],
    "self acquired": ["self-acquired property", "absolute ownership", "Section 30 Hindu Succession Act", "testamentary disposition", "will"],
    "power of attorney": ["Power of Attorney", "GPA", "SPA", "Powers of Attorney Act 1882", "Suraj Lamp judgment", "GPA does not convey title"],
    "gpa": ["General Power of Attorney", "Suraj Lamp v State of Haryana", "GPA sale invalid title", "agent authority"],
    "conversion": ["agricultural to non-agricultural conversion", "Section 95 Karnataka Land Revenue Act", "Deputy Commissioner conversion order", "DC conversion"],
    "ptcl": ["PTCL Act 1978", "Section 4 PTCL", "Section 5 resumption", "prohibition of transfer of granted land", "SC ST land alienation", "Nekkanti Rama Lakshmi"],
    "land grabbing": ["Karnataka Land Grabbing Prohibition Act 2011", "Special Court for Land Grabbing", "encroachment of government land", "imprisonment"],
    "encroachment": ["encroachment", "trespass", "boundary dispute", "Section 104 KLRA", "eviction of unauthorized occupant", "injunction"],
    "adverse possession": ["adverse possession", "Article 65 Limitation Act 1963", "12 years continuous peaceful possession", "Ravinder Kaur Grewal v Manjit Kaur", "hostile title"],
    "easement": ["Indian Easements Act 1882", "Section 4 easement definition", "Section 15 easement by prescription", "pathway right", "right of way", "light and air"],
    "pathway": ["pathway right", "easement of necessity Section 13", "cart track", "prescriptive right of way Section 15 Easements Act"],
    "injunction": ["temporary injunction Order 39 Rules 1 2 CPC", "permanent injunction Section 38 Specific Relief Act", "settled possession Rame Gowda"],
    "declaration": ["declaration of title", "Section 34 Specific Relief Act", "Anathula Sudhakar v P Buchi Reddy", "cloud on title"],
    "specific performance": ["Specific Performance of Contract", "Section 10 Specific Relief Act", "Section 16 ready and willing", "Article 54 Limitation Act 3 years"],

    # ── Real Estate, RERA & Construction ──
    "rera": ["Real Estate Regulation and Development Act 2016", "Section 18 RERA refund and interest", "Section 14 structural defects", "Section 31 complaint", "KRERA"],
    "builder delay": ["builder delay in possession", "Section 18 RERA", "interest for delay", "refund with interest", "Imperia Structures v Anil Patni"],
    "occupancy certificate": ["Occupancy Certificate", "OC", "Completion Certificate", "Section 19 RERA", "possession without OC illegal"],
    "undivided share": ["Undivided Share of Land", "UDS", "Karnataka Apartment Ownership Act 1972", "common areas and facilities"],
    "apartment": ["Karnataka Apartment Ownership Act 1972", "Deed of Declaration", "association of apartment owners", "maintenance charges", "common parking"],

    # ── Tenancy & Leases ──
    "deposit": ["security deposit", "advance", "refund", "wear and tear", "Section 108 TPA", "Section 27 Karnataka Rent Act", "tenancy"],
    "landlord": ["lessor", "tenant", "rent agreement", "eviction", "Karnataka Rent Act", "handover possession", "repairs"],
    "tenant": ["rent agreement", "possession", "Section 108 Transfer of Property Act", "Section 27 Karnataka Rent Act", "Model Tenancy Act"],
    "rent": ["Karnataka Rent Act", "Section 27 eviction protection", "Section 14 premises repairs", "Section 108 TPA", "security deposit"],
    "repair": ["repair of premises", "Section 14 Karnataka Rent Act", "landlord obligation to maintain", "tenant repairs deduction"],
    "wear and tear": ["normal wear and tear", "painting deduction", "Section 108 TPA", "security deposit refund"],
    "eviction": ["Section 27 Karnataka Rent Act", "unlawful eviction", "due process of law", "formal eviction petition Rent Court"],

    # ── Cheque Bounce & Banking ──
    "cheque": ["dishonour of cheque", "bounced cheque", "Section 138 Negotiable Instruments Act", "bank return memo", "30 days notice", "Section 142 NI Act"],
    "bounce": ["Section 138 Negotiable Instruments Act", "dishonour", "bank return memo", "30 days legal notice"],
    "138": ["Section 138 Negotiable Instruments Act", "dishonour of cheque", "bank memo date", "statutory demand notice", "limitation one month"],
    "142": ["Section 142 Negotiable Instruments Act", "cognizance of offences", "one month limitation", "jurisdiction magistrate"],
    "sarfaesi": ["SARFAESI Act 2002", "Section 13(2) notice 60 days", "Section 13(4) possession", "DRT appeal Section 17", "bank auction"],
    "loan harassment": ["loan recovery agent harassment", "RBI Fair Practices Code", "recovery agents guidelines", "police extortion complaint"],
    "ombudsman": ["RBI Integrated Ombudsman Scheme", "banking ombudsman complaint", "unauthorized transaction deficiency", "CMS portal"],

    # ── Criminal Law & Procedures (BNSS / BNS / BSA) ──
    "arrest": ["Article 22 Constitution", "grounds of arrest", "24 hours magistrate", "DK Basu guidelines", "Section 35 BNSS", "memo of arrest", "police custody"],
    "police": ["FIR", "Zero FIR", "Section 173 BNSS", "refusal to register FIR", "Superintendent of Police", "cognizable offence", "Lalita Kumari"],
    "fir": ["Section 173 BNSS", "First Information Report", "Zero FIR", "cognizable offence", "police station jurisdiction", "mandatory FIR Lalita Kumari"],
    "zero fir": ["Zero FIR", "Section 173(1) BNSS", "jurisdiction anywhere", "immediate registration transfer later"],
    "bail": ["anticipatory bail", "Section 482 BNSS", "regular bail", "Section 480 BNSS", "non bailable offence", "Satender Kumar Antil categories"],
    "anticipatory bail": ["Section 482 BNSS", "apprehension of arrest", "Sessions Court High Court", "conditions for pre-arrest bail"],
    "cheating": ["Section 318(4) BNS 2023", "cheating and dishonestly inducing delivery", "IPC 420 equivalent", "criminal breach of trust Section 316"],
    "420": ["Section 318(4) Bharatiya Nyaya Sanhita 2023", "cheating", "fraud", "delivery of property"],
    "theft": ["Section 303 BNS 2023", "theft", "dishonest taking of movable property", "IPC 379 equivalent"],
    "assault": ["Section 115 BNS 2023", "voluntarily causing hurt", "grievous hurt Section 117 BNS", "IPC 323 325 equivalent"],
    "forgery": ["Section 336 BNS 2023", "making a false document", "forgery for cheating Section 338", "IPC 468 equivalent"],
    "domestic violence": ["Protection of Women from Domestic Violence Act 2005", "Section 18 PWDVA protection order", "Section 19 residence order", "Section 85 BNS"],
    "498a": ["Section 85 Bharatiya Nyaya Sanhita 2023", "cruelty by husband or relatives", "IPC 498A equivalent", "Arnesh Kumar notice"],
    "cybercrime": ["Information Technology Act 2000", "Section 66C identity theft", "Section 66D cheating by personation", "Helpline 1930", "cybercrime.gov.in"],
    "otp fraud": ["UPI fraud", "Section 66D IT Act", "cyber financial fraud", "freeze transaction within golden hour Helpline 1930"],

    # ── Family Law & Succession ──
    "divorce": ["Section 13B Hindu Marriage Act", "mutual consent divorce", "cooling off period six months", "mediation", "Section 13 contested grounds"],
    "mutual consent": ["Section 13B Hindu Marriage Act", "living separately 1 year", "first motion second motion", "cooling off waiver Amardeep Singh"],
    "maintenance": ["Section 144 BNSS", "maintenance of wife children parents", "desertion", "Section 24 HMA", "Rajnesh v Neha affidavit"],
    "child custody": ["Guardians and Wards Act 1890", "welfare of the child paramount", "custody petition Family Court", "visitation rights"],

    # ── Consumer Protection ──
    "consumer": ["Consumer Protection Act 2019", "Section 35 CPA", "District Commission", "e-Daakhil", "e-Jagriti", "deficiency in service", "product liability"],
    "deficiency": ["deficiency in service", "Section 2(11) Consumer Protection Act", "refund", "compensation", "unfair trade practice"],
    "e-daakhil": ["e-Daakhil", "e-Jagriti", "consumer complaint online", "Section 35 Consumer Protection Act", "District Commission"],

    # ── Labour & Employment ──
    "salary": ["unpaid salary", "Code on Wages 2019", "Payment of Wages Act 1936", "labour commissioner complaint", "summary recovery"],
    "termination": ["wrongful termination", "Section 25F Industrial Disputes Act", "retrenchment compensation", "notice pay", "Industrial Relations Code"],
    "gratuity": ["Payment of Gratuity Act 1972", "Section 4 gratuity entitlement", "5 years continuous service", "15 days wages per year"],
    "posh": ["POSH Act 2013", "Internal Complaints Committee ICC", "Section 4 POSH", "Section 9 complaint 90 days", "workplace harassment"],
    "non compete": ["Section 27 Indian Contract Act", "agreement in restraint of trade", "void agreement", "employment contract non-compete"],

    # ── Motor Vehicle & Accidents ──
    "accident": ["Motor Vehicles Act 1988", "Section 166 MACT claim", "Motor Accidents Claims Tribunal", "no fault liability Section 164", "third party insurance"],
    "mact": ["Motor Accidents Claims Tribunal", "Section 166 MV Act", "accident compensation", "limitation 6 months Section 166(3)"],
    "drink and drive": ["Motor Vehicles Act 1988", "Section 185 MVA", "drunk driving", "breath analyser", "fine 10000", "blood alcohol 30mg", "licence suspension"],
    "drunk driving": ["Section 185 Motor Vehicles Act", "breath analyser", "fine 10000", "imprisonment six months", "driving licence disqualification"],
    "traffic": ["Motor Vehicles Act 1988", "Section 194", "traffic police fine", "challan", "Section 200 compounding", "helmet fine", "seatbelt penalty"],
    "challan": ["traffic challan", "Section 200 Motor Vehicles Act", "e-challan parivahan", "virtual court", "compounding fee receipt"],
    "traffic police": ["Motor Vehicles Act", "Section 194", "traffic challan", "Section 200 compounding", "spot fine receipt"],
    "traffic fine": ["Motor Vehicles Act Section 194", "Section 200 compounding", "official printed receipt", "virtual court challan"],

    # ── Summons, Notices & Process ──
    "summon": ["court summons", "Section 63 BNSS", "Section 64 BNSS", "notice of appearance Section 35", "duplicate copy signed", "witness or accused", "warrant prevention"],
    "summons": ["court summons", "Section 63 BNSS", "Section 64 BNSS", "Order V CPC", "notice of appearance", "30 days written statement", "warrant"],
    "legal summon": ["court summons", "Section 63 BNSS", "Order V CPC", "written statement 30 days", "advocate representation", "warrant"],
    "warrant": ["bailable warrant", "non bailable warrant", "Section 72 BNSS", "magistrate court", "appearance"],

    # ── Plot & Land Conveyancing ──
    "plot": ["plot ownership", "Section 128 Karnataka Land Revenue Act", "Section 54 Transfer of Property Act", "mutation", "khata transfer", "sale deed"],
    "plot owner": ["change of plot owner", "Section 128 Karnataka Land Revenue Act", "mutation Form 12", "Section 54 TPA", "e-Khata transfer", "sale deed registration"],
    "plot ownership": ["change of plot owner", "Section 128 KLRA", "Section 129 mutation", "Section 54 TPA", "registered sale deed", "e-Aasthi"],

    # ── Civil Procedure & Legal Aid ──
    "limitation": ["Limitation Act 1963", "Article 54 specific performance 3 years", "Section 5 condonation of delay", "statutory deadline"],
    "rti": ["Right to Information Act 2005", "Section 7 RTI", "30 days information", "48 hours life liberty", "First Appeal Section 19"],
    "free legal aid": ["NALSA", "KSLSA", "DLSA", "Helpline 15100", "Section 12 Legal Services Authorities Act", "free advocate representation"],
    "lok adalat": ["National Lok Adalat", "Section 21 Legal Services Authorities Act", "award deemed civil court decree", "court fee refund", "no appeal"],
}


# ── Extensive Multilingual Legal Glossary (500+ items across Kannada, Hindi, English, Transliterations) ──
VERNACULAR_MAPPINGS: Dict[str, str] = {
    # ── KANNADA (ಕನ್ನಡ) & KANGLISH PROPERTY / REVENUE TERMS ──
    "ಖಾತಾ": "khata transfer e-Khata A-Khata B-Khata property tax register Section 114 KMC Act",
    "ಇ-ಖಾತಾ": "e-Khata digital property certificate e-Aasthi Bhoomi",
    "ಪಹಣಿ": "Pahani RTC Form 16 Section 133 Karnataka Land Revenue Act possession record",
    "ಆರ್‌ಟಿಸಿ": "RTC Pahani Section 133 Karnataka Land Revenue Act Bhoomi land record",
    "ಪೌತಿ": "Pouthi mutation inheritance transfer Section 128 KLRA legal heir Vamshavruksha",
    "ದುರಸ್ತಿ": "Durasti survey rectification boundary Phodi Bhoomi Mojini",
    "ಪೋಡಿ": "Phodi land subdivision 11E sketch Section 106 Karnataka Land Revenue Act",
    "ಕ್ರಯಪತ್ರ": "Sale deed Section 54 Transfer of Property Act Section 17 Registration Act",
    "ದಾನಪತ್ರ": "Gift deed Section 122 Transfer of Property Act registered gift",
    "ವಿಭಾಗ ಪತ್ರ": "Partition deed coparcenary property Section 6 Hindu Succession Act",
    "ಹಕ್ಕು ಬಿಡುಗಡೆ": "Release deed relinquishment deed coparcenary family settlement",
    "ಋಣಭಾರ": "Encumbrance Certificate EC Form 15 Form 16 Kaveri portal",
    "ಗೋಮಾಳ": "Gomal land pasture land government land restriction KLRA",
    "ಖರಾಬು": "Kharab land A-Kharab B-Kharab government land road buffer",
    "ಒತ್ತುವರಿ": "encroachment land grabbing Karnataka Land Grabbing Prohibition Act 2011",
    "ದಾರಿ": "pathway right easement of necessity Section 13 Indian Easements Act",
    "ಈಸ್‌ಮೆಂಟ್": "Indian Easements Act 1882 pathway right prescriptive right of way",
    "ವಂಶವೃಕ್ಷ": "Vamshavruksha genealogy tree legal heir certificate revenue department",
    "ದಾವೆ": "civil suit plaint declaration of title partition suit CPC",
    "ತಡೆಯಾಜ್ಞೆ": "injunction temporary injunction Order 39 Rules 1 2 CPC Section 38 SRA",
    "ಕೃಷಿ ಜಮೀನು": "agricultural land Karnataka Land Reforms Act Section 79 Section 95 conversion",
    "ಪರಿವರ್ತನೆ": "land conversion Section 95 Karnataka Land Revenue Act DC conversion",
    "ಪಿಟಿಸಿಎಲ್": "PTCL Act 1978 Section 4 prohibition of transfer of SC ST granted land",
    "ಗ್ರಾಮಠಾಣ": "Grama Tana rural property e-Swathu Form 9 Form 11 Gram Panchayat",
    "ಇ-ಸ್ವತ್ತು": "e-Swathu rural property certificate Form 9 Form 11 Gram Panchayat",
    "ಕಾವೇರಿ": "Kaveri 2.0 property registration encumbrance certificate certified copy",
    "ಭೂಮಿ": "Bhoomi Karnataka land records portal RTC mutation extract Form 12",
    "ಮೋಜಣಿ": "Bhoomi Mojini land survey 11E sketch pre-mutation sketch",
    "ಅನಧಿಕೃತ": "unauthorized construction building plan violation Section 321 KMC Act",
    "ರೇರಾ": "KRERA Real Estate Regulation and Development Act Section 18 builder delay refund",
    "ಠೇವಣಿ": "security deposit tenancy refund Karnataka Rent Act Section 27 Section 108 TPA",
    "ಭದ್ರತಾ": "security deposit advance tenancy Karnataka Rent Act Section 27",
    "ಮಾಲೀಕ": "landlord tenancy lessor possession Karnataka Rent Act",
    "ಬಾಡಿಗೆ": "tenancy rent agreement Section 27 Karnataka Rent Act Section 108 TPA Section 14",
    "ಖಾಲಿ": "vacating premises surrender possession tenancy deposit refund Section 27",
    "ಸವೆತ": "normal wear and tear painting deduction Section 108 TPA deposit refund",
    "ಅಪಾರ್ಟ್‌ಮೆಂಟ್": "Karnataka Apartment Ownership Act 1972 common areas Deed of Declaration",

    # ── KANNADA CRIMINAL, FAMILY, LABOUR, BANKING ──
    "ಚೆಕ್": "cheque bounce Section 138 Negotiable Instruments Act",
    "ಬೌನ್ಸ್": "dishonour cheque Section 138 bank memo 30 days notice Section 142",
    "ಅಮಾನ್ಯ": "dishonour cheque Section 138 Negotiable Instruments Act",
    "ಮೆಮೊ": "bank return memo Section 138 Negotiable Instruments Act 30 days",
    "ಬಂಧನ": "arrest Article 22 Constitution 24 hours magistrate BNSS Section 35 DK Basu",
    "ಪೊಲೀಸ್": "police FIR Zero FIR Section 173 BNSS complaint",
    "ಎಫ್‌ಐಆರ್": "FIR Zero FIR Section 173 BNSS First Information Report Lalita Kumari",
    "ಶೂನ್ಯ ಎಫ್‌ಐಆರ್": "Zero FIR Section 173(1) BNSS jurisdiction anywhere",
    "ನಿರಾಕರಿಸಿದರೆ": "refusal to register FIR Section 173 BNSS Superintendent of Police",
    "ಜಾಮೀನು": "anticipatory bail Section 482 BNSS regular bail Section 480 BNSS",
    "ನಿರೀಕ್ಷಣಾ": "anticipatory bail Section 482 BNSS pre arrest bail",
    "ಆಸ್ತಿ": "ancestral property partition Hindu Succession Act Section 6 coparcenary",
    "ಪೂರ್ವಜರ": "ancestral coparcenary daughters property rights Section 6 Hindu Succession Act",
    "ವಿಭಾಗ": "partition suit ancestral property coparcenary Section 6",
    "ವಿಚ್ಛೇದನ": "divorce mutual consent Hindu Marriage Act Section 13B",
    "ಪರಸ್ಪರ": "mutual consent divorce Section 13B Hindu Marriage Act 6 months",
    "ಜೀವನಾಂಶ": "maintenance Section 144 BNSS family court wives children Rajnesh v Neha",
    "ಗೃಹಹಿಂಸೆ": "domestic violence Protection of Women from Domestic Violence Act Section 18 PWDVA",
    "ಹಿಂಸೆ": "domestic violence Protection of Women from Domestic Violence Act Section 18",
    "ವರದಕ್ಷಿಣೆ": "Dowry Prohibition Act Section 85 BNS Section 86 BNS",
    "ಗ್ರಾಹಕ": "consumer protection Section 35 CPA District Commission e-Daakhil deficiency",
    "ದೋಷಪೂರಿತ": "defective product deficiency in service Consumer Protection Act",
    "ಮಾಹಿತಿ ಹಕ್ಕು": "Right to Information Act 2005 Section 7 RTI 30 days 48 hours",
    "ಉಚಿತ ಕಾನೂನು ನೆರವು": "free legal aid NALSA KSLSA helpline 15100 Article 39A",
    "ಸಹಾಯವಾಣಿ": "helpline 15100 NALSA free legal aid DLSA",
    "ಕಾಲಮಿತಿ": "limitation period Limitation Act 1963 Article 54 Section 142 NI Act",
    "ಕರಾರು": "agreement contract Section 27 Indian Contract Act restraint of trade",
    "ವೇತನ": "unpaid salary Code on Wages Payment of Wages Act labour commissioner",
    "ಉಪಧನ": "gratuity Payment of Gratuity Act Section 4 continuous service 5 years",
    "ಲೋಕ ಅದಾಲತ್": "Lok Adalat Section 21 Legal Services Authorities Act final decree fee refund",
    "ಅಪಘಾತ": "motor accident compensation Section 166 MV Act MACT claim tribunal",
    "ಸೈಬರ್": "cybercrime IT Act Section 66C 66D helpline 1930 online fraud",

    # ── KANGLISH TRANSLITERATIONS ──
    "khatha": "khata transfer e-Khata property tax register Section 114 KMC Act",
    "thevani": "security deposit tenancy refund Section 27 Karnataka Rent Act Section 108 TPA",
    "bhadrathe": "security deposit tenancy refund",
    "maalika": "landlord tenant dispute Karnataka Rent Act",
    "baadige": "rent tenancy agreement Section 27",
    "bounc": "cheque bounce Section 138 Negotiable Instruments Act",
    "jameenu": "agricultural land revenue conversion Section 95 KLRA",
    "jameen": "land property dispute Karnataka Land Revenue Act",
    "dhaave": "civil suit partition suit declaration title CPC",
    "vibhaga": "partition suit ancestral property Hindu Succession Act Section 6",
    "kraya": "sale deed conveyance registration Section 54 TPA",
    "dhaanapatra": "gift deed Section 122 Transfer of Property Act",
    "hakku": "legal right property right coparcenary share",
    "otti": "mortgage deed Section 58 Transfer of Property Act",
    "pothi": "pouthi mutation inheritance transfer Section 128 KLRA",
    "vamshavriksha": "Vamshavruksha genealogy tree legal heir certificate",
    "ottawari": "encroachment land grabbing prohibition act trespass",
    "daari": "pathway right easement of necessity Section 13 Easements Act",
    "eswathu": "e-Swathu rural Gram Panchayat property Form 9 Form 11",
    "bhoomi": "Bhoomi Karnataka land record portal RTC Pahani",
    "kaveri": "Kaveri 2.0 property registration encumbrance certificate",

    # ── HINDI (हिंदी) & HINGLISH PROPERTY / REVENUE TERMS ──
    "खसरा": "Khasra land revenue survey plot number Record of Rights",
    "खतौनी": "Khatauni record of rights land tenure Pahani equivalent",
    "दाखिल खारिज": "mutation dakhil kharij acquisition of rights revenue record",
    "नामांतरण": "mutation namantaran change of name revenue records Section 128",
    "बैनामा": "sale deed bainama conveyance deed Section 54 Transfer of Property Act",
    "रजिस्ट्री": "property registration Section 17 Registration Act stamp duty",
    "इकरारनामा": "agreement to sell contract Section 53A TPA specific performance",
    "दानपत्र": "gift deed danpatra Section 122 Transfer of Property Act",
    "वसीयत": "Will testament Section 30 Hindu Succession Act Indian Succession Act",
    "बंटवारा": "partition batwara coparcenary ancestral property Section 6 HSA",
    "पैतृक संपत्ति": "ancestral property coparcenary Hindu Succession Act Section 6",
    "हक त्याग": "relinquishment deed release deed coparcenary share",
    "कब्जा": "possession physical possession Section 6 Specific Relief Act",
    "प्रतिकूल कब्जा": "adverse possession Article 65 Limitation Act 12 years hostile possession",
    "अवैध कब्जा": "illegal possession trespass encroachment eviction injunction",
    "सुखाधिकार": "easement right right of way pathway Section 15 Easements Act",
    "रास्ता": "pathway right easement of necessity Section 13 Indian Easements Act",
    "जमा": "security deposit tenancy refund Section 108 TPA Section 27 Karnataka Rent Act",
    "सुरक्षा जमा": "security deposit tenancy advance refund Section 108 TPA Section 27",
    "मकान मालिक": "landlord tenancy eviction possession Section 27 Karnataka Rent Act",
    "किराया": "tenancy rent agreement deposit refund Section 108 TPA Section 27 Karnataka Rent Act Section 14",
    "खाली": "vacate flat surrender possession deposit refund Section 27 Section 108",
    "टूट-फूट": "wear and tear painting deduction Section 108 TPA deposit refund",
    "मरम्मत": "repairs Section 14 Karnataka Rent Act landlord obligation",
    "रेरा": "RERA builder delay refund Section 18 possession compensation",
    "बिल्डर": "builder delay possession RERA Section 18 defect liability",

    # ── HINDI CRIMINAL, FAMILY, LABOUR, BANKING ──
    "चेक बाउंस": "cheque bounce Section 138 Negotiable Instruments Act 30 days notice Section 142",
    "चेक": "cheque Section 138 Negotiable Instruments Act dishonour",
    "अनादर": "dishonour cheque Section 138 Negotiable Instruments Act",
    "मेमो": "bank memo Section 138 Negotiable Instruments Act 30 days notice",
    "गिरफ्तारी": "arrest Article 22 Constitution 24 hours magistrate DK Basu Section 35 BNSS",
    "हिरासत": "custody arrest Article 22 Constitution 24 hours magistrate DK Basu",
    "पुलिस": "police FIR Zero FIR Section 173 BNSS Superintendent of Police Lalita Kumari",
    "एफआईआर": "FIR Zero FIR Section 173 BNSS police complaint Lalita Kumari",
    "जीरो एफआईआर": "Zero FIR Section 173(1) BNSS jurisdiction anywhere",
    "जमानत": "anticipatory bail Section 482 BNSS regular bail Section 480 BNSS",
    "अग्रिम जमानत": "anticipatory bail Section 482 BNSS Sessions High Court",
    "धोखाधड़ी": "cheating Section 318(4) Bharatiya Nyaya Sanhita 2023 BNS 318 IPC 420",
    "420": "Section 318(4) Bharatiya Nyaya Sanhita 2023 cheating fraud",
    "चोरी": "theft Section 303 BNS 2023 dishonest taking IPC 379",
    "मारपीट": "assault voluntarily causing hurt Section 115 BNS IPC 323",
    "जालसाजी": "forgery false document Section 336 BNS IPC 468",
    "तलाक": "divorce mutual consent Hindu Marriage Act Section 13B",
    "आपसी सहमति": "mutual consent divorce Section 13B Hindu Marriage Act 6 months",
    "भरण पोषण": "maintenance Section 144 BNSS wives children parents family court Rajnesh v Neha",
    "घरेलू हिंसा": "domestic violence Protection of Women from Domestic Violence Act Section 18 PWDVA",
    "दहेज": "Dowry Prohibition Act Section 85 BNS Section 86 BNS cruelty",
    "उपभोक्ता": "consumer protection Section 35 CPA District Commission e-Daakhil",
    "खराब सामान": "defective product deficiency in service Consumer Protection Act",
    "सूचना का अधिकार": "Right to Information Act 2005 Section 7 RTI 30 days 48 hours",
    "मुफ्त कानूनी सहायता": "free legal aid NALSA DLSA helpline 15100 Article 39A",
    "समय सीमा": "limitation period Limitation Act Article 54 Section 142 NI Act",
    "वेतन": "unpaid salary Code on Wages Payment of Wages Act recovery",
    "ग्रेच्युटी": "gratuity Payment of Gratuity Act Section 4 continuous service 5 years",
    "लोक अदालत": "Lok Adalat Section 21 Legal Services Authorities Act final decree fee refund",
    "सड़क दुर्घटना": "motor accident compensation Section 166 MV Act MACT claim tribunal",
    "साइबर अपराध": "cybercrime IT Act Section 66C 66D helpline 1930 online fraud",

    # ── HINGLISH TRANSLITERATIONS ──
    "kiraya": "tenancy rent agreement deposit refund Section 108 TPA Section 27",
    "advance": "advance security deposit refund tenancy Section 27",
    "vacate": "vacate flat surrender possession deposit refund Section 27",
    "makan malik": "landlord tenant dispute Karnataka Rent Act Section 27",
    "kabza": "possession adverse possession illegal occupation eviction",
    "batwara": "partition coparcenary ancestral property Hindu Succession Act",
    "bainama": "sale deed conveyance deed registration Section 54 TPA",
    "dakhil kharij": "mutation transfer of title revenue records Section 128",
    "iqrarnama": "agreement to sell contract specific performance",
    "wasiyat": "will testament succession certificate",
    "danpatra": "gift deed Section 122 Transfer of Property Act",
    "paitrik sampatti": "ancestral property coparcenary Hindu Succession Act Section 6",
    "hissa": "share in coparcenary ancestral property partition",
    "rasta": "pathway right easement of necessity Section 13 Easements Act",
}


OUT_OF_SCOPE_PATTERNS = [
    r"(?i)\b(recipe|weather|cricket|movie|capital of france|how to bake|stock price|crypto|tourist|travel|switzerland|nodejs|python script|linked list|install)\b",
    r"(?i)\b(quantum physics|video game|football|horoscope|astrology|software|programming|extraterrestrial|spacecraft|ufo|alien|neptune treaty)\b",
    r"(?i)(ಹವಾಮಾನ|ಪಾಕ್|ಕ್ರಿಕೆಟ್|ರೆಸಿಪಿ|ಬೆಣ್ಣೆ|ಅಡುಗೆ)",
    r"(?i)(मौसम|क्रिकेट|रेसिपी|केक|सिनेमा|पर्यटन|सॉफ्टवेयर)",
]

# Dynamically enrich VERNACULAR_MAPPINGS from MULTILINGUAL_GLOSSARY.json
import json
import os

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
_GLOSSARY_FILE = os.path.join(_BASE_DIR, "docs", "MULTILINGUAL_GLOSSARY.json")
if os.path.exists(_GLOSSARY_FILE):
    try:
        with open(_GLOSSARY_FILE, "r", encoding="utf-8") as _gf:
            _glossary_data = json.load(_gf)
            for _k, _entry in _glossary_data.items():
                _statute = _entry.get("canonical_statute", "")
                _eng = _entry.get("english", "")
                _defn = _entry.get("definition", "")
                _exp = f"{_eng} {_statute}".strip()
                if _entry.get("kannada"):
                    VERNACULAR_MAPPINGS[_entry["kannada"]] = _exp
                if _entry.get("hindi"):
                    VERNACULAR_MAPPINGS[_entry["hindi"]] = _exp
                for _trans in _entry.get("transliterations", []):
                    VERNACULAR_MAPPINGS[_trans.lower()] = _exp
                for _mis in _entry.get("common_misspellings", []):
                    VERNACULAR_MAPPINGS[_mis.lower()] = _exp
    except Exception:
        pass


class LegalQueryRewriter:
    """Normalizes citizen language, detects dialects, expands legacy statutes, and enriches search terms."""

    @classmethod
    def detect_language(cls, text: str) -> str:
        """Detects language script: Kannada (kn), Hindi (hi), English (en), or mixed."""
        kannada_chars = len(re.findall(r"[\u0C80-\u0CFF]", text))
        devanagari_chars = len(re.findall(r"[\u0900-\u097F]", text))
        latin_chars = len(re.findall(r"[A-Za-z]", text))

        total_script_chars = kannada_chars + devanagari_chars + latin_chars
        if total_script_chars == 0:
            return "en"

        if kannada_chars / total_script_chars > 0.35:
            return "kn" if latin_chars == 0 else "mixed"
        if devanagari_chars / total_script_chars > 0.35:
            return "hi" if latin_chars == 0 else "mixed"

        return "en"

    @classmethod
    def check_out_of_scope(cls, text: str) -> bool:
        """Flags queries completely unrelated to Indian civil, criminal, or statutory law."""
        for pattern in OUT_OF_SCOPE_PATTERNS:
            if re.search(pattern, text):
                return True
        return False

    @classmethod
    def rewrite(cls, raw_query: str) -> RewrittenQuery:
        """Executes full normalization, language detection, legacy concordance replacement,
        and domain synonym enrichment."""
        norm = raw_query.strip()
        lower = norm.lower()

        # Check out-of-scope
        is_oos = cls.check_out_of_scope(norm)
        lang = cls.detect_language(norm)

        # Legacy concordance checking (e.g. IPC 420 -> BNS 318)
        concordance_info = None
        expanded_terms: List[str] = [norm]
        domain_tags: Set[str] = set()

        # Check for IPC patterns (e.g. "IPC 420", "IPC section 302", "sec 420 ipc")
        ipc_match = (
            re.search(r"(?i)(?:ipc|indian\s+penal\s+code)\s*(?:section|sec)?\s*([0-9]+[a-z]?)", norm)
            or re.search(r"(?i)(?:section|sec)?\s*([0-9]+[a-z]?)\s*(?:of\s+the\s+)?ipc", norm)
        )
        if ipc_match:
            sec_num = ipc_match.group(1)
            entry = lookup_concordance("IPC", sec_num)
            if entry:
                concordance_info = f"{entry.repealed_act} {entry.repealed_section} -> {entry.active_act} {entry.active_section}"
                expanded_terms.append(f"{entry.active_act} {entry.active_section} {entry.active_title}")
                domain_tags.add("CRIMINAL_LAW")

        # Check for CrPC patterns (e.g. "CrPC 154", "CrPC 438", "CrPC 41A")
        crpc_match = (
            re.search(r"(?i)(?:crpc|code\s+of\s+criminal\s+procedure)\s*(?:section|sec)?\s*([0-9]+[a-z]?)", norm)
            or re.search(r"(?i)(?:section|sec)?\s*([0-9]+[a-z]?)\s*(?:of\s+the\s+)?crpc", norm)
        )
        if crpc_match:
            sec_num = crpc_match.group(1)
            entry = lookup_concordance("CRPC", sec_num)
            if entry:
                concordance_info = f"{entry.repealed_act} {entry.repealed_section} -> {entry.active_act} {entry.active_section}"
                expanded_terms.append(f"{entry.active_act} {entry.active_section} {entry.active_title}")
                domain_tags.add("CRIMINAL_PROCEDURE")

        # Vernacular term expansion
        for vern_word, expansion in VERNACULAR_MAPPINGS.items():
            if vern_word in norm or vern_word.lower() in lower:
                expanded_terms.append(expansion)
                # Map to primary domain
                if any(w in expansion for w in ["Karnataka Land Revenue", "Bhoomi", "Pahani", "RTC", "mutation"]):
                    domain_tags.add("LAND_REVENUE")
                if any(w in expansion for w in ["Transfer of Property", "coparcenary", "partition", "easement"]):
                    domain_tags.add("PROPERTY_LAW")
                if any(w in expansion for w in ["Karnataka Rent Act", "tenancy", "deposit"]):
                    domain_tags.add("TENANCY")
                if any(w in expansion for w in ["cheque", "138", "NI Act"]):
                    domain_tags.add("BANKING_FINANCE")
                if any(w in expansion for w in ["arrest", "BNSS", "BNS", "FIR", "bail"]):
                    domain_tags.add("CRIMINAL_LAW")
                if any(w in expansion for w in ["divorce", "Hindu Marriage", "maintenance", "PWDVA"]):
                    domain_tags.add("FAMILY_LAW")
                if any(w in expansion for w in ["Consumer Protection", "e-Daakhil"]):
                    domain_tags.add("CONSUMER_PROTECTION")

        # English legal concept synonym expansion
        for keyword, synonyms in SYNONYM_EXPANSIONS.items():
            if keyword in lower:
                expanded_terms.extend(synonyms[:4])
                if keyword in ["khata", "pahani", "rtc", "mutation", "phodi", "patta", "conversion", "ptcl", "plot", "plot owner", "plot ownership"]:
                    domain_tags.add("LAND_REVENUE")
                    domain_tags.add("PROPERTY_LAW")
                elif keyword in ["sale deed", "gift deed", "partition", "ancestral", "easement", "encumbrance", "ownership"]:
                    domain_tags.add("PROPERTY_LAW")
                elif keyword in ["deposit", "landlord", "tenant", "rent", "eviction"]:
                    domain_tags.add("TENANCY")
                elif keyword in ["rera", "builder delay", "occupancy certificate", "apartment"]:
                    domain_tags.add("REAL_ESTATE")
                elif keyword in ["cheque", "bounce", "138", "sarfaesi", "loan harassment", "ombudsman"]:
                    domain_tags.add("BANKING_FINANCE")
                elif keyword in ["arrest", "police", "fir", "bail", "cheating", "assault"]:
                    domain_tags.add("CRIMINAL_LAW")
                elif keyword in ["summon", "summons", "legal summon", "warrant"]:
                    domain_tags.add("CRIMINAL_PROCEDURE")
                    domain_tags.add("CIVIL_PROCEDURE")
                elif keyword in ["divorce", "maintenance", "child custody", "domestic violence"]:
                    domain_tags.add("FAMILY_LAW")
                elif keyword in ["consumer", "deficiency", "e-daakhil"]:
                    domain_tags.add("CONSUMER_PROTECTION")
                elif keyword in ["salary", "termination", "gratuity", "posh"]:
                    domain_tags.add("LABOUR_EMPLOYMENT")
                elif keyword in ["accident", "mact", "drink and drive", "drunk driving", "traffic", "challan", "traffic police", "traffic fine"]:
                    domain_tags.add("MOTOR_VEHICLE_LAW")
                elif keyword in ["cybercrime", "otp fraud"]:
                    domain_tags.add("CYBERCRIME")

        final_expanded = " ".join(dict.fromkeys(" ".join(expanded_terms).split()))

        return RewrittenQuery(
            original_query=raw_query,
            normalized_query=norm,
            expanded_query=final_expanded,
            detected_language=lang,
            legacy_concordance_detected=concordance_info,
            is_out_of_scope=is_oos,
            domain_tags=list(domain_tags) if domain_tags else ["GENERAL_CIVIL"],
        )
