from homenet.checks import speed


def test_speed_ok(monkeypatch):
    monkeypatch.setattr(speed, "timed_http_get", lambda url, timeout: (b"x" * 10_000_000, 1.0))
    monkeypatch.setattr(speed, "timed_http_post", lambda url, data, timeout: 0.5)
    f = speed.run()[0]
    assert f.status == "ok"
    assert "Mbps" in f.summary


def test_speed_math_download(monkeypatch):
    monkeypatch.setattr(speed, "timed_http_get", lambda url, timeout: (b"x" * 10_000_000, 1.0))
    monkeypatch.setattr(speed, "timed_http_post", lambda url, data, timeout: 1.0)
    f = speed.run(verbose=True)[0]
    # 10MB in 1s = 80 Mbps
    assert abs(f.details["download_mbps"] - 80.0) < 0.1
    assert f.details["upload_mbps"] == 16.0  # 2MB in 1s = 16 Mbps


def test_speed_error_when_download_fails(monkeypatch):
    def boom(url, timeout):
        raise Exception("offline")
    monkeypatch.setattr(speed, "timed_http_get", boom)
    f = speed.run()[0]
    assert f.status == "error"


def test_speed_warn_on_near_zero(monkeypatch):
    monkeypatch.setattr(speed, "timed_http_get", lambda url, timeout: (b"x" * 100, 10.0))
    monkeypatch.setattr(speed, "timed_http_post", lambda url, data, timeout: 10.0)
    assert speed.run()[0].status == "warn"