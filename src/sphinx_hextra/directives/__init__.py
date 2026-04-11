"""Directive package — `register()` wires every directive into Sphinx."""

from __future__ import annotations

from typing import Any


def register(app: Any) -> None:
    """Register all sphinx-hextra directives, nodes, and HTML visitors."""
    # Concrete registrations added in each directive's task.
