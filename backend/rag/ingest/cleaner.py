"""Legal text cleaner and sequential section verification module."""

import re
from typing import List, Tuple, Dict, Any


class LegalTextCleaner:
    """Cleans legal text extracted from official gazettes, bare acts, and PDFs."""

    @staticmethod
    def clean_text(raw_text: str) -> str:
        """Removes headers, footers, gazette pagination, and OCR artifacts."""
        if not raw_text:
            return ""

        text = raw_text

        # 1. Normalize line breaks and carriage returns
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        # 2. Remove common gazette headers/footers
        text = re.sub(r"(?i)THE\s+GAZETTE\s+OF\s+INDIA\s*:?\s*EXTRAORDINARY.*?\n", "", text)
        text = re.sub(r"(?i)PART\s+II\s*—\s*SECTION\s*\d+.*?\n", "", text)
        text = re.sub(r"(?i)PUBLISHED\s+BY\s+AUTHORITY.*?\n", "", text)
        text = re.sub(r"(?i)NEW\s+DELHI,\s+[A-Z]+,\s+[A-Z]+\s+\d+,\s+\d{4}.*?\n", "", text)
        text = re.sub(r"(?i)KARNATAKA\s+GAZETTE,\s+[A-Z]+\s+\d+,\s+\d{4}.*?\n", "", text)

        # 3. Remove standalone page numbers (e.g., "[12]", "Page 45 of 120", "--- 3 ---")
        text = re.sub(r"^\s*\[?\s*\d+\s*\]?\s*$", "", text, flags=re.MULTILINE)
        text = re.sub(r"(?i)^\s*page\s+\d+(\s+of\s+\d+)?\s*$", "", text, flags=re.MULTILINE)
        text = re.sub(r"^\s*[-—–]+\s*\d+\s*[-—–]+\s*$", "", text, flags=re.MULTILINE)

        # 4. Remove legal margin notes and stray running titles
        text = re.sub(r"(?m)^\s*(SEC\.|SECTION|SCHEDULE)\s*\d+[A-Z]?\s*$", "", text)

        # 5. Fix common OCR character confusions in legal text
        text = re.sub(r"(?<=\bSec\.)\s*([lI1])(?=\b)", "1", text)
        text = re.sub(r"(?<=\bSection\s)l(?=\d)", "1", text)
        text = re.sub(r"(?<=\bSection\s)O(?=\d)", "0", text)
        text = re.sub(r"\bO(?=\.\s*S\.)", "O", text)  # Protect Order/Suit

        # 6. Normalize smart quotes, dashes, and currency symbols
        text = text.replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
        text = text.replace("—", " - ").replace("–", " - ")
        text = text.replace("Rs.", "₹").replace("Rs ", "₹ ")

        # 7. Collapse excessive whitespace while preserving paragraphing
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)

        return text.strip()

    @staticmethod
    def verify_sequential_sections(section_numbers: List[str]) -> Tuple[bool, List[str]]:
        """Verifies that extracted section numbers form a continuous sequential chain.
        Flags gaps or out-of-order anomalies for manual lawyer review."""
        parsed: List[Tuple[int, str]] = []
        for s in section_numbers:
            # Extract primary integer from "Section 138", "138A", "Sec 27", etc.
            match = re.search(r"(\d+)", str(s))
            if match:
                parsed.append((int(match.group(1)), s))

        anomalies: List[str] = []
        if len(parsed) <= 1:
            return True, anomalies

        for i in range(len(parsed) - 1):
            curr_num, curr_str = parsed[i]
            next_num, next_str = parsed[i + 1]

            # In legal statutes, jump > 1 means a missing section unless an amendment letter is present
            if next_num > curr_num + 1:
                anomalies.append(
                    f"Possible missing section between '{curr_str}' and '{next_str}' (Gap: {next_num - curr_num - 1})"
                )
            elif next_num < curr_num and not any(letter in next_str for letter in ["A", "B", "C", "D"]):
                anomalies.append(
                    f"Non-sequential order detected: '{curr_str}' followed by '{next_str}'"
                )

        return len(anomalies) == 0, anomalies
