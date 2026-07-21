"""Wi-Fi congestion check: best-effort OS-native scan, fallback to current connection."""
from __future__ import annotations

import platform
import re
import subprocess

from ..utils import Finding, learn_more_book

_CROWDED_24GHZ = 6  # warn if more than this many neighbors share the 2.4GHz band
_CONGESTION_WHY = (
    "Wi-Fi shares the air with nearby networks. When too many crowd the same channel, "
    "everyone slows down. Moving to 5 GHz (or moving the router) usually helps a lot."
)


def _scan_linux() -> list[tuple[str, int, int]] | None:
    """Return list of (ssid, freq_mhz, signal) via nmcli, or None on failure."""
    try:
        out = subprocess.run(
            ["nmcli", "-t", "-f", "SSID,FREQ,SIGNAL", "dev", "wifi", "list"],
            capture_output=True, text=True, timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    results = []
    for line in out.stdout.splitlines():
        parts = line.split(":")
        if len(parts) < 3:
            continue
        ssid, freq_s, signal_s = parts[0], parts[1], parts[-1]
        try:
            freq = int(freq_s)
            signal = int(signal_s)
        except ValueError:
            continue
        results.append((ssid, freq, signal))
    return results if results else None


def _scan_macos() -> list[tuple[str, int, int]] | None:
    try:
        out = subprocess.run(
            ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-s"],
            capture_output=True, text=True, timeout=5)
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    results = []
    for line in out.stdout.splitlines()[1:]:
        cols = line.split()
        if len(cols) < 4:
            continue
        channel_s = cols[3].split(",")[0]
        try:
            channel = int(channel_s)
        except ValueError:
            continue
        freq = 2412 if channel <= 14 else 5180
        results.append(("", freq, 0))
    return results if results else None


def _scan_windows() -> list[tuple[str, int, int]] | None:
    try:
        out = subprocess.run(
            ["netsh", "wlan", "show", "networks", "mode=Bssid"],
            capture_output=True, text=True, timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    results = []
    for line in out.stdout.splitlines():
        m = re.match(r"\s*Channel\s*:\s*(\d+)", line, re.IGNORECASE)
        if m:
            channel = int(m.group(1))
            freq = 2412 if channel <= 14 else 5180
            results.append(("", freq, 0))
    return results if results else None


def _native_scan() -> list[tuple[str, int, int]] | None:
    system = platform.system().lower()
    if system == "linux":
        return _scan_linux()
    if system == "darwin":
        return _scan_macos()
    if system == "windows":
        return _scan_windows()
    return None


def _current_connection() -> tuple[str | None, str | None]:
    """Best-effort current SSID + signal description. Returns (None,None) if unknown."""
    system = platform.system().lower()
    try:
        if system == "linux":
            out = subprocess.run(["iwgetid", "-r"], capture_output=True, text=True, timeout=3)
            ssid = out.stdout.strip() or None
            return ssid, None
        if system == "darwin":
            out = subprocess.run(["networksetup", "-getairportnetwork", "en0"],
                                 capture_output=True, text=True, timeout=3)
            m = re.search(r"Current Wi-Fi Network:\s*(.+)", out.stdout)
            return (m.group(1).strip() if m else None, None)
        if system == "windows":
            out = subprocess.run(["netsh", "wlan", "show", "interfaces"],
                                 capture_output=True, text=True, timeout=3)
            ssid = None
            for line in out.stdout.splitlines():
                m = re.match(r"\s*SSID\s*:\s*(.+)", line)
                if m and m.group(1).strip():
                    ssid = m.group(1).strip()
            return ssid, None
    except (OSError, subprocess.SubprocessError):
        pass
    return None, None


def run(verbose: bool = False) -> list[Finding]:
    scan = _native_scan()
    if scan:
        neighbors_24 = sum(1 for _, freq, _ in scan if freq < 4000)
        neighbors_5 = sum(1 for _, freq, _ in scan if freq >= 4000)
        crowded = neighbors_24 > _CROWDED_24GHZ
        status = "warn" if crowded else "ok"
        if crowded:
            summary = f"{neighbors_24} nearby networks share the 2.4 GHz band — that's crowded."
        else:
            summary = f"Found {neighbors_24} nearby 2.4 GHz network(s) and {neighbors_5} on 5 GHz; not too crowded."
        return [Finding(
            check="wifi", title="Wi-Fi congestion", status=status,
            summary=summary, why_it_matters=_CONGESTION_WHY, learn_more=learn_more_book(),
            details={"mode": "full_scan", "neighbors_24ghz": neighbors_24,
                     "neighbors_5ghz": neighbors_5} if verbose else None,
        )]

    # fallback: current connection only
    ssid, signal = _current_connection()
    details = {"mode": "current_only", "ssid": ssid, "signal": signal} if verbose else None
    findings = []
    if ssid:
        findings.append(Finding(
            check="wifi", title="Wi-Fi connection", status="info",
            summary=f"You're connected to \"{ssid}\".",
            why_it_matters="I couldn't scan for nearby networks (this often needs extra permission), so I can't measure congestion directly.",
            learn_more=learn_more_book(), details=details,
        ))
    else:
        findings.append(Finding(
            check="wifi", title="Wi-Fi congestion", status="info",
            summary="I couldn't scan for nearby networks.",
            why_it_matters="Scanning usually needs extra permission. I couldn't measure congestion directly, but the tips below still apply.",
            learn_more=learn_more_book(), details=details,
        ))
    findings.append(Finding(
        check="wifi", title="Wi-Fi congestion", status="info",
        summary="Crowded channels slow everyone down.",
        why_it_matters=_CONGESTION_WHY, learn_more=learn_more_book(),
        details=None,
    ))
    return findings