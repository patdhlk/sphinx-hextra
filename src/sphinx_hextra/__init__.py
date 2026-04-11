"""sphinx-hextra: Hextra-inspired Sphinx theme with component directives."""

from __future__ import annotations

from pathlib import Path
from typing import Any

__version__ = "0.1.0.dev0"

_THEME_PATH = Path(__file__).resolve().parent / "theme"


def setup(app: Any) -> dict[str, Any]:
    app.add_html_theme("sphinx_hextra", str(_THEME_PATH / "sphinx_hextra"))
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
