"""Plain-English (rich) output for homenet."""
from __future__ import annotations

from io import StringIO

from rich.console import Console
from rich.text import Text

from ..utils import Finding

_ICONS = {"ok": "✓", "warn": "!", "info": "•", "error": "✗", "skip": "✗"}
_COLORS = {
    "ok": "green",
    "warn": "yellow",
    "info": "cyan",
    "error": "red",
    "skip": "dim red",
}


def render(findings: list[Finding], title: str | None = None,
           verbose: bool = False, use_colors: bool = True) -> str:
    """Render findings as a friendly human-readable report string."""
    buf = StringIO()
    console = Console(file=buf, color_system="auto" if use_colors else None,
                      highlight=False, soft_wrap=True)
    if title:
        console.print(f"[bold]{title}[/bold]")
        console.print()

    for f in findings:
        icon = _ICONS.get(f.status, "•")
        color = _COLORS.get(f.status, "white")
        header = Text()
        header.append(f"{icon} ", style=color)
        header.append(f"{f.title}: ", style="bold")
        header.append(f.summary)
        console.print(header)

        if f.status in ("warn", "error") and f.why_it_matters:
            console.print(f"  [dim]{f.why_it_matters}[/dim]")

        if verbose and f.details:
            for key, value in f.details.items():
                console.print(f"  [dim]{key}: {value}[/dim]")

        console.print()

    # One consolidated Learn-more line at the end, not repeated after every
    # finding. Findings may carry different URLs; print each unique one once.
    seen: set[str] = set()
    for f in findings:
        if f.learn_more and f.learn_more not in seen:
            seen.add(f.learn_more)
            console.print(f"[dim]Learn more: {f.learn_more}[/dim]")

    return buf.getvalue()