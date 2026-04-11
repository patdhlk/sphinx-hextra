"""The ``hextra-callout`` directive."""

from __future__ import annotations

from typing import Any

from docutils import nodes

from ..nodes import CalloutNode
from ._base import HextraDirective

_VALID_TYPES = {"info", "warning", "error", "default"}
_DEFAULT_EMOJI = {
    "info": "\u2139",
    "warning": "\u26a0",
    "error": "\u2716",
    "default": "\u2022",
}


class CalloutDirective(HextraDirective):
    optional_arguments = 1
    final_argument_whitespace = False
    option_spec = {"emoji": str}

    def run(self) -> list[nodes.Node]:
        callout_type = (self.arguments[0] if self.arguments else "info").lower()
        if callout_type not in _VALID_TYPES:
            callout_type = "info"
        emoji = self.options.get("emoji", _DEFAULT_EMOJI[callout_type])
        node = CalloutNode(callout_type=callout_type, emoji=emoji)
        self.nested_parse(node)
        return [node]


def visit_callout_html(self: Any, node: CalloutNode) -> None:
    classes = f"hx-callout hx-callout--{node['callout_type']}"
    self.body.append(
        f'<div class="{classes}">'
        f'<span class="hx-callout__icon" aria-hidden="true">{node["emoji"]}</span>'
        f'<div class="hx-callout__body">'
    )


def depart_callout_html(self: Any, node: CalloutNode) -> None:
    self.body.append("</div></div>")


def register(app: Any) -> None:
    app.add_node(CalloutNode, html=(visit_callout_html, depart_callout_html))
    app.add_directive("hextra-callout", CalloutDirective)
