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

## Installing homenet

`homenet` is a **command-line tool** — it runs in a terminal, not a window. You install it once and then run `homenet` any time you want to check your network.

It needs **Python 3.10 or newer** on your computer, and a small helper tool called **[pipx](https://pypa.github.io/pipx/)**. pipx installs `homenet` cleanly and keeps it separate from the rest of your system, so it won't interfere with anything else. Three steps:

### Step 1 — Check you have Python 3.10 or newer

Open a terminal (see *How to open a terminal* below) and type:

```
python3 --version
```

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

Python 3.10 or newer. Works on Linux, macOS, and Windows. Some checks need a working internet connection; `homenet` degrades gracefully and explains when it can't run something.

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

MIT — see [LICENSE](LICENSE). Free to use, modify, and share.

## Author & Credits

homenet is written by **Greg Weir** and published by **[tartanleaf.com](https://tartanleaf.com)** as the companion tool to *Home Networking for Real People* (part of the *Smart Tech for Real People* series). The book is forthcoming; follow tartanleaf.com for updates.