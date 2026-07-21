"""UPnP/IGD discovery check (SSDP, no extra dependencies)."""
from __future__ import annotations

import socket

from ..utils import Finding, learn_more_book

_SSDP_ADDR = "239.255.255.250"
_SSDP_PORT = 1900
_SEARCH = (
    "M-SEARCH * HTTP/1.1\r\n"
    "HOST: 239.255.255.250:1900\r\n"
    'MAN: "ssdp:discover"\r\n'
    "MX: 2\r\n"
    "ST: urn:schemas-upnp-org:device:InternetGatewayDevice:1\r\n"
    "\r\n"
).encode()


def run(verbose: bool = False) -> list[Finding]:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except OSError:
        return [Finding(
            check="upnp", title="UPnP", status="error",
            summary="I couldn't open a socket to look for UPnP.",
            why_it_matters="UPnP is optional, so this failure doesn't mean your network is broken — it just means I couldn't run this particular check.",
            learn_more=learn_more_book(),
        )]
    found = False
    try:
        s.settimeout(3)
        s.sendto(_SEARCH, (_SSDP_ADDR, _SSDP_PORT))
        try:
            data, _ = s.recvfrom(4096)
            found = b"InternetGatewayDevice".lower() in data.lower() or b"upnp" in data.lower()
        except socket.timeout:
            found = False
    except OSError:
        found = False
    finally:
        s.close()

    if found:
        return [Finding(
            check="upnp", title="UPnP", status="ok",
            summary="Your router answered a UPnP discovery request, so UPnP is on.",
            why_it_matters="UPnP lets devices like game consoles open the ports they need automatically. It's convenient, though some people switch it off for tighter control.",
            learn_more=learn_more_book(),
            details={"response": True} if verbose else None,
        )]
    return [Finding(
        check="upnp", title="UPnP", status="info",
        summary="Your router did not answer a UPnP discovery request.",
        why_it_matters="UPnP being off is perfectly fine and often safer. It just means devices can't open ports automatically — you'd forward ports by hand if you ever need to.",
        learn_more=learn_more_book(),
        details={"response": False} if verbose else None,
    )]