from unittest.mock import patch

from homenet.checks import dns


def _resolve_ok(*a, **k):
    return [(None, None, None, None, None)]


def _resolve_fail(*a, **k):
    raise OSError("nope")


def test_dns_ok(monkeypatch):
    monkeypatch.setattr(dns.socket, "getaddrinfo", _resolve_ok)
    # force fast timing
    monkeypatch.setattr(dns.time, "perf_counter", lambda: 0.0)
    findings = dns.run()
    assert findings[0].status == "ok"
    assert "ms" in findings[0].summary


def test_dns_warn_when_slow(monkeypatch):
    # perf_counter increments so elapsed ~ 150ms per resolve
    counter = {"n": 0}
    def fake():
        counter["n"] += 1
        return counter["n"] * 0.150  # 150ms steps
    monkeypatch.setattr(dns.socket, "getaddrinfo", _resolve_ok)
    monkeypatch.setattr(dns.time, "perf_counter", fake)
    findings = dns.run()
    assert findings[0].status == "warn"


def test_dns_error_when_resolve_fails(monkeypatch):
    monkeypatch.setattr(dns.socket, "getaddrinfo", _resolve_fail)
    findings = dns.run()
    assert findings[0].status == "error"


def test_dns_verbose_details(monkeypatch):
    monkeypatch.setattr(dns.socket, "getaddrinfo", _resolve_ok)
    monkeypatch.setattr(dns.time, "perf_counter", lambda: 0.0)
    findings = dns.run(verbose=True)
    assert "median_ms" in findings[0].details