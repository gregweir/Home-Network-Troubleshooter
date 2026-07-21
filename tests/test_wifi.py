from unittest.mock import MagicMock

from homenet.checks import wifi


def _proc(stdout="", returncode=0):
    p = MagicMock()
    p.stdout = stdout
    p.returncode = returncode
    return p


def test_wifi_full_scan_crowded_warn(monkeypatch):
    # nmcli -t -f SSID,FREQ,SIGNAL dev wifi list: lines of SSID:FREQ:SIGNAL
    # 8 networks all on channel 1 (2412 MHz) -> 8 neighbors on 2.4GHz -> crowded
    lines = "\n".join([
        "MyNet:2412:60",
        "Neighbor1:2412:40",
        "Neighbor2:2412:30",
        "Neighbor3:2412:20",
        "Neighbor4:2412:20",
        "Neighbor5:2412:20",
        "Neighbor6:2412:20",
        "Neighbor7:2412:20",
    ]) + "\n"
    monkeypatch.setattr(wifi.platform, "system", lambda: "Linux")
    monkeypatch.setattr(wifi.subprocess, "run", lambda *a, **k: _proc(lines))
    f = wifi.run()[0]
    assert f.status == "warn"
    fv = wifi.run(verbose=True)[0]
    assert fv.details["mode"] == "full_scan"
    assert fv.details["neighbors_24ghz"] == 8
    assert fv.details["neighbors_5ghz"] == 0


def test_wifi_full_scan_ok(monkeypatch):
    lines = "MyNet:2412:60\nOneOther:5180:40\n"
    monkeypatch.setattr(wifi.platform, "system", lambda: "Linux")
    monkeypatch.setattr(wifi.subprocess, "run", lambda *a, **k: _proc(lines))
    f = wifi.run(verbose=True)[0]
    assert f.status == "ok"
    assert f.details["mode"] == "full_scan"


def test_wifi_fallback_current_only(monkeypatch):
    def boom(*a, **k):
        raise wifi.subprocess.SubprocessError("nope")
    monkeypatch.setattr(wifi.platform, "system", lambda: "Linux")
    monkeypatch.setattr(wifi.subprocess, "run", boom)
    findings = wifi.run(verbose=True)
    # at least one info finding with current_only mode
    modes = [f.details.get("mode") for f in findings if f.details]
    assert "current_only" in modes


def test_wifi_scan_command_failure_falls_back(monkeypatch):
    # nmcli returns nonzero -> fallback
    monkeypatch.setattr(wifi.platform, "system", lambda: "Linux")
    monkeypatch.setattr(wifi.subprocess, "run", lambda *a, **k: _proc("", returncode=1))
    findings = wifi.run(verbose=True)
    assert any(f.details and f.details.get("mode") == "current_only" for f in findings)