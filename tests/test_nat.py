from homenet.checks import nat


def test_double_nat_warn(monkeypatch):
    monkeypatch.setattr(nat, "wan_ip", lambda: "192.168.1.5")
    monkeypatch.setattr(nat, "local_ip", lambda: "10.0.0.5")
    findings = nat.run()
    assert findings[0].status == "warn"
    assert "double" in findings[0].summary.lower() or "private" in findings[0].summary.lower()


def test_cgnat_warn(monkeypatch):
    monkeypatch.setattr(nat, "wan_ip", lambda: "100.64.0.1")
    monkeypatch.setattr(nat, "local_ip", lambda: "192.168.1.5")
    assert nat.run()[0].status == "warn"


def test_no_double_nat_ok(monkeypatch):
    monkeypatch.setattr(nat, "wan_ip", lambda: "203.0.113.9")
    monkeypatch.setattr(nat, "local_ip", lambda: "192.168.1.5")
    findings = nat.run()
    assert findings[0].status == "ok"


def test_offline_error(monkeypatch):
    monkeypatch.setattr(nat, "wan_ip", lambda: None)
    monkeypatch.setattr(nat, "local_ip", lambda: "192.168.1.5")
    assert nat.run()[0].status == "error"


def test_verbose_details(monkeypatch):
    monkeypatch.setattr(nat, "wan_ip", lambda: "203.0.113.9")
    monkeypatch.setattr(nat, "local_ip", lambda: "192.168.1.5")
    f = nat.run(verbose=True)[0]
    assert f.details["wan_ip"] == "203.0.113.9"
    assert f.details["lan_ip"] == "192.168.1.5"