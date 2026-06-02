[![Release](https://img.shields.io/github/v/release/BitNinja01/pinsheet-printables.svg?style=for-the-badge&color=green)](https://github.com/BitNinja01/pinsheet-printables/releases)
[![Downloads](https://img.shields.io/github/downloads/BitNinja01/pinsheet-printables/total.svg?style=for-the-badge&color=green)](https://github.com/BitNinja01/pinsheet-printables/releases)
[![Platform](https://img.shields.io/badge/Platforms-Linux%20|%20macOS%20|%20Windows-white.svg?style=for-the-badge&color=green)](https://github.com/BitNinja01/pinsheet-printables)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg?style=for-the-badge&color=green)](https://www.python.org/downloads/)

---

> Ready-to-print golf forms for the course and the clubhouse.

---

A plugin for [PinSheet](https://github.com/BitNinja01/pinsheet), the golf stats and round tracking app. Generates printable PDF golf forms — blank scorecards and par bingo cards.

- **Blank Scorecards** — 18-hole shorthand scorecard with Score / FW / GIR / Putts / Pen columns
- **Par Bingo** — 18-hole bingo cards for tracking par, birdie, and scoring achievements
- **Multiple formats** — single-sided tall (4.25" × 14"), double-sided tall, and letter (8.5" × 11")
- **Regenerate on demand** — admins can regenerate all PDFs from the web UI

### Setup

Requires PinSheet v2.1.0+.

---

## Installation

### Prerequisites

- **Python 3.11+**
- **PinSheet v2.1.0+** — the parent app must be installed and its plugin system available
- **System libraries** — `cairosvg` needs libcairo2:

| Platform | Command |
|----------|---------|
| Ubuntu/Debian | `sudo apt install libcairo2-dev` |
| macOS (Homebrew) | `brew install cairo` |
| Windows | Bundled with `cairosvg` wheel; no extra steps |

**PinSheet's launcher (`launch.sh`/`launch.bat`) auto-installs plugin dependencies at startup** — no manual `pip install` needed when running inside PinSheet. The steps below just place the files in the right directory.

### Option 1: Release zip (recommended)

Download the latest release from the [releases page](https://github.com/BitNinja01/pinsheet-printables/releases) and extract it into PinSheet's `plugins/` directory:

```bash
# From your PinSheet install directory
mkdir -p plugins
cd plugins
wget https://github.com/BitNinja01/pinsheet-printables/releases/latest/download/pinsheet-printables_0.3.1.zip
unzip pinsheet-printables_0.3.1.zip -d printables
```

### Option 2: Git clone

```bash
# From your PinSheet install directory
mkdir -p plugins
cd plugins
git clone https://github.com/BitNinja01/pinsheet-printables.git
```

For standalone use outside PinSheet, run `pip install -r requirements.txt` from the printables directory.

### Verify installation

Launch PinSheet — if installed correctly, you'll see a **Printables** nav link. Navigate there to view and download PDFs or click **Regenerate All** (admin only) to rebuild them.

---

## Usage

Navigate to `/printables` in PinSheet's web UI. You'll see a grid of available PDFs:

| File | Description |
|------|-------------|
| `scorecard_shorthand_single.pdf` | 18-hole scorecard (1 sheet, 4.25" × 14") |
| `scorecard_shorthand_double.pdf` | 18-hole scorecard (2 sheets, 4.25" × 14") |
| `scorecard_shorthand_letter.pdf` | 18-hole scorecard (letter size, 8.5" × 11") |
| `bingo.pdf` | Par bingo card (1 sheet, 4.25" × 14") |
| `bingo_double.pdf` | Par bingo card (2 sheets, 4.25" × 14") |
| `bingo_letter.pdf` | Par bingo card (letter size, 8.5" × 11") |

Each card shows its file size. Click **Download** to grab any PDF. Admins see a **Regenerate All** button that deletes and rebuilds all PDFs from scratch.

---

## PDF Formats

### Scorecard (Shorthand)

The scorecard uses a compact 6-column layout:

| Hole | Score | FW | GIR | Putts | Pen |
|------|-------|----|-----|-------|-----|

Holes 1-9 on the first card, 10-18 on the second. Summary rows for OUT, IN, and TOT include crossed-out tally columns for aggregate stats. A Course: and Date: line sits below the table.

### Par Bingo

A 3×6 grid with holes 1-18, each cell showing:
- **Hole number** (large)
- **PAR** and **BIRDIE** labels — circle or cross off as you earn each

A Season: line and instruction ("Cross off each as you earn it.") sit below the grid.

### Page Sizes

- **Tall (4.25" × 14")** — two scorecard/bingo halves per sheet, stacked vertically. Matches the yardage book format from cartographer. Print on legal paper.
- **Letter (8.5" × 11")** — two halves side by side. Print on standard letter paper.

---

## Development

```bash
pip install -r requirements.txt
```

PDFs are generated as SVG via `svgwrite`, rendered to PDF via `cairosvg`, and assembled into multi-page documents via `pypdf`. Font: [JetBrains Mono](https://www.jetbrains.com/lp/mono/) (bundled, auto-installed on startup).
