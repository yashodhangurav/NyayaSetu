"""Bounded discovery adapters for configured official legal sources.

Discovery never invents endpoints. It uses declared document URLs, sitemap URLs
advertised in robots.txt (or explicitly configured), explicitly configured feed
URLs, or a configured official listing page.
"""

from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Iterable, List, Optional
from urllib.parse import urldefrag, urljoin, urlparse
import xml.etree.ElementTree as ET

from app.core.config import settings
from app.core.logging import logger
from app.modules.legal_knowledge.fetcher import FetchError, SecureFetcher
from app.modules.legal_knowledge.source_registry import SourceCandidate, is_official_indian_domain


@dataclass(frozen=True)
class DiscoveredDocument:
    url: str
    title: str
    source_key: str
    parser_strategy: str


class _AnchorParser(HTMLParser):
    def __init__(self, base_url: str) -> None:
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.links: list[tuple[str, str]] = []
        self._href: Optional[str] = None
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, Optional[str]]]) -> None:
        if tag.lower() != "a":
            return
        self._href = dict(attrs).get("href")
        self._text = []

    def handle_data(self, data: str) -> None:
        if self._href is not None:
            self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() != "a" or self._href is None:
            return
        clean_url, _ = urldefrag(urljoin(self.base_url, self._href))
        self.links.append((clean_url, " ".join("".join(self._text).split())))
        self._href = None
        self._text = []


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()


def _normalize_candidate(url: str, base_url: str) -> Optional[str]:
    try:
        clean, _ = urldefrag(urljoin(base_url, url))
    except Exception:
        return None
    return clean if is_official_indian_domain(clean) else None


def _document_like(url: str) -> bool:
    path = urlparse(url).path.lower()
    return any(path.endswith(ext) for ext in (".pdf", ".html", ".htm", ".txt", ".xml", ".doc", ".docx"))


async def discover_documents(
    candidate: SourceCandidate,
    fetcher: SecureFetcher,
    *,
    max_documents: Optional[int] = None,
) -> List[DiscoveredDocument]:
    """Discover a bounded set of candidate URLs for one source."""
    limit = max_documents or settings.RAG_DISCOVERY_MAX_DOCUMENTS
    strategy = (candidate.fetch_strategy or "STATIC_DOCUMENT").upper()
    raw_urls: List[tuple[str, str]] = []

    if strategy == "STATIC_DOCUMENT":
        raw_urls = [(url, candidate.name) for url in candidate.source_config.get("document_urls", [])]

    elif strategy == "SITEMAP":
        sitemap_urls = list(candidate.source_config.get("sitemap_urls") or [])
        if not sitemap_urls:
            sitemap_urls = await fetcher.sitemap_urls(candidate.base_url)
        for sitemap_url in sitemap_urls:
            try:
                result = await fetcher.fetch(sitemap_url)
                root = ET.fromstring(result.content)
            except (FetchError, ET.ParseError) as exc:
                logger.warning("Sitemap discovery failed for %s: %s", sitemap_url, exc)
                continue
            for element in root.iter():
                if _local_name(element.tag) == "loc" and (element.text or "").strip():
                    raw_urls.append(((element.text or "").strip(), candidate.name))

    elif strategy in {"FEED", "RSS", "ATOM"}:
        feed_urls = list(candidate.source_config.get("feed_urls") or [])
        for feed_url in feed_urls:
            try:
                result = await fetcher.fetch(feed_url)
                root = ET.fromstring(result.content)
            except (FetchError, ET.ParseError) as exc:
                logger.warning("Feed discovery failed for %s: %s", feed_url, exc)
                continue
            for item in root.iter():
                name = _local_name(item.tag)
                if name == "item" or name == "entry":
                    title = ""
                    link = ""
                    for child in item:
                        child_name = _local_name(child.tag)
                        if child_name == "title":
                            title = (child.text or "").strip()
                        elif child_name == "link":
                            link = (child.attrib.get("href") or child.text or "").strip()
                    if link:
                        raw_urls.append((link, title or candidate.name))

    elif strategy in {"LISTING", "HTML"}:
        try:
            result = await fetcher.fetch(candidate.base_url)
            parser = _AnchorParser(candidate.base_url)
            parser.feed(result.content.decode(result.content_type_encoding or "utf-8", errors="replace"))
            raw_urls = parser.links
        except FetchError as exc:
            logger.warning("Listing discovery failed for %s: %s", candidate.base_url, exc)

    else:
        logger.warning("Unsupported fetch strategy %s for %s", strategy, candidate.registry_key)
        return []

    # Declared static URLs are already explicit document pointers; many official
    # India Code handles have no file extension. Only discovered listing/feed/
    # sitemap links need the extension heuristic.
    allow_extensionless = strategy == "STATIC_DOCUMENT"
    seen: set[str] = set()
    documents: List[DiscoveredDocument] = []
    for raw_url, title in raw_urls:
        normalized = _normalize_candidate(raw_url, candidate.base_url)
        if not normalized or normalized in seen:
            continue
        if not allow_extensionless and not _document_like(normalized):
            continue
        seen.add(normalized)
        documents.append(
            DiscoveredDocument(
                url=normalized,
                title=(title or candidate.name)[:255],
                source_key=candidate.registry_key,
                parser_strategy=candidate.parser_strategy,
            )
        )
        if len(documents) >= limit:
            break

    return documents


def unique_documents(documents: Iterable[DiscoveredDocument]) -> List[DiscoveredDocument]:
    """Return URL-deduplicated documents preserving discovery order."""
    seen: set[str] = set()
    result: List[DiscoveredDocument] = []
    for doc in documents:
        key = doc.url.lower()
        if key not in seen:
            seen.add(key)
            result.append(doc)
    return result
