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