"""Conditional sphinx-needs CSS injection."""

from __future__ import annotations

from typing import Any

_NEEDS_CSS = "sphinx-hextra-needs.css"


def _on_builder_inited(app: Any) -> None:
    if "sphinx_needs" in app.extensions:
        app.add_css_file(_NEEDS_CSS)


def register(app: Any) -> None:
    app.connect("builder-inited", _on_builder_inited)
