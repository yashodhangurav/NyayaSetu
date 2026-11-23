"""Multilingual Legal Query Rewriting, Normalization & Concordance Expansion Module."""

import re
from typing import Dict, List, Optional, Tuple, NamedTuple

from rag.ingest.concordance_table import lookup_concordance


class RewrittenQuery(NamedTuple):
    original_query: str
    normalized_query: str
    expanded_query: str
    detected_language: str  # en | kn | hi | mixed
    legacy_concordance_detected: Optional[str]  # e.g. "IPC 420 -> BNS Section 318(4)"
    is_out_of_scope: bool
    domain_tags: List[str]


# Domain synonym dictionaries for Indian law
SYNONYM_EXPANSIONS: Dict[str, List[str]] = {
    "deposit": ["security deposit", "advance", "refund", "wear and tear", "Section 108 TPA", "Section 27 Karnataka Rent Act", "tenancy"],
    "landlord": ["lessor", "tenant", "rent agreement", "eviction", "Karnataka Rent Act", "handover possession", "repairs"],
    "tenant": ["rent agreement", "possession", "Section 108 Transfer of Property Act", "Section 27 Karnataka Rent Act"],
    "rent": ["Karnataka Rent Act", "Section 27", "Section 14 repairs", "Section 108 TPA", "security deposit"],
    "repair": ["repair of premises", "Section 14 Karnataka Rent Act", "landlord obligation to maintain", "tenant repairs deduction"],
    "wear and tear": ["normal wear and tear", "painting deduction", "Section 108 TPA", "security deposit refund"],
    "cheque": ["dishonour of cheque", "bounced cheque", "Section 138 Negotiable Instruments Act", "bank return memo", "30 days notice", "Section 142 NI Act"],
    "bounce": ["Section 138 Negotiable Instruments Act", "dishonour", "bank return memo", "30 days legal notice"],
    "138": ["Section 138 Negotiable Instruments Act", "dishonour of cheque", "bank memo date", "statutory demand notice", "limitation one month"],
    "142": ["Section 142 Negotiable Instruments Act", "cognizance of offences", "one month limitation", "jurisdiction magistrate"],
    "arrest": ["Article 22 Constitution", "grounds of arrest", "24 hours magistrate", "DK Basu guidelines", "Section 35 BNSS", "memo of arrest", "police custody"],
    "police": ["FIR", "Zero FIR", "Section 173 BNSS", "refusal to register FIR", "Superintendent of Police", "cognizable offence"],
    "fir": ["Section 173 BNSS", "First Information Report", "Zero FIR", "cognizable offence", "police station jurisdiction"],
    "bail": ["anticipatory bail", "Section 482 BNSS", "regular bail", "Section 480 BNSS", "non bailable offence", "High Court Sessions Court"],
    "ancestral": ["ancestral property", "coparcenary", "Section 6 Hindu Succession Act", "partition suit", "daughters rights in property", "Vamshavruksha"],
    "divorce": ["Section 13B Hindu Marriage Act", "mutual consent divorce", "cooling off period six months", "mediation", "family court"],
    "maintenance": ["Section 144 BNSS", "maintenance of wife children parents", "desertion", "Section 24 HMA", "monthly allowance"],
    "domestic violence": ["Protection of Women from Domestic Violence Act 2005", "Section 18 PWDVA", "protection order", "shared household", "magistrate"],
    "pwdva": ["Protection of Women from Domestic Violence Act", "Section 18", "Section 19", "shared household", "protection order"],
    "consumer": ["Consumer Protection Act 2019", "Section 35 CPA", "District Commission", "e-Daakhil", "deficiency in service", "product liability"],
    "e-daakhil": ["e-Daakhil", "consumer complaint online", "Section 35 Consumer Protection Act", "District Commission"],
    "non compete": ["Section 27 Indian Contract Act", "agreement in restraint of trade", "void agreement", "employment contract non-compete"],
    "limitation": ["Limitation Act 1963", "Article 54", "three years limitation", "breach of contract recovery", "statutory deadline"],
    "rti": ["Right to Information Act 2005", "Section 7 RTI", "30 days information", "48 hours life liberty", "CPIO"],
    "free legal aid": ["NALSA", "KSLSA", "DLSA", "Helpline 15100", "Section 12 Legal Services Authorities Act", "free advocate representation"],
    "nalsa": ["National Legal Services Authority", "Helpline 15100", "free legal aid", "Article 39A", "KSLSA"],
}

# Vernacular keywords to core legal concept mappings
VERNACULAR_MAPPINGS: Dict[str, str] = {
    # Kannada script & Kanglish
    "ಠೇವಣಿ": "security deposit tenancy refund Karnataka Rent Act Section 27 Section 108 TPA",
    "ಭದ್ರತಾ": "security deposit advance tenancy",
    "ಮಾಲೀಕ": "landlord tenancy lessor possession Karnataka Rent Act",
    "ಬಾಡಿಗೆ": "tenancy rent agreement Section 27 Karnataka Rent Act Section 108 TPA Section 14",
    "ಖಾಲಿ": "vacating premises surrender possession tenancy deposit refund Section 27",
    "ಸವೆತ": "normal wear and tear painting deduction Section 108 TPA deposit refund",
    "ದುರಸ್ತಿ": "repairs of premises Section 14 Karnataka Rent Act landlord",
    "ಚೆಕ್": "cheque bounce Section 138 Negotiable Instruments Act",
    "ಬೌನ್ಸ್": "dishonour cheque Section 138 bank memo 30 days notice Section 142",
    "ಅಮಾನ್ಯ": "dishonour cheque Section 138 Negotiable Instruments Act",
    "ಮೆಮೊ": "bank return memo Section 138 Negotiable Instruments Act 30 days",
    "ಬಂಧನ": "arrest Article 22 Constitution 24 hours magistrate BNSS Section 35 DK Basu",
    "ಪೊಲೀಸ್": "police FIR Zero FIR Section 173 BNSS complaint",
    "ಎಫ್‌ಐಆರ್": "FIR Zero FIR Section 173 BNSS First Information Report",
    "ನಿರಾಕರಿಸಿದರೆ": "refusal to register FIR Section 173 BNSS Superintendent of Police",
    "ಜಾಮೀನು": "anticipatory bail Section 482 BNSS regular bail",
    "ನಿರೀಕ್ಷಣಾ": "anticipatory bail Section 482 BNSS arrest",
    "ಆಸ್ತಿ": "ancestral property partition Hindu Succession Act Section 6 coparcenary",
    "ಪೂರ್ವಜರ": "ancestral coparcenary daughters property rights Section 6 Hindu Succession Act",
    "ವಿಭಾಗ": "partition suit ancestral property coparcenary Section 6",
    "ವಿಚ್ಛೇದನ": "divorce mutual consent Hindu Marriage Act Section 13B",
    "ಪರಸ್ಪರ": "mutual consent divorce Section 13B Hindu Marriage Act",
    "ಜೀವನಾಂಶ": "maintenance Section 144 BNSS family court wives children",
    "ಗೃಹಹಿಂಸೆ": "domestic violence Protection of Women from Domestic Violence Act Section 18 PWDVA",
    "ಹಿಂಸೆ": "domestic violence Protection of Women from Domestic Violence Act Section 18",
    "ಗ್ರಾಹಕ": "consumer protection Section 35 CPA District Commission e-Daakhil deficiency",
    "ಮಾಹಿತಿ ಹಕ್ಕು": "Right to Information Act 2005 Section 7 RTI 30 days 48 hours",
    "ಉಚಿತ ಕಾನೂನು ನೆರವು": "free legal aid NALSA KSLSA helpline 15100 Article 39A",
    "ಸಹಾಯವಾಣಿ": "helpline 15100 NALSA free legal aid DLSA",
    "ಕಾಲಮಿತಿ": "limitation period Limitation Act 1963 Article 54 Section 142 NI Act",
    "ಕರಾರು": "agreement contract Section 27 Indian Contract Act restraint of trade",
    "thevani": "security deposit tenancy refund Section 27 Karnataka Rent Act Section 108 TPA",
    "bhadrathe": "security deposit tenancy refund",
    "maalika": "landlord tenant dispute Karnataka Rent Act",
    "baadige": "rent tenancy agreement Section 27",
    "bounc": "cheque bounce Section 138 Negotiable Instruments Act",

    # Hindi script & Hinglish
    "जमा": "security deposit tenancy refund Section 108 TPA Section 27 Karnataka Rent Act",
    "सुरक्षा जमा": "security deposit tenancy advance refund Section 108 TPA Section 27",
    "मकान मालिक": "landlord tenancy eviction possession Section 27 Karnataka Rent Act",
    "किराया": "tenancy rent agreement deposit refund Section 108 TPA Section 27 Karnataka Rent Act Section 14",
    "खाली": "vacate flat surrender possession deposit refund Section 27 Section 108",
    "टूट-फूट": "wear and tear painting deduction Section 108 TPA deposit refund",
    "मरम्मत": "repairs Section 14 Karnataka Rent Act landlord obligation",
    "चेक बाउंस": "cheque bounce Section 138 Negotiable Instruments Act 30 days notice Section 142",
    "चेक": "cheque Section 138 Negotiable Instruments Act dishonour",
    "अनादर": "dishonour cheque Section 138 Negotiable Instruments Act",
    "मेमो": "bank memo Section 138 Negotiable Instruments Act 30 days notice",
    "गिरफ्तारी": "arrest Article 22 Constitution 24 hours magistrate DK Basu Section 35 BNSS",
    "हिरासत": "custody arrest Article 22 Constitution 24 hours magistrate DK Basu",
    "पुलिस": "police FIR Zero FIR Section 173 BNSS Superintendent of Police",
    "एफआईआर": "FIR Zero FIR Section 173 BNSS police complaint",
    "जमानत": "anticipatory bail Section 482 BNSS bail",
    "अग्रिम जमानत": "anticipatory bail Section 482 BNSS Sessions High Court",
    "पैतृक संपत्ति": "ancestral property coparcenary Hindu Succession Act Section 6",
    "बंटवारा": "partition ancestral property coparcenary Section 6 Hindu Succession Act",
    "तलाक": "divorce mutual consent Hindu Marriage Act Section 13B",
    "आपसी सहमति": "mutual consent divorce Section 13B Hindu Marriage Act 6 months",
    "भरण पोषण": "maintenance Section 144 BNSS wives children parents family court",
    "घरेलू हिंसा": "domestic violence Protection of Women from Domestic Violence Act Section 18 PWDVA",
    "उपभोक्ता": "consumer protection Section 35 CPA District Commission e-Daakhil",
    "सूचना का अधिकार": "Right to Information Act 2005 Section 7 RTI 30 days 48 hours",
    "मुफ्त कानूनी सहायता": "free legal aid NALSA DLSA helpline 15100 Article 39A",
    "समय सीमा": "limitation period Limitation Act Article 54 Section 142 NI Act",
    "धोखाधड़ी": "cheating Section 318(4) Bharatiya Nyaya Sanhita 2023 BNS 318 IPC 420",
    "420": "Section 318(4) Bharatiya Nyaya Sanhita 2023 cheating fraud",
    "kiraya": "tenancy rent agreement deposit refund Section 108 TPA Section 27",
    "advance": "advance security deposit refund tenancy Section 27",
    "vacate": "vacate flat surrender possession deposit refund Section 27",
}

OUT_OF_SCOPE_PATTERNS = [
    r"(?i)\b(recipe|weather|cricket|movie|capital of france|how to bake|stock price|crypto|tourist|travel|switzerland|nodejs|python script|linked list|install)\b",
    r"(?i)\b(quantum physics|video game|football|horoscope|astrology|software|programming|extraterrestrial|spacecraft|ufo|alien|neptune treaty)\b",
    r"(?i)(ಹವಾಮಾನ|ಪಾಕ್|ಕ್ರಿಕೆಟ್|ರೆಸಿಪಿ|ಬೆಣ್ಣೆ|ಅಡುಗೆ)",
    r"(?i)(मौसम|क्रिकेट|रेसिपी|केक|सिनेमा|पर्यटन|सॉफ्टवेयर)",
]


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
        domain_tags: List[str] = []

        # Check for IPC patterns (e.g. "IPC 420", "IPC section 302", "sec 420 ipc")
        ipc_match = re.search(r"(?i)(?:ipc|indian\s+penal\s+code)\s*(?:section|sec)?\s*([0-9]+[a-z]?)", norm) or \
                    re.search(r"(?i)(?:section|sec)?\s*([0-9]+[a-z]?)\s*(?:of\s+the\s+)?ipc", norm)
        if ipc_match:
            sec_num = ipc_match.group(1)
            entry = lookup_concordance("IPC", sec_num)
            if entry:
                concordance_info = f"{entry.repealed_act} {entry.repealed_section} -> {entry.active_act} {entry.active_section}"
                expanded_terms.append(f"{entry.active_act} {entry.active_section} {entry.active_title}")
                domain_tags.append("criminal")

        # Check for CrPC patterns (e.g. "CrPC 154", "CrPC 438", "CrPC 41A")
        crpc_match = re.search(r"(?i)(?:crpc|code\s+of\s+criminal\s+procedure)\s*(?:section|sec)?\s*([0-9]+[a-z]?)", norm) or \
                     re.search(r"(?i)(?:section|sec)?\s*([0-9]+[a-z]?)\s*(?:of\s+the\s+)?crpc", norm)
        if crpc_match:
            sec_num = crpc_match.group(1)
            entry = lookup_concordance("CRPC", sec_num)
            if entry:
                concordance_info = f"{entry.repealed_act} {entry.repealed_section} -> {entry.active_act} {entry.active_section}"
                expanded_terms.append(f"{entry.active_act} {entry.active_section} {entry.active_title}")
                domain_tags.append("criminal")

        # Vernacular term expansion
        for vern_word, expansion in VERNACULAR_MAPPINGS.items():
            if vern_word in norm or vern_word.lower() in lower:
                expanded_terms.append(expansion)
                domain_tags.append(expansion.split()[0].lower())

        # English legal concept synonym expansion
        for keyword, synonyms in SYNONYM_EXPANSIONS.items():
            if keyword in lower:
                expanded_terms.extend(synonyms[:4])
                domain_tags.append(keyword)

        final_expanded = " ".join(dict.fromkeys(" ".join(expanded_terms).split()))

        return RewrittenQuery(
            original_query=raw_query,
            normalized_query=norm,
            expanded_query=final_expanded,
            detected_language=lang,
            legacy_concordance_detected=concordance_info,
            is_out_of_scope=is_oos,
            domain_tags=list(set(domain_tags)),
        )
