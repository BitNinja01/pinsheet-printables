"""Printables Blueprint — routes for viewing and downloading printable PDFs."""

from __future__ import annotations

import logging
import shutil
from pathlib import Path

from flask import (
    Blueprint, current_app, jsonify, render_template,
    send_from_directory, g,
)
from flask_login import current_user, login_required
from source.request_data import base_context

log = logging.getLogger("pinsheet")

bp = Blueprint("printables", __name__, template_folder="templates")


@bp.route("/")
@login_required
def printables_page():
    view_user = getattr(g, "view_user", None)
    if view_user is None:
        log.warning("printables: no view_user for %s", current_user.id)
        return "No user", 400

    output_dir = Path(current_app.config["DATA_DIR"]) / "plugins" / "printables"
    try:
        pdfs = []
        for name in [
            "scorecard_shorthand_single.pdf",
            "scorecard_shorthand_double.pdf",
            "scorecard_shorthand_letter.pdf",
            "bingo.pdf",
            "bingo_double.pdf",
            "bingo_letter.pdf",
        ]:
            path = output_dir / name
            if path.exists():
                pdfs.append({
                    "name": name,
                    "exists": True,
                    "size": path.stat().st_size,
                })
            else:
                pdfs.append({
                    "name": name,
                    "exists": False,
                    "size": 0,
                })

        return render_template(
            "printables.html",
            pdfs=pdfs,
            is_admin=current_user.is_admin,
            current_page="printables",
            **base_context(),
        )
    except Exception:
        log.exception("printables: error rendering page")
        return "Failed to load printables page", 500


@bp.route("/download/<name>")
@login_required
def download_pdf(name):
    output_dir = Path(current_app.config["DATA_DIR"]) / "plugins" / "printables"
    return send_from_directory(str(output_dir), name)


@bp.route("/regenerate", methods=["POST"])
@login_required
def regenerate():
    if not current_user.is_admin:
        return jsonify({"error": "admin only"}), 403

    from . import generate_pdfs

    output_dir = Path(current_app.config["DATA_DIR"]) / "plugins" / "printables"
    try:
        if output_dir.exists():
            shutil.rmtree(output_dir)
        generate_pdfs(output_dir)
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
