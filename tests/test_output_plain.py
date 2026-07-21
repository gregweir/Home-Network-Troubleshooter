from homenet.utils import Finding
from homenet.output import plain


def _f(status, summary="A finding", why="Why it matters text", check="dns", title="DNS"):
    return Finding(check=check, title=title, status=status, summary=summary,
                   why_it_matters=why, learn_more="Home Networking for Real People — in development. Updates at https://tartanleaf.com/books/home-networking")


def test_render_includes_summary_and_learn_more():
    out = plain.render([_f("ok"), _f("warn")], use_colors=False)
    assert "DNS" in out
    assert "A finding" in out
    assert "Why it matters text" in out
    assert "Learn more:" in out
    assert "tartanleaf.com/books/home-networking" in out


def test_render_no_colors_when_disabled():
    out = plain.render([_f("ok")], use_colors=False)
    # plain text path should not contain ANSI escape codes
    assert "\x1b[" not in out


def test_render_includes_title_when_provided():
    out = plain.render([_f("ok")], title="Let's check your home network", use_colors=False)
    assert "Let's check your home network" in out


def test_render_verbose_includes_details():
    f = Finding(check="dns", title="DNS", status="ok", summary="s",
                why_it_matters="w", learn_more="l", details={"median_ms": 12.0})
    out = plain.render([f], verbose=True, use_colors=False)
    assert "median_ms" in out
    assert "12.0" in out