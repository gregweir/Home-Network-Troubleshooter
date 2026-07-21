import json

from homenet import cli
from homenet.checks import gateway


def test_cli_run_all_json(monkeypatch, capsys):
    from homenet.utils import Finding, learn_more_book
    from homenet.checks import gateway, dns, nat, upnp, speed, wifi
    # stub every check to fast, deterministic, no-network behavior
    monkeypatch.setattr(gateway, "default_gateway_ip", lambda: "192.168.1.1")
    monkeypatch.setattr(dns.socket, "getaddrinfo", lambda *a, **k: [None])
    monkeypatch.setattr(nat, "wan_ip", lambda: "203.0.113.9")
    monkeypatch.setattr(nat, "local_ip", lambda: "192.168.1.5")
    monkeypatch.setattr(speed, "timed_http_get", lambda url, timeout: (b"x" * 10_000_000, 1.0))
    monkeypatch.setattr(speed, "timed_http_post", lambda url, data, timeout: 1.0)
    monkeypatch.setattr(upnp, "run", lambda verbose=False: [Finding(
        check="upnp", title="UPnP", status="info", summary="skipped in test",
        why_it_matters="w", learn_more=learn_more_book())])
    monkeypatch.setattr(wifi, "_native_scan", lambda: None)
    monkeypatch.setattr(wifi, "_current_connection", lambda: (None, None))

    code = cli.main(["--json"])
    out = capsys.readouterr().out
    obj = json.loads(out)
    assert code == 0
    assert len(obj["findings"]) >= 6


def test_cli_unknown_subcommand_exits_2(capsys):
    code = cli.main(["bogus"])
    assert code == 2


def test_cli_subcommand_dns(monkeypatch, capsys):
    from homenet.checks import dns
    monkeypatch.setattr(dns.socket, "getaddrinfo", lambda *a, **k: [None])
    code = cli.main(["dns"])
    assert code == 0
    out = capsys.readouterr().out
    assert "DNS" in out


def test_cli_warn_exits_1(monkeypatch, capsys):
    from homenet.checks import nat
    monkeypatch.setattr(nat, "wan_ip", lambda: "192.168.1.5")
    monkeypatch.setattr(nat, "local_ip", lambda: "10.0.0.5")
    code = cli.main(["nat", "--json"])
    assert code == 1