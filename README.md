# homenet

A friendly home network troubleshooter that diagnoses common problems and explains them in plain English.

`homenet` checks your router, DNS, double NAT, UPnP, internet speed, and Wi-Fi congestion — then tells you what it found and why it matters, in language for humans (not sysadmins).

## Companion to the book

`homenet` is the companion tool to **Home Networking for Real People**, part of the *Smart Tech for Real People* series.

📘 **The book is forthcoming / in development.** Updates and chapters will appear at:
- **https://tartanleaf.com/books/home-networking** — the main book page
- **https://tartanleaf.com/books/smart-tech-for-real-people** — the series page
- **https://tartanleaf.com** — the publisher site (follow for updates)

Every warning the tool prints includes a *Learn more* link pointing back to the book.

## Install

With [pipx](https://pypa.github.io/pipx/) (recommended — keeps `homenet` isolated):

```bash
pipx install .
```

Or from GitHub:

```bash
pipx install git+https://github.com/gregweir/Home-Network-Troubleshooter.git
```

Or, in a virtual environment:

```bash
python -m venv .venv
.venv/bin/pip install .
.venv/bin/homenet
```

**Requirements:** Python 3.10 or newer. Works on Linux, macOS, and Windows.

## Usage

Run every check and read a friendly report:

```bash
homenet
```

Run a single check:

```bash
homenet dns
homenet nat          # double NAT
homenet speed
```

Machine-readable output (great for scripts):

```bash
homenet --json
homenet wifi --json
```

See technical details (timings, raw IPs, counts):

```bash
homenet --verbose
```

### Checks

| Check | What it tells you |
|-------|-------------------|
| `gateway` | Finds your router and reports its address. |
| `dns` | Tests name resolution and timing. |
| `nat` | Detects double NAT (two routers in a row). |
| `upnp` | Checks whether UPnP is responding on your router. |
| `speed` | A basic download/upload speed test. |
| `wifi` | Best-effort scan for Wi-Fi congestion (with a fallback). |

### Exit codes

`homenet` is scriptable:

- `0` — everything looks fine
- `1` — at least one warning
- `2` — a check couldn't run, or a usage error

## Help

- **https://tartanleaf.com/netcheck/help** — troubleshooting and tips (in development)

## License

MIT — see [LICENSE](LICENSE).