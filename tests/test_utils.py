from homenet.utils import Finding, book_url, learn_more_book, learn_more_site, BOOK_HOME


def test_finding_to_dict_details_defaults_to_empty_dict():
    f = Finding(check="dns", title="DNS", status="ok", summary="s",
                why_it_matters="w", learn_more="l")
    d = f.to_dict()
    assert d["details"] == {}
    assert d["status"] == "ok"
    assert d["check"] == "dns"


def test_finding_to_dict_keeps_details_when_provided():
    f = Finding(check="dns", title="DNS", status="warn", summary="s",
                why_it_matters="w", learn_more="l", details={"ms": 12.0})
    assert f.to_dict()["details"] == {"ms": 12.0}


def test_finding_rejects_invalid_status():
    import pytest
    with pytest.raises(ValueError):
        Finding(check="dns", title="DNS", status="bogus", summary="s",
                why_it_matters="w", learn_more="l")


def test_learn_more_book_contains_book_url_and_in_development_language():
    s = learn_more_book()
    assert BOOK_HOME in s
    assert "in development" in s


def test_book_url_known_slugs():
    assert book_url("home-networking") == BOOK_HOME
    assert book_url("smart-tech-for-real-people") == "https://tartanleaf.com/books/smart-tech-for-real-people"
    assert book_url("netcheck/help") == "https://tartanleaf.com/netcheck/help"


def test_learn_more_site():
    assert learn_more_site() == "Updates at https://tartanleaf.com"

import ipaddress
from unittest.mock import patch, MagicMock

import homenet.utils as u


def test_is_private_or_cgnat_detects_private_ranges():
    assert u.is_private_or_cgnat("192.168.1.1")
    assert u.is_private_or_cgnat("10.0.0.1")
    assert u.is_private_or_cgnat("172.16.4.4")
    assert u.is_private_or_cgnat("100.64.0.1")   # CGNAT


def test_is_private_or_cgnat_passes_public():
    assert not u.is_private_or_cgnat("203.0.113.5")
    assert not u.is_private_or_cgnat("8.8.8.8")


def test_is_private_or_cgnat_invalid_string():
    assert not u.is_private_or_cgnat("not-an-ip")


def test_local_ip_returns_source_ip(monkeypatch):
    fake_sock = MagicMock()
    fake_sock.getsockname.return_value = ("192.168.1.42", 80)
    monkeypatch.setattr(u.socket, "socket", lambda *a, **k: fake_sock)
    assert u.local_ip() == "192.168.1.42"
    fake_sock.close.assert_called_once()


def test_local_ip_returns_none_on_error(monkeypatch):
    def boom(*a, **k):
        raise OSError("no network")
    monkeypatch.setattr(u.socket, "socket", boom)
    assert u.local_ip() is None


def test_wan_ip_returns_stripped_text(monkeypatch):
    resp = MagicMock(text="  203.0.113.9\n", raise_for_status=lambda: None)
    monkeypatch.setattr(u.requests, "get", lambda url, timeout: resp)
    assert u.wan_ip() == "203.0.113.9"


def test_wan_ip_returns_none_on_request_error(monkeypatch):
    def boom(url, timeout):
        raise u.requests.RequestException("offline")
    monkeypatch.setattr(u.requests, "get", boom)
    assert u.wan_ip() is None


def test_timed_http_get_returns_body_and_elapsed(monkeypatch):
    resp = MagicMock(content=b"x" * 1000, raise_for_status=lambda: None)
    monkeypatch.setattr(u.requests, "get", lambda url, timeout: resp)
    body, elapsed = u.timed_http_get("http://x", timeout=5)
    assert body == b"x" * 1000
    assert elapsed >= 0.0


def test_timed_http_post_returns_elapsed(monkeypatch):
    resp = MagicMock(raise_for_status=lambda: None)
    monkeypatch.setattr(u.requests, "post", lambda url, data, timeout: resp)
    elapsed = u.timed_http_post("http://x", b"hello", timeout=5)
    assert elapsed >= 0.0


def test_hex_to_ip():
    assert u._hex_to_ip("0100A8C0") == "192.168.0.1"


def test_default_gateway_ip_linux(monkeypatch):
    proc_content = "Iface\tDestination\tGateway\tFlags\nwlan0\t00000000\t0100A8C0\t0003\n"
    import io
    monkeypatch.setattr("builtins.open", lambda p, *a, **k: io.StringIO(proc_content) if str(p) == "/proc/net/route" else open(p, *a, **k))
    monkeypatch.setattr(u.platform, "system", lambda: "Linux")
    assert u.default_gateway_ip() == "192.168.0.1"


def test_default_gateway_ip_none_when_no_default(monkeypatch):
    proc_content = "Iface\tDestination\tGateway\tFlags\nwlan0\t0102A8C0\t00000000\t0003\n"
    import io
    monkeypatch.setattr("builtins.open", lambda p, *a, **k: io.StringIO(proc_content) if str(p) == "/proc/net/route" else open(p, *a, **k))
    monkeypatch.setattr(u.platform, "system", lambda: "Linux")
    assert u.default_gateway_ip() is None
