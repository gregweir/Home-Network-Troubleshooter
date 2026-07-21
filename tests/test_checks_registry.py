from homenet import checks


def test_registry_has_all_checks():
    assert set(checks.ORDER) == {"gateway", "dns", "nat", "upnp", "speed", "wifi"}
    for name in checks.ORDER:
        assert hasattr(checks.CHECKS[name], "run")


def test_alias_double_nat():
    assert checks.ALIASES["double-nat"] == "nat"