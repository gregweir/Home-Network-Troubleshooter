from unittest.mock import patch, MagicMock

from homenet.checks import gateway


def test_gateway_ok(monkeypatch):
    monkeypatch.setattr(gateway, "default_gateway_ip", lambda: "192.168.1.1")
    findings = gateway.run()
    assert len(findings) == 1
    assert findings[0].status == "ok"
    assert "192.168.1.1" in findings[0].summary
    assert findings[0].learn_more  # non-empty


def test_gateway_error_when_unknown(monkeypatch):
    monkeypatch.setattr(gateway, "default_gateway_ip", lambda: None)
    findings = gateway.run()
    assert findings[0].status == "error"


def test_gateway_verbose_includes_details(monkeypatch):
    monkeypatch.setattr(gateway, "default_gateway_ip", lambda: "192.168.1.1")
    findings = gateway.run(verbose=True)
    assert findings[0].details == {"gateway": "192.168.1.1", "model": None}