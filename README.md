# homenet

A friendly home network troubleshooter that diagnoses common problems and explains them in plain English.

`homenet` checks your router, DNS, double NAT, UPnP, internet speed, and Wi-Fi congestion — then tells you what it found and why it matters, in language for humans (not sysadmins).

> **Project status:** Early public release, version 0.1.1. The core diagnostic checks are usable now, but results may vary by operating system, network configuration, and permissions. Bug reports and practical feedback are welcome.

## Companion to the book

homenet is a free companion utility for the forthcoming *Home Networking for Real People*. The book is still in development and is not currently available for purchase. The utility works independently and does not require the book.

- **https://www.tartanleaf.com/smart-tech/home-networking/** — the book page
- **https://www.tartanleaf.com/smart-tech/** — the Smart Tech series page
- **https://www.tartanleaf.com/netcheck/** — the project page (follow for updates)

## Installing homenet

`homenet` is a **command-line tool** — it runs in a terminal, not a window. You install it once and then run `homenet` any time you want to check your network.

It needs **Python 3.10 or newer** on your computer, and a small helper tool called **[pipx](https://pypa.github.io/pipx/)**. pipx installs `homenet` cleanly and keeps it separate from the rest of your system, so it won't interfere with anything else. Three steps:

### Step 1 — Check you have Python 3.10 or newer

Open a terminal (see *How to open a terminal* below) and check your version:

- **Windows:** `py --version`
- **macOS / Linux:** `python3 --version`

If it prints `Python 3.10` or higher (for example `Python 3.12.1`), you're set — go to Step 2. If it says "command not found" or shows an older version, install Python first:

- **macOS:** Download the installer from <https://www.python.org/downloads/macos/> and run it. Or, if you use [Homebrew](https://brew.sh/): `brew install python`
- **Windows:** Download from <https://www.python.org/downloads/windows/> — during setup, tick the box **"Add python.exe to PATH"**. Or get "Python" from the Microsoft Store.
- **Linux:** Most distributions already have Python 3.10+. If not, use your package manager. On Ubuntu/Debian: `sudo apt update && sudo apt install python3 python3-pip python3-venv`

**How to open a terminal:**
- **macOS:** Applications → Utilities → Terminal
- **Windows:** Start menu → type `PowerShell` (or "Command Prompt") → open it
- **Linux:** Usually `Ctrl`+`Alt`+`T`, or search for "Terminal"

### Step 2 — Install pipx (the installer helper)

First check whether you already have it:

```
pipx --version
```

If that prints a version number, skip to Step 3. Otherwise install pipx:

- **macOS:** `brew install pipx` then `pipx ensurepath` — close your terminal and open a new one afterward.
- **Windows:** `pip install --user pipx` then `python -m pipx ensurepath` — close your terminal and open a new one afterward.
- **Linux:** On Ubuntu/Debian: `sudo apt install pipx` then `pipx ensurepath`. On other distributions: `pip install --user pipx` then `python -m pipx ensurepath`. Close and reopen your terminal.

### Step 3 — Install homenet

With pipx ready, install homenet straight from GitHub (no need to download anything first):

```
pipx install git+https://github.com/gregweir/Home-Network-Troubleshooter.git
```

This fetches the code from GitHub, so it also needs **Git** installed on your computer (Git comes preinstalled on macOS and most Linux setups; on Windows get it from <https://git-scm.com/download/win>).

That's it — `homenet` is now available from any terminal. (If you downloaded this source code instead, open a terminal in the project folder and run `pipx install .`)

#### Trouble on Windows? (`Unable to read current working directory`)

On some Windows setups, the install above fails near the end with a message like `fatal: Unable to read current working directory: No such file or directory`. This is a known quirk in how `pipx` re-clones a git URL on Windows — it's not a problem with `homenet`, and the fix is to install from a local copy instead. In PowerShell:

```powershell
cd $HOME
git clone https://github.com/gregweir/Home-Network-Troubleshooter.git
cd Home-Network-Troubleshooter
pipx install .
```

If `pipx` says `homenet` is already installed, run `pipx uninstall homenet` first, or use `pipx install --force .`. Then check it with `homenet --version`.

### Keeping it up to date, and removing it

- **Update:** `pipx upgrade homenet`
- **Uninstall:** `pipx uninstall homenet`

### Requirements

Python 3.10 or newer, pipx, and Git. Works on Linux, macOS, and Windows. Some checks need a working internet connection; `homenet` degrades gracefully and explains when it can't run something.

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

## Privacy and network activity

Most checks run locally. homenet does not change router settings or upload your diagnostic report.

Some tests necessarily contact external services:
- DNS tests resolve `example.com` and `cloudflare.com`.
- The public-address test contacts `api.ipify.org`.
- The optional speed test downloads and uploads test data through Cloudflare's speed-test service.

Results may display your router's local address and your public IP address. Verbose output can contain additional technical details. Review and redact output before posting screenshots or diagnostic reports publicly.

## Limitations

homenet is a diagnostic aid, not a replacement for your ISP, router manufacturer, or qualified network support. Speed results are approximate, and Wi-Fi information depends on operating-system support and permissions. homenet reports findings but does not modify network settings.

## Support

- **Usage help:** [NetCheck Help](https://www.tartanleaf.com/netcheck/help/)
- **Project information:** [NetCheck](https://www.tartanleaf.com/netcheck/)
- **Bugs and feature requests:** [GitHub Issues](https://github.com/gregweir/Home-Network-Troubleshooter/issues)

## License

MIT — see [LICENSE](LICENSE). Free to use, modify, and share.

## Author & Credits

homenet is written by **Greg Weir** and published by **[tartanleaf.com](https://www.tartanleaf.com)** as the companion tool to *Home Networking for Real People* (part of the *Smart Tech for Real People* series). The book is still in development; follow [tartanleaf.com](https://www.tartanleaf.com/netcheck/) for updates.