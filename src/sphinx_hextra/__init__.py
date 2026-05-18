"""sphinx-hextra: Hextra-inspired Sphinx theme with component directives."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from . import directives as _directives
from . import needs_integration as _needs_integration

try:
    from ._version import __version__
except ImportError:
    __version__ = "0.0.0+unknown"

_THEME_PATH = Path(__file__).resolve().parent / "theme"


def setup(app: Any) -> dict[str, Any]:
    app.add_html_theme("sphinx_hextra", str(_THEME_PATH / "sphinx_hextra"))
    app.add_js_file("theme-toggle.js")
    app.add_js_file("tabs.js")
    _directives.register(app)
    _needs_integration.register(app)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
