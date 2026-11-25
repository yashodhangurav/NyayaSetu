"""Legal Document Parser and Text Extractor.

Extracts, cleans, and standardizes legal text from PDF, HTML, plain text,
and JSON documents while strictly preserving statutory phrasing and numbering.
"""

from html.parser import HTMLParser
import io
import re
from typing import Optional, Union
import xml.etree.ElementTree as ET
import zipfile


class _LegalHTMLStripper(HTMLParser):
    """HTML Parser that strips tags, scripts, and navigation while preserving paragraph boundaries."""

    def __init__(self):
        super().__init__()
        self._pieces = []
        self._ignore = False
        self._ignore_tags = {"script", "style", "nav", "footer", "header", "noscript"}

    def handle_starttag(self, tag, attrs):
        tag_lower = tag.lower()
        if tag_lower in self._ignore_tags:
            self._ignore = True
        elif tag_lower in {"p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "tr", "li"}:
            self._pieces.append("\n")
        elif tag_lower == "br":
            self._pieces.append("\n")

    def handle_endtag(self, tag):
        tag_lower = tag.lower()
        if tag_lower in self._ignore_tags:
            self._ignore = False
        elif tag_lower in {"p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "tr"}:
            self._pieces.append("\n")

    def handle_data(self, data):
        if not self._ignore:
            self._pieces.append(data)

    def get_text(self) -> str:
        return "".join(self._pieces)


class DocumentParser:
    """Robust document extractor and cleaner for Indian statutory Bare Acts and judgments."""

    @classmethod
    def extract_text(
        cls,
        content: Union[bytes, str],
        file_format: str,
        filename: Optional[str] = None,
    ) -> str:
        """Extract plain text from raw bytes or string content according to file_format."""
        fmt = (file_format or "").strip().upper()
        if not fmt and filename:
            if filename.lower().endswith(".pdf"):
                fmt = "PDF"
            elif filename.lower().endswith((".html", ".htm")):
                fmt = "HTML"
            elif filename.lower().endswith((".txt", ".md")):
                fmt = "TXT"
            elif filename.lower().endswith(".json"):
                fmt = "JSON"
            elif filename.lower().endswith(".xml"):
                fmt = "XML"
            elif filename.lower().endswith(".docx"):
                fmt = "DOCX"

        if fmt == "PDF":
            if isinstance(content, str):
                content = content.encode("utf-8")
            return cls.extract_from_pdf(content)
        elif fmt in {"HTML", "HTM"}:
            return cls.extract_from_html(content)
        elif fmt in {"TXT", "TEXT", "MD"}:
            return cls.extract_from_txt(content)
        elif fmt == "JSON":
            return cls.extract_from_txt(content)
        elif fmt == "XML":
            return cls.extract_from_xml(content)
        elif fmt == "DOCX":
            return cls.extract_from_docx(content)
        else:
            raise ValueError(
                f"Unsupported file format '{file_format}'. Supported formats: PDF, HTML, TXT, JSON, XML, DOCX."
            )

    @classmethod
    def extract_from_pdf(cls, content_bytes: bytes) -> str:
        """Extract text from PDF using pypdf, stripping gazette watermarks and joining line breaks."""
        try:
            from pypdf import PdfReader
        except ImportError:
            raise RuntimeError("pypdf is required for PDF parsing. Please install pypdf>=4.0.0.")

        if not content_bytes:
            raise ValueError("PDF content bytes cannot be empty.")

        stream = io.BytesIO(content_bytes)
        try:
            reader = PdfReader(stream)
        except Exception as e:
            raise ValueError(f"Failed to read PDF document: {str(e)}")

        pages_text = []
        for i, page in enumerate(reader.pages):
            try:
                page_raw = page.extract_text() or ""
                # Strip typical gazette headers/footers
                cleaned_page = cls._strip_gazette_headers_and_footers(page_raw)
                pages_text.append(cleaned_page)
            except Exception as e:
                # Log page extraction error but continue
                continue

        full_text = "\n\n".join(pages_text)
        return cls.clean_legal_text(full_text)

    @classmethod
    def extract_from_html(cls, content: Union[str, bytes]) -> str:
        """Extract text from HTML content, discarding scripts, CSS, and navigation markup."""
        if isinstance(content, bytes):
            try:
                html_str = content.decode("utf-8")
            except UnicodeDecodeError:
                html_str = content.decode("latin-1", errors="replace")
        else:
            html_str = content

        if not html_str.strip():
            raise ValueError("HTML content cannot be empty.")

        stripper = _LegalHTMLStripper()
        stripper.feed(html_str)
        raw_text = stripper.get_text()
        return cls.clean_legal_text(raw_text)

    @classmethod
    def extract_from_txt(cls, content: Union[str, bytes]) -> str:
        """Extract text from plain text or Markdown bytes/string."""
        if isinstance(content, bytes):
            try:
                text_str = content.decode("utf-8")
            except UnicodeDecodeError:
                text_str = content.decode("latin-1", errors="replace")
        else:
            text_str = content

        if not text_str.strip():
            raise ValueError("Text content cannot be empty.")

        return cls.clean_legal_text(text_str)

    @classmethod
    def extract_from_xml(cls, content: Union[str, bytes]) -> str:
        """Extract readable text from XML/RSS/Atom documents without executing markup."""
        if isinstance(content, bytes):
            content = content.decode("utf-8", errors="replace")
        if not content.strip():
            raise ValueError("XML content cannot be empty.")
        try:
            root = ET.fromstring(content)
        except ET.ParseError as exc:
            raise ValueError(f"Malformed XML document: {exc}") from exc
        pieces = [text.strip() for text in root.itertext() if text and text.strip()]
        return cls.clean_legal_text("\n".join(pieces))

    @classmethod
    def extract_from_docx(cls, content: Union[bytes, str]) -> str:
        """Extract paragraphs from a DOCX package using only the standard library."""
        if isinstance(content, str):
            content = content.encode("utf-8")
        try:
            with zipfile.ZipFile(io.BytesIO(content)) as archive:
                xml_bytes = archive.read("word/document.xml")
        except (zipfile.BadZipFile, KeyError) as exc:
            raise ValueError("Invalid DOCX document: word/document.xml is missing") from exc

        root = ET.fromstring(xml_bytes)
        namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
        paragraphs: list[str] = []
        for paragraph in root.iter(f"{namespace}p"):
            text = "".join(node.text or "" for node in paragraph.iter(f"{namespace}t"))
            if text.strip():
                paragraphs.append(text.strip())
        return cls.clean_legal_text("\n".join(paragraphs))

    @classmethod
    def clean_legal_text(cls, raw_text: str) -> str:
        """Clean formatting without modifying legal meaning, statutory words, or numbering."""
        if not raw_text:
            return ""

        text = raw_text

        # 1. Normalize unicode characters (smart quotes, em-dashes, non-breaking spaces)
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        text = text.replace("\xa0", " ")  # Non-breaking space
        text = text.replace("“", '"').replace("”", '"')
        text = text.replace("‘", "'").replace("’", "'")
        text = text.replace("—", " - ").replace("–", " - ")

        # 2. Fix hyphenated word breaks at end of line (e.g., 'deter-\nmination' -> 'determination')
        # Only when word characters precede and follow the hyphen
        text = re.sub(r"([a-zA-Z]{2,})-\n\s*([a-zA-Z]{2,})", r"\1\2", text)

        # 3. Strip page number artifacts e.g. '[Page 12 of 45]' or '[ 12 ]'
        text = re.sub(r"\[\s*Page\s+\d+\s+(?:of\s+\d+\s+)?\]", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\n\s*\d+\s*\n", "\n", text)  # Isolated page number on its own line

        # 4. Normalize multiple horizontal spaces to single space, but preserve linebreaks
        text = re.sub(r"[ \t]+", " ", text)

        # 5. Normalize excessive blank lines (more than 2 consecutive newlines to 2)
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()

    @staticmethod
    def _strip_gazette_headers_and_footers(page_text: str) -> str:
        """Remove common Indian Gazette publication headers and footers."""
        lines = page_text.splitlines()
        filtered = []
        for line in lines:
            stripped = line.strip()
            # Gazette headers
            if re.search(r"THE\s+GAZETTE\s+OF\s+INDIA|EXTRAORDINARY|PART\s+II|REGD\.\s*NO\.", stripped, re.IGNORECASE):
                continue
            if re.search(r"PUBLISHED\s+BY\s+AUTHORITY|MINISTRY\s+OF\s+LAW\s+AND\s+JUSTICE", stripped, re.IGNORECASE):
                continue
            # Footer pagination e.g. 'SEC. 1] THE GAZETTE OF INDIA'
            if re.search(r"^\s*SEC\.\s*\d+\s*\]", stripped, re.IGNORECASE):
                continue
            filtered.append(line)
        return "\n".join(filtered)
