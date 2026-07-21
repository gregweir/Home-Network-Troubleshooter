"""DNS resolution + timing check."""
from __future__ import annotations

import socket
import time

from ..utils import Finding, learn_more_book

_HOSTS = ["example.com", "cloudflare.com"]
_SLOW_MS = 100.0


def run(verbose: bool = False) -> list[Finding]:
    times_ms: list[float] = []
    for host in _HOSTS:
        start = time.perf_counter()
        try:
            socket.getaddrinfo(host, None)
        except OSError:
            return [Finding(
                check="dns", title="DNS resolution", status="error",
                summary=f"I couldn't look up {host}.",
                why_it_matters="DNS turns website names into the addresses computers use. When it fails, web pages and apps won't load even though you may be connected.",
                learn_more=learn_more_book(),
                details={"host": host} if verbose else None,
            )]
        times_ms.append((time.perf_counter() - start) * 1000)

    median = sorted(times_ms)[len(times_ms) // 2]
    status = "warn" if median > _SLOW_MS else "ok"
    if status == "warn":
        why = "Your DNS responder is a bit slow, which can make the whole web feel sluggish even on fast internet."
    else:
        why = "Your DNS is responding quickly, so web pages should start loading promptly."
    return [Finding(
        check="dns", title="DNS resolution", status=status,
        summary=f"Resolves names in about {median:.0f} ms.",
        why_it_matters=why, learn_more=learn_more_book(),
        details={"median_ms": round(median, 1),
                 "samples_ms": [round(t, 1) for t in times_ms]} if verbose else None,
    )]