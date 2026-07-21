"""Double-NAT detection check."""
from __future__ import annotations

from ..utils import Finding, wan_ip, local_ip, is_private_or_cgnat, learn_more_book


def run(verbose: bool = False) -> list[Finding]:
    wan = wan_ip()
    lan = local_ip()
    details = {"wan_ip": wan, "lan_ip": lan} if verbose else None
    if not wan:
        return [Finding(
            check="nat", title="Double NAT", status="error",
            summary="I couldn't reach the internet to find your public address.",
            why_it_matters="This usually means you're offline or a firewall blocked the check — it doesn't by itself mean your network is broken.",
            learn_more=learn_more_book(), details=details,
        )]
    if is_private_or_cgnat(wan):
        return [Finding(
            check="nat", title="Double NAT", status="warn",
            summary=f"Your public address ({wan}) is still a private one — you likely have two routers stacked together.",
            why_it_matters="Double NAT can break port forwarding, online gaming, and some VPNs. It usually means your modem is acting as a router in front of your router.",
            learn_more=learn_more_book(), details=details,
        )]
    return [Finding(
        check="nat", title="Double NAT", status="ok",
        summary=f"Your public address ({wan}) is properly public — no double NAT detected.",
        why_it_matters="Having a single router between you and the internet keeps port forwarding and gaming simpler.",
        learn_more=learn_more_book(), details=details,
    )]