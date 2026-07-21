"""Basic download/upload speed check."""
from __future__ import annotations

import os

from ..utils import Finding, timed_http_get, timed_http_post, learn_more_book

_DEFAULT_DOWN = "https://speed.cloudflare.com/__down?bytes=10000000"
_DEFAULT_UP = "https://speed.cloudflare.com/__up"
_UPLOAD_BYTES = 2_000_000


def _mbps(num_bytes: int, seconds: float) -> float:
    if seconds <= 0:
        return 0.0
    return (num_bytes * 8) / 1_000_000 / seconds


def run(verbose: bool = False) -> list[Finding]:
    down_url = os.environ.get("HOMENET_SPEED_DOWN_URL", _DEFAULT_DOWN)
    up_url = os.environ.get("HOMENET_SPEED_UP_URL", _DEFAULT_UP)
    details: dict = {}

    try:
        body, elapsed = timed_http_get(down_url, timeout=30)
    except Exception:
        return [Finding(
            check="speed", title="Speed test", status="error",
            summary="I couldn't reach the speed-test server.",
            why_it_matters="The speed test downloads from a public server, so this usually means you're offline or a firewall blocked it.",
            learn_more=learn_more_book(),
            details={"down_url": down_url} if verbose else None,
        )]
    down = _mbps(len(body), elapsed)
    details.update(download_mbps=round(down, 1), download_bytes=len(body),
                   download_seconds=round(elapsed, 3))

    upload: float | None = None
    try:
        payload = b"x" * _UPLOAD_BYTES
        elapsed_up = timed_http_post(up_url, payload, timeout=30)
        upload = _mbps(len(payload), elapsed_up)
        details.update(upload_mbps=round(upload, 1), upload_bytes=len(payload),
                       upload_seconds=round(elapsed_up, 3))
    except Exception:
        pass  # upload optional; report download only

    summary = f"Download ~{down:.1f} Mbps"
    if upload is not None:
        summary += f", upload ~{upload:.1f} Mbps"
    status = "ok" if down > 1.0 else "warn"
    if status == "warn":
        why = "This is how fast data arrives. Compare it to the speed you pay your provider for — if it's far lower, something between your device and the provider is slowing you down."
    else:
        why = "This is how fast data arrives. Compare it to the speed you pay for to see whether you're getting what you're charged for."
    return [Finding(
        check="speed", title="Speed test", status=status,
        summary=summary, why_it_matters=why, learn_more=learn_more_book(),
        details=details if verbose else None,
    )]