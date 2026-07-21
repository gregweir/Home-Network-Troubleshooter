"""homenet command-line interface."""
from __future__ import annotations

import argparse
import sys

from .checks import CHECKS, ORDER, ALIASES
from .output import plain as plain_out
from .output import json as json_out
from .utils import Finding, learn_more_book
from . import __version__

_INTRO = "Let's check your home network…"


def _resolve(name: str) -> str | None:
    if name in CHECKS:
        return name
    if name in ALIASES:
        return ALIASES[name]
    return None


def _run_checks(names: list[str], verbose: bool) -> list:
    findings = []
    for name in names:
        try:
            findings.extend(CHECKS[name].run(verbose=verbose))
        except Exception as exc:  # a flaky check never aborts the whole run
            findings.append(Finding(
                check=name, title=name, status="error",
                summary=f"The {name} check failed to run: {exc}",
                why_it_matters="This check hit an unexpected error. The rest of the report is still useful.",
                learn_more=learn_more_book(),
            ))
    return findings


def _exit_code(findings) -> int:
    statuses = {f.status for f in findings}
    if "error" in statuses:
        return 2
    if "warn" in statuses:
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="homenet",
        description="A friendly home network troubleshooter.",
    )
    parser.add_argument("check", nargs="?", default=None,
                        help=f"Run a single check: {', '.join(ORDER)} (alias: double-nat). "
                             "Omit to run all checks.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    parser.add_argument("--verbose", action="store_true", help="Show technical details.")
    parser.add_argument("-V", "--version", action="version", version=f"homenet {__version__}")
    args = parser.parse_args(argv)

    use_colors = sys.stdout.isatty() and not args.json

    if args.check is None:
        names = ORDER
        title = _INTRO
    else:
        resolved = _resolve(args.check)
        if resolved is None:
            if args.json:
                sys.stderr.write(json_out.render_error(
                    f"I don't have a check called '{args.check}'. Try one of: {', '.join(ORDER)}"))
            else:
                print(f"I don't have a check called '{args.check}'. "
                      f"Try one of: {', '.join(ORDER)} (alias: double-nat).")
            return 2
        names = [resolved]
        title = None

    findings = _run_checks(names, verbose=args.verbose)

    if args.json:
        sys.stdout.write(json_out.render(findings))
    else:
        sys.stdout.write(plain_out.render(findings, title=title, verbose=args.verbose,
                                           use_colors=use_colors))
    return _exit_code(findings)


if __name__ == "__main__":
    sys.exit(main())