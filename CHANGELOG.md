# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-07-21

Initial release of `homenet`, the friendly home network troubleshooter —
companion to *Home Networking for Real People* (forthcoming).

### Added
- **`gateway`** check — finds your router and reports its address.
- **`dns`** check — tests name resolution and reports timing.
- **`nat`** check — detects double NAT (and carrier-grade NAT).
- **`upnp`** check — best-effort UPnP/IGD discovery.
- **`speed`** check — a basic download/upload throughput test.
- **`wifi`** check — best-effort Wi-Fi congestion scan with a current-connection fallback.
- Plain-English terminal output (rendered with [rich](https://rich.readthedocs.io/)).
- Machine-readable JSON output via `--json`, for scripts and automation.
- `--verbose` flag for technical details (timings, raw IPs, counts).
- Single-check subcommands (`homenet dns`, `homenet nat`, `homenet speed`, …).
- Cross-platform support for Linux, macOS, and Windows.
- Every warning includes a Learn-more link to tartanleaf.com.
- Scriptable exit codes: `0` (ok), `1` (warning), `2` (error/usage).
- MIT license.