"""Shared helpers for sphinx-hextra directives."""

from __future__ import annotations

from docutils.parsers.rst import Directive


class HextraDirective(Directive):
    """Base class. Each concrete directive sets its own spec."""

    has_content = True
    optional_arguments = 0
    required_arguments = 0
    final_argument_whitespace = False
    option_spec: dict = {}

    def nested_parse(self, node) -> None:
        """Parse `self.content` into `node`."""
        self.state.nested_parse(self.content, self.content_offset, node)
