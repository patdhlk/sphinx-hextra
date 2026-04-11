"""Directive package — `register()` wires every directive into Sphinx."""

from __future__ import annotations

from typing import Any

from . import callout, cards, steps, tabs


def register(app: Any) -> None:
    callout.register(app)
    cards.register(app)
    tabs.register(app)
    steps.register(app)
