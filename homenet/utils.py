"""Shared helpers for homenet: the Finding dataclass and tartanleaf.com URLs."""
from __future__ import annotations

from dataclasses import dataclass, asdict

# --- tartanleaf.com URLs (book is forthcoming / in development) ---
BOOK_HOME = "https://tartanleaf.com/books/home-networking"
BOOK_SERIES = "https://tartanleaf.com/books/smart-tech-for-real-people"
SITE = "https://tartanleaf.com"
HELP_URL = "https://tartanleaf.com/netcheck/help"

_VALID_STATUS = {"ok", "warn", "info", "error", "skip"}


def book_url(slug: str = "home-networking") -> str:
    """Return a tartanleaf.com URL for the given slug."""
    if slug == "home-networking":
        return BOOK_HOME
    if slug == "smart-tech-for-real-people":
        return BOOK_SERIES
    return f"{SITE}/{slug}"


def learn_more_book() -> str:
    """Default Learn-more sentence (no 'Learn more:' prefix)."""
    return f"Home Networking for Real People — in development. Updates at {BOOK_HOME}"


def learn_more_site() -> str:
    """Generic site Learn-more sentence (no 'Learn more:' prefix)."""
    return f"Updates at {SITE}"


@dataclass
class Finding:
    """A single check result, readable by both humans and machines."""

    check: str
    title: str
    status: str            # ok | warn | info | error | skip
    summary: str           # plain-English one-liner
    why_it_matters: str     # 1-2 sentences for a non-expert
    learn_more: str         # descriptive sentence, no 'Learn more:' prefix
    details: dict | None = None

    def __post_init__(self) -> None:
        if self.status not in _VALID_STATUS:
            raise ValueError(f"invalid status {self.status!r}; expected one of {_VALID_STATUS}")

    def to_dict(self) -> dict:
        """Serialize to a dict with a guaranteed dict details field (never None)."""
        d = asdict(self)
        if d.get("details") is None:
            d["details"] = {}
        return d

# --- network helpers ---
import os
import socket
import time
import ipaddress
import platform
import subprocess

import requests

_CGNAT = ipaddress.ip_network("100.64.0.0/10")
_PRIVATE_NETWORKS = (
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    _CGNAT,
)


def local_ip() -> str | None:
    """Best-effort primary LAN IPv4 address (no packets actually sent)."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2)
        try:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        finally:
            s.close()
    except OSError:
        return None


def wan_ip(timeout: float = 4.0) -> str | None:
    """Public/WAN IPv4 address via a what's-my-ip endpoint (overridable)."""
    url = os.environ.get("HOMENET_WAN_URL", "https://api.ipify.org")
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        return r.text.strip() or None
    except requests.RequestException:
        return None


def is_private_or_cgnat(ip: str) -> bool:
    """True if ip is RFC1918 private or CGNAT (100.64.0.0/10)."""
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return False
    return any(addr in net for net in _PRIVATE_NETWORKS)


def timed_http_get(url: str, timeout: float = 15.0) -> tuple[bytes, float]:
    """GET url; return (body_bytes, elapsed_seconds). Raises on HTTP error."""
    start = time.perf_counter()
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    return r.content, time.perf_counter() - start


def timed_http_post(url: str, data: bytes, timeout: float = 15.0) -> float:
    """POST data to url; return elapsed_seconds. Raises on HTTP error."""
    start = time.perf_counter()
    r = requests.post(url, data=data, timeout=timeout)
    r.raise_for_status()
    return time.perf_counter() - start


def _hex_to_ip(h: str) -> str:
    """Convert a little-endian hex IPv4 (from /proc/net/route) to dotted form."""
    return ".".join(str(int(h[i:i + 2], 16)) for i in (6, 4, 2, 0))


def default_gateway_ip() -> str | None:
    """Best-effort default gateway IPv4. Cross-platform; returns None if unknown."""
    system = platform.system().lower()
    if system == "linux":
        return _gateway_linux()
    return _gateway_netstat()


def _gateway_linux() -> str | None:
    try:
        with open("/proc/net/route") as f:
            for line in f.readlines()[1:]:
                parts = line.split()
                if len(parts) < 3:
                    continue
                if parts[1] == "00000000":  # default route
                    return _hex_to_ip(parts[2])
    except OSError:
        return None
    return None


def _gateway_netstat() -> str | None:
    try:
        out = subprocess.run(["netstat", "-rn"], capture_output=True, text=True, timeout=5)
    except (OSError, subprocess.SubprocessError):
        return None
    for line in out.stdout.splitlines():
        stripped = line.strip()
        if stripped.startswith("default"):
            parts = stripped.split()
            if len(parts) >= 2:
                gw = parts[1]
                return None if gw == "0.0.0.0" else gw
        elif stripped.startswith("0.0.0.0"):
            # Windows `netstat -rn` default route:
            # Network Destination, Netmask, Gateway, Interface, Metric
            parts = stripped.split()
            if len(parts) >= 3:
                gw = parts[2]
                return None if gw == "0.0.0.0" else gw
    return None
