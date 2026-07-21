import json

from homenet.utils import Finding
from homenet.output import json as jsonout


def _f(status, details=None):
    return Finding(check="dns", title="DNS", status=status, summary="s",
                   why_it_matters="w", learn_more="l", details=details)


def test_render_returns_single_json_line():
    out = jsonout.render([_f("ok"), _f("warn", {"x": 1})])
    assert out.endswith("\n")
    assert out.count("\n") == 1
    obj = json.loads(out)
    assert obj["findings"][0]["status"] == "ok"
    assert obj["findings"][1]["details"] == {"x": 1}
    assert obj["findings"][0]["details"] == {}  # None normalized


def test_render_summary_counts_statuses():
    out = jsonout.render([_f("ok"), _f("ok"), _f("warn")])
    obj = json.loads(out)
    assert obj["summary"] == {"ok": 2, "warn": 1, "error": 0, "skip": 0, "info": 0, "total": 3}


def test_render_error():
    obj = json.loads(jsonout.render_error("boom"))
    assert obj["error"] == "boom"