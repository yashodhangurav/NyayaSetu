"""Deterministic tests for secure fetching and bounded source discovery."""

import httpx
import pytest

from app.modules.legal_knowledge.discovery import discover_documents
from app.modules.legal_knowledge.fetcher import FetchError, SecureFetcher
from app.modules.legal_knowledge.source_registry import SourceCandidate

BASE = "https://www.indiacode.nic.in"


def _handler(request: httpx.Request) -> httpx.Response:
    path = request.url.path
    if path == "/robots.txt":
        return httpx.Response(
            200,
            text=(
                "User-agent: *\nDisallow: /private/\n"
                "Sitemap: https://www.indiacode.nic.in/sitemap.xml\n"
            ),
        )
    if path == "/sitemap.xml":
        return httpx.Response(
            200,
            text=(
                "<?xml version='1.0'?><urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>"
                "<url><loc>https://www.indiacode.nic.in/bitstream/act.pdf</loc></url>"
                "<url><loc>https://random-blog.example/not-allowed.pdf</loc></url>"
                "</urlset>"
            ),
        )
    if path == "/listing":
        return httpx.Response(
            200,
            text=(
                "<html><body><a href='/bitstream/one.pdf'>Act One</a>"
                "<a href='https://evil.example/bad.pdf'>Bad</a></body></html>"
            ),
            headers={"content-type": "text/html"},
        )
    if path == "/bitstream/cond.pdf":
        if request.headers.get("if-none-match") == '"abc"':
            return httpx.Response(304, headers={"etag": '"abc"'})
        return httpx.Response(
            200,
            content=b"%PDF-1.7 test",
            headers={"content-type": "application/pdf", "etag": '"abc"'},
        )
    if path == "/private/secret.pdf":
        return httpx.Response(200, content=b"secret")
    return httpx.Response(404)


def _fetcher() -> SecureFetcher:
    transport = httpx.MockTransport(_handler)
    client = httpx.AsyncClient(transport=transport, follow_redirects=True)
    return SecureFetcher(
        client=client,
        verify_dns=False,
        rate_limit_per_minute=600,
        enforce_robots=True,
        max_retries=0,
    )


def test_url_validation_blocks_non_https_and_private_addresses():
    fetcher = SecureFetcher(
        verify_dns=False, require_official_domain=False, enforce_robots=False, rate_limit_per_minute=600
    )
    with pytest.raises(FetchError):
        fetcher.validate_url("http://www.indiacode.nic.in/bitstream/a.pdf")
    with pytest.raises(FetchError):
        fetcher.validate_url("https://127.0.0.1/bitstream/a.pdf")
    with pytest.raises(FetchError):
        fetcher.validate_url("https://10.0.0.5/bitstream/a.pdf")
    assert fetcher.validate_url("https://www.indiacode.nic.in/bitstream/a.pdf")


@pytest.mark.asyncio
async def test_fetch_respects_robots_and_conditional_requests():
    async with _fetcher() as fetcher:
        result = await fetcher.fetch(f"{BASE}/bitstream/cond.pdf")
        assert result.status_code == 200
        assert result.content.startswith(b"%PDF")
        assert result.etag == '"abc"'

        cached = await fetcher.fetch(f"{BASE}/bitstream/cond.pdf", if_none_match=result.etag)
        assert cached.not_modified
        assert cached.content == b""

        with pytest.raises(FetchError, match="robots.txt"):
            await fetcher.fetch(f"{BASE}/private/secret.pdf")


@pytest.mark.asyncio
async def test_size_limit_rejects_oversized_document():
    transport = httpx.MockTransport(
        lambda request: httpx.Response(
            200, text="x" * 100, headers={"content-type": "text/plain"}
        )
    )
    client = httpx.AsyncClient(transport=transport)
    fetcher = SecureFetcher(
        client=client,
        verify_dns=False,
        enforce_robots=False,
        rate_limit_per_minute=600,
        max_bytes=10,
        max_retries=0,
    )
    with pytest.raises(FetchError, match="maximum download size"):
        await fetcher.fetch(f"{BASE}/bitstream/large.txt")


def _candidate(strategy: str, document_urls=None, extra_config=None) -> SourceCandidate:
    config = {"document_urls": document_urls or [], **(extra_config or {})}
    return SourceCandidate(
        registry_key="SRC_TEST",
        name="Test Act",
        official_domain="www.indiacode.nic.in",
        base_url=BASE if strategy != "LISTING" else f"{BASE}/listing",
        source_category="CENTRAL_ACT",
        jurisdiction="Union of India",
        legal_domains=[],
        document_types=["CENTRAL_ACT"],
        fetch_strategy=strategy,
        parser_strategy="PDF",
        authority_level="TIER 1",
        supported_languages=["English"],
        update_frequency_hours=168,
        source_config=config,
    )


@pytest.mark.asyncio
async def test_static_and_sitemap_discovery_filters_unofficial_urls():
    async with _fetcher() as fetcher:
        static_docs = await discover_documents(
            _candidate("STATIC_DOCUMENT", [f"{BASE}/bitstream/act.pdf"]), fetcher
        )
        assert [doc.url for doc in static_docs] == [f"{BASE}/bitstream/act.pdf"]

        # Explicit static declarations may be extensionless India Code handles.
        handle_docs = await discover_documents(
            _candidate("STATIC_DOCUMENT", [f"{BASE}/handle/123456789/2263"]), fetcher
        )
        assert [doc.url for doc in handle_docs] == [f"{BASE}/handle/123456789/2263"]

        sitemap_docs = await discover_documents(_candidate("SITEMAP"), fetcher)
        assert [doc.url for doc in sitemap_docs] == [f"{BASE}/bitstream/act.pdf"]


@pytest.mark.asyncio
async def test_listing_discovery_keeps_only_official_document_links():
    async with _fetcher() as fetcher:
        docs = await discover_documents(_candidate("LISTING"), fetcher)
    assert [doc.url for doc in docs] == [f"{BASE}/bitstream/one.pdf"]
    assert docs[0].title == "Act One"
