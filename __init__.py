"""Printables plugin for PinSheet Server.

Generates printable golf forms (blank scorecards, par bingo cards) as PDFs.
"""

from __future__ import annotations

import logging
import shutil
import subprocess
import threading
from pathlib import Path

from .blueprint import bp

log = logging.getLogger("pinsheet")

plugin_info = {
    "name": "pinsheet-printables",
    "version": "0.3.2",
    "description": "Printable golf forms (scorecards, bingo cards)",
    "author": "PinSheet",
}


def _install_fonts() -> None:
    fonts_dir = Path(__file__).parent / "fonts" / "JetBrainsMono"
    target_dir = Path.home() / ".local" / "share" / "fonts" / "pinsheet"
    target_dir.mkdir(parents=True, exist_ok=True)
    needs_cache = False
    for ttf in fonts_dir.glob("*.ttf"):
        dst = target_dir / ttf.name
        if not dst.exists() or dst.stat().st_size != ttf.stat().st_size:
            shutil.copy2(ttf, dst)
            needs_cache = True
    if needs_cache and shutil.which("fc-cache"):
        subprocess.run(["fc-cache", "-f"], check=False)


def generate_pdfs(output_dir: Path) -> None:
    from .scorecard import generate_scorecard_pdf, generate_scorecard_letter_pdf
    from .bingo import generate_bingo_pdf, generate_bingo_letter_pdf

    output_dir.mkdir(parents=True, exist_ok=True)
    generate_scorecard_pdf(output_dir)
    generate_scorecard_letter_pdf(output_dir)
    generate_bingo_pdf(output_dir)
    generate_bingo_letter_pdf(output_dir)


def _startup_background(app) -> None:
    try:
        _install_fonts()
    except Exception:
        log.warning("printables: font installation failed", exc_info=True)

    output_dir = Path(app.config["DATA_DIR"]) / "plugins" / "printables"
    expected = [
        "bingo.pdf",
        "bingo_double.pdf",
        "bingo_letter.pdf",
        "scorecard_shorthand_double.pdf",
        "scorecard_shorthand_letter.pdf",
        "scorecard_shorthand_single.pdf",
    ]
    if not all((output_dir / name).exists() for name in expected):
        try:
            generate_pdfs(output_dir)
            log.info("printables: generated startup PDFs")
        except Exception:
            log.warning("printables: PDF generation failed", exc_info=True)
    else:
        log.info("printables: PDFs already exist, skipping generation")


def _ensure_cairo() -> bool:
    try:
        from cairosvg import svg2pdf
        svg2pdf(bytestring=b"<svg xmlns='http://www.w3.org/2000/svg' width='10' height='10'><rect width='10' height='10'/></svg>")
        return True
    except Exception:
        return False


def register(app):
    app.register_blueprint(bp, url_prefix="/printables")

    # Exempt POST routes from CSRF (same as cartographer)
    csrf_exempt = app.extensions.get("csrf")
    if csrf_exempt is not None:
        for name in ("printables.regenerate",):
            fn = app.view_functions.get(name)
            if fn is not None:
                csrf_exempt.exempt(fn)

    from source.plugin_api import add_block
    pname = plugin_info["name"]

    # 1. Inject CSS
    add_block(app, pname, "head", f'<link rel="stylesheet" href="/plugins/{pname}/static/printables.css">')

    # 2. Add nav link
    if not hasattr(app, "_plugin_nav"):
        app._plugin_nav = []
    app._plugin_nav.append({
        "label": "Printables",
        "url": "/printables/",
        "page_id": "printables",
    })

    # 3. Check cairo availability
    if not _ensure_cairo():
        log.warning("printables: cairosvg/cairo not functional — PDF generation will fail at runtime")

    # 4. Defer slow startup work (font install, PDF generation) to background
    #    so the server can start accepting connections immediately.
    t = threading.Thread(target=_startup_background, args=(app,), daemon=True)
    t.start()


def unregister(app):
    pname = plugin_info["name"]
    output_dir = Path(app.config["DATA_DIR"]) / "plugins" / "printables"
    if output_dir.exists():
        for name in ["bingo.pdf", "bingo_double.pdf", "bingo_letter.pdf", "scorecard_shorthand_double.pdf", "scorecard_shorthand_letter.pdf", "scorecard_shorthand_single.pdf"]:
            (output_dir / name).unlink(missing_ok=True)
        try:
            output_dir.rmdir()
        except OSError:
            pass
    head_tag = f'<link rel="stylesheet" href="/plugins/{pname}/static/printables.css">'
    current_head = app._plugin_blocks.get("head", "")
    app._plugin_blocks["head"] = current_head.replace(head_tag, "").strip()
    app._plugin_nav[:] = [n for n in app._plugin_nav if n.get("page_id") != "printables"]
