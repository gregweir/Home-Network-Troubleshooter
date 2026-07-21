"""Machine-readable JSON output for homenet."""
from __future__ import annotations

import json

from ..utils import Finding

_STATUSES = ("ok", "warn", "info", "error", "skip")


def render(findings: list[Finding]) -> str:
    """Render findings as one newline-terminated JSON object."""
    summary = {s: 0 for s in _STATUSES}
    summary["total"] = len(findings)
    for f in findings:
        summary[f.status] = summary.get(f.status, 0) + 1
    payload = {
        "findings": [f.to_dict() for f in findings],
        "summary": summary,
    }
    return json.dumps(payload) + "\n"


def render_error(message: str) -> str:
    """Render a single error as JSON (used for usage/unrecoverable errors)."""
    return json.dumps({"error": message}) + "\n"