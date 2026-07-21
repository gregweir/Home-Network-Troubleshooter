"""Gateway (router) detection check."""
from __future__ import annotations

from ..utils import Finding, default_gateway_ip, learn_more_book


def _detect_model(gateway_ip: str) -> str | None:
    """Best-effort: no model detection in MVP. Returns None."""
    return None


def run(verbose: bool = False) -> list[Finding]:
    gw = default_gateway_ip()
    details = {"gateway": gw, "model": None} if verbose else None
    if not gw:
        return [Finding(
            check="gateway", title="Router (gateway)", status="error",
            summary="I couldn't find your router's address.",
            why_it_matters="Your router is the box that connects your home to the internet. If I can't find it, you may be offline or the network is unusual.",
            learn_more=learn_more_book(), details=details,
        )]
    model = _detect_model(gw)
    summary = f"Your router is at {gw}."
    if model:
        summary = f"Your router is at {gw} (looks like a {model})."
        details = {"gateway": gw, "model": model} if verbose else None
    return [Finding(
        check="gateway", title="Router (gateway)", status="ok",
        summary=summary,
        why_it_matters="Your router is the brain of your home network — every device talks to it to reach the internet.",
        learn_more=learn_more_book(), details=details,
    )]