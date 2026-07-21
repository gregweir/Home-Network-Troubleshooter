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


def test_cli_unknown_subcommand_json_to_stderr(capsys):
    code = cli.main(["bogus", "--json"])
    captured = capsys.readouterr()
    assert code == 2
    assert captured.out == ""
    obj = json.loads(captured.err)
    assert "error" in obj


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

def test_cli_flaky_check_becomes_error_finding(monkeypatch, capsys):
    # A check that raises must become an error finding, not abort the run.
    from homenet.checks import dns
    def boom(verbose=False):
        raise RuntimeError("boom")
    monkeypatch.setattr(dns, "run", boom)
    # stub the rest so the run completes
    from homenet.checks import gateway, nat, upnp, speed, wifi
    from homenet.utils import Finding, learn_more_book
    monkeypatch.setattr(gateway, "default_gateway_ip", lambda: "192.168.1.1")
    monkeypatch.setattr(nat, "wan_ip", lambda: "203.0.113.9")
    monkeypatch.setattr(nat, "local_ip", lambda: "192.168.1.5")
    monkeypatch.setattr(upnp, "run", lambda verbose=False: [Finding(
        check="upnp", title="UPnP", status="info", summary="x",
        why_it_matters="w", learn_more=learn_more_book())])
    monkeypatch.setattr(speed, "timed_http_get", lambda url, timeout: (b"x" * 10_000_000, 1.0))
    monkeypatch.setattr(speed, "timed_http_post", lambda url, data, timeout: 1.0)
    monkeypatch.setattr(wifi, "_native_scan", lambda: None)
    monkeypatch.setattr(wifi, "_current_connection", lambda: (None, None))
    code = cli.main(["--json"])
    out = capsys.readouterr().out
    obj = json.loads(out)
    assert code == 2  # an error finding present
    assert any(f["status"] == "error" and f["check"] == "dns" for f in obj["findings"])


def test_python_m_homenet_runs(tmp_path):
    import subprocess, sys
    result = subprocess.run(
        [sys.executable, "-m", "homenet", "--version"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0
    assert "homenet" in result.stdout
