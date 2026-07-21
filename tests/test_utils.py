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