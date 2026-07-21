"""Check registry for homenet."""
from . import gateway, dns, nat, upnp, speed, wifi

CHECKS = {
    "gateway": gateway,
    "dns": dns,
    "nat": nat,
    "upnp": upnp,
    "speed": speed,
    "wifi": wifi,
}

ORDER = ["gateway", "dns", "nat", "upnp", "speed", "wifi"]

ALIASES = {"double-nat": "nat"}