"""Secure, policy-aware HTTP fetching for official legal sources.

Every request is bounded, HTTPS-only, DNS/SSRF checked, robots.txt aware, and
redirect validated. Content is treated as untrusted bytes: this module never
interprets page text as instructions.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
import ipaddress
from pathlib import Path
import socket
import time
from typing import Dict, Optional, Tuple
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import httpx

from app.core.config import settings
from app.core.logging import logger
from app.modules.legal_knowledge.source_registry import is_official_indian_domain


class FetchError(RuntimeError):
    """Raised when a source request violates policy or cannot be completed."""


@dataclass(frozen=True)
class FetchResult:
    url: str
    final_url: str
    status_code: int
    content_type: str
    content: bytes
    etag: Optional[str] = None
    last_modified: Optional[str] = None

    @property
    def not_modified(self) -> bool:
        return self.status_code == 304

    @property
    def content_type_encoding(self) -> str:
        """Charset declared in the Content-Type header, defaulting to UTF-8."""
        for part in self.content_type.split(";"):
            if part.strip().lower().startswith("charset="):
                return part.split("=", 1)[1].strip() or "utf-8"
        return "utf-8"


class SecureFetcher:
    """Bounded official-source HTTP client with robots and SSRF enforcement."""

    def __init__(
        self,
        *,
        client: Optional[httpx.AsyncClient] = None,
        timeout: Optional[float] = None,
        max_bytes: Optional[int] = None,
        max_retries: Optional[int] = None,
        backoff_seconds: Optional[float] = None,
        allowed_content_types: Optional[str] = None,
        user_agent: Optional[str] = None,
        verify_dns: bool = True,
        rate_limit_per_minute: Optional[int] = None,
        enforce_robots: bool = True,
        require_official_domain: bool = True,
    ) -> None:
        self.timeout = timeout if timeout is not None else settings.RAG_FETCH_TIMEOUT_SECONDS
        self.max_bytes = max_bytes if max_bytes is not None else settings.RAG_FETCH_MAX_BYTES
        self.max_retries = max_retries if max_retries is not None else settings.RAG_FETCH_MAX_RETRIES
        self.backoff = (
            backoff_seconds if backoff_seconds is not None else settings.RAG_FETCH_RETRY_BACKOFF_SECONDS
        )
        raw_types = allowed_content_types if allowed_content_types is not None else settings.RAG_FETCH_ALLOWED_CONTENT_TYPES
        self.allowed_content_types = {item.strip().lower() for item in raw_types.split(",") if item.strip()}
        self.user_agent = user_agent or settings.RAG_FETCH_USER_AGENT
        self.verify_dns = verify_dns
        self.enforce_robots = enforce_robots
        self.require_official_domain = require_official_domain
        self.rate_limit_per_minute = rate_limit_per_minute or 6
        self._min_interval = 60.0 / max(1, self.rate_limit_per_minute)
        self._last_request: Dict[str, float] = {}
        self._rate_locks: Dict[str, asyncio.Lock] = {}
        self._robots_cache: Dict[str, Tuple[Optional[RobotFileParser], bool]] = {}
        self._client = client or httpx.AsyncClient(
            timeout=self.timeout,
            follow_redirects=True,
            headers={"User-Agent": self.user_agent},
        )
        self._owns_client = client is None

    async def __aenter__(self) -> "SecureFetcher":
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        if self._owns_client:
            await self._client.aclose()

    def validate_url(self, url: str) -> str:
        """Validate scheme, host, and absence of credentials/fragments."""
        try:
            parsed = urlparse(url)
        except Exception as exc:
            raise FetchError(f"Malformed URL: {url!r}") from exc
        if parsed.scheme.lower() != "https":
            raise FetchError(f"Only HTTPS URLs are permitted: {url!r}")
        if parsed.username or parsed.password:
            raise FetchError(f"URL credentials are not permitted: {url!r}")
        if not parsed.hostname:
            raise FetchError(f"URL has no host: {url!r}")
        if self.require_official_domain and not is_official_indian_domain(url):
            raise FetchError(f"URL is not an official Indian legal domain: {url!r}")
        self._validate_host_literal(parsed.hostname)
        return url

    @staticmethod
    def _validate_host_literal(host: str) -> None:
        clean = host.strip("[]").lower()
        try:
            ip = ipaddress.ip_address(clean)
        except ValueError:
            return
        if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_reserved:
            raise FetchError(f"Private or non-routable address refused: {host}")

    async def _resolve_host(self, url: str) -> None:
        if not self.verify_dns:
            return
        host = (urlparse(url).hostname or "").lower()
        try:
            infos = await asyncio.to_thread(socket.getaddrinfo, host, 443, type=socket.SOCK_STREAM)
        except OSError as exc:
            raise FetchError(f"DNS resolution failed for {host}: {exc}") from exc
        for info in infos:
            address = info[4][0]
            self._validate_host_literal(address)

    async def _throttle(self, url: str) -> None:
        host = (urlparse(url).hostname or "").lower()
        lock = self._rate_locks.setdefault(host, asyncio.Lock())
        async with lock:
            now = time.monotonic()
            wait = self._min_interval - (now - self._last_request.get(host, 0.0))
            if wait > 0:
                await asyncio.sleep(wait)
            self._last_request[host] = time.monotonic()

    @staticmethod
    def _origin(url: str) -> str:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"

    async def _robots_policy(self, url: str) -> Tuple[Optional[RobotFileParser], bool]:
        """Return (parser, fetch_succeeded). A 404 means no policy and is allowed."""
        origin = self._origin(url)
        if origin in self._robots_cache:
            return self._robots_cache[origin]

        robots_url = urljoin(origin, "/robots.txt")
        self.validate_url(robots_url)
        await self._resolve_host(robots_url)
        parser: Optional[RobotFileParser] = None
        succeeded = False
        try:
            response = await self._client.get(
                robots_url,
                headers={"User-Agent": self.user_agent},
                timeout=self.timeout,
                follow_redirects=True,
            )
            self._validate_final_url(response)
            if response.status_code == 404:
                succeeded = True
            elif response.status_code < 400:
                parser = RobotFileParser()
                parser.parse(response.text.splitlines())
                succeeded = True
        except (httpx.HTTPError, FetchError) as exc:
            logger.warning("robots.txt unavailable for %s: %s", origin, exc)

        self._robots_cache[origin] = (parser, succeeded)
        return parser, succeeded

    async def robots_allows(self, url: str) -> bool:
        if not self.enforce_robots:
            return True
        parser, succeeded = await self._robots_policy(url)
        if not succeeded:
            return False  # fail closed when policy cannot be established
        if parser is None:
            return True
        return parser.can_fetch(self.user_agent, url)

    def _validate_final_url(self, response: httpx.Response) -> None:
        for hop in [*response.history, response]:
            self.validate_url(str(hop.url))

    def _content_type_allows(self, content_type: str) -> bool:
        base = content_type.split(";", 1)[0].strip().lower()
        return base in self.allowed_content_types or base == ""

    async def fetch(
        self,
        url: str,
        *,
        if_none_match: Optional[str] = None,
        if_modified_since: Optional[str] = None,
        method: str = "GET",
    ) -> FetchResult:
        """Fetch one URL under the configured policy."""
        self.validate_url(url)
        await self._resolve_host(url)
        if not await self.robots_allows(url):
            raise FetchError(f"robots.txt does not permit fetching {url}")

        headers = {"User-Agent": self.user_agent, "Accept": ", ".join(sorted(self.allowed_content_types))}
        if if_none_match:
            headers["If-None-Match"] = if_none_match
        if if_modified_since:
            headers["If-Modified-Since"] = if_modified_since

        last_error: Optional[Exception] = None
        for attempt in range(self.max_retries + 1):
            await self._throttle(url)
            try:
                async with self._client.stream(
                    method, url, headers=headers, follow_redirects=True, timeout=self.timeout
                ) as response:
                    self._validate_final_url(response)
                    if response.status_code == 304:
                        return FetchResult(
                            url=url,
                            final_url=str(response.url),
                            status_code=304,
                            content_type="",
                            content=b"",
                            etag=response.headers.get("etag"),
                            last_modified=response.headers.get("last-modified"),
                        )
                    if response.status_code >= 400:
                        raise FetchError(f"HTTP {response.status_code} fetching {url}")

                    content_type = response.headers.get("content-type", "")
                    if not self._content_type_allows(content_type):
                        raise FetchError(f"Disallowed content type {content_type!r} from {url}")

                    declared_size = response.headers.get("content-length")
                    if declared_size and int(declared_size) > self.max_bytes:
                        raise FetchError(f"Document exceeds maximum download size ({declared_size} bytes)")

                    chunks: list[bytes] = []
                    total = 0
                    async for chunk in response.aiter_bytes():
                        total += len(chunk)
                        if total > self.max_bytes:
                            raise FetchError(f"Document exceeds maximum download size ({self.max_bytes} bytes)")
                        chunks.append(chunk)

                    return FetchResult(
                        url=url,
                        final_url=str(response.url),
                        status_code=response.status_code,
                        content_type=content_type,
                        content=b"".join(chunks),
                        etag=response.headers.get("etag"),
                        last_modified=response.headers.get("last-modified"),
                    )
            except FetchError:
                raise
            except (httpx.HTTPError, OSError, ValueError) as exc:
                last_error = exc
                if attempt < self.max_retries:
                    await asyncio.sleep(self.backoff * (2**attempt))

        raise FetchError(f"Failed to fetch {url}: {last_error}")

    async def sitemap_urls(self, base_url: str) -> list[str]:
        """Discover sitemap URLs only from robots.txt or explicit configuration."""
        self.validate_url(base_url)
        parser, succeeded = await self._robots_policy(base_url)
        if not succeeded:
            return []
        candidates: list[str] = []
        if parser is not None:
            candidates.extend(parser.site_maps() or [])
        origin = self._origin(base_url)
        urls: list[str] = []
        for candidate in candidates:
            normalized = urljoin(origin, candidate)
            self.validate_url(normalized)
            if is_official_indian_domain(normalized):
                urls.append(normalized)
        return urls


def storage_key_for_document(source_key: str, checksum: str, suffix: str = ".bin") -> str:
    """Build a deterministic, traversal-safe raw document storage key."""
    safe_key = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in source_key)[:96]
    safe_suffix = suffix if suffix.startswith(".") and len(suffix) <= 8 else ".bin"
    return f"legal-sources/{safe_key}/{checksum}{safe_suffix}"
