"""The ``hextra-tabs`` directive."""

from __future__ import annotations

from typing import Any

from docutils import nodes

from ..nodes import TabNode, TabsNode
from ._base import HextraDirective


class TabsDirective(HextraDirective):
    def run(self) -> list[nodes.Node]:
        wrapper = nodes.section()
        self.nested_parse(wrapper)

        tabs = TabsNode()
        sections = [c for c in wrapper.children if isinstance(c, nodes.section)]
        if sections:
            for section in sections:
                title_node = section.next_node(nodes.title)
                label = title_node.astext() if title_node else ""
                if title_node is not None:
                    title_node.parent.remove(title_node)
                tab = TabNode(label=label)
                for child in list(section.children):
                    section.remove(child)
                    tab += child
                tabs += tab
        else:
            # Fallback: manually split self.content on lines starting with "### ".
            from docutils.statemachine import ViewList

            groups: list[tuple[str, list[tuple[str, int]]]] = []
            current_label: str | None = None
            current_lines: list[tuple[str, int]] = []
            for idx, line in enumerate(self.content):
                stripped = line.lstrip()
                if stripped.startswith("### "):
                    if current_label is not None:
                        groups.append((current_label, current_lines))
                    current_label = stripped[4:].strip()
                    current_lines = []
                else:
                    if current_label is not None:
                        current_lines.append(
                            (line, self.content_offset + idx)
                        )
            if current_label is not None:
                groups.append((current_label, current_lines))

            for label, lines in groups:
                tab = TabNode(label=label)
                vl = ViewList()
                for text, offset in lines:
                    vl.append(text, "<hextra-tabs>", offset)
                self.state.nested_parse(vl, self.content_offset, tab)
                tabs += tab

        return [tabs]


def visit_tabs_html(self: Any, node: TabsNode) -> None:
    labels = [child["label"] for child in node.children if isinstance(child, TabNode)]
    self.body.append('<div class="hx-tabs" data-hx-tabs>')
    self.body.append('<div class="hx-tabs__labels" role="tablist">')
    for idx, label in enumerate(labels):
        active = "hx-tabs__label--active" if idx == 0 else ""
        self.body.append(
            f'<button type="button" class="hx-tabs__label {active}" '
            f'role="tab" data-hx-tab-index="{idx}">{label}</button>'
        )
    self.body.append("</div>")
    self.body.append('<div class="hx-tabs__panels">')


def depart_tabs_html(self: Any, node: TabsNode) -> None:
    self.body.append("</div></div>")


def visit_tab_html(self: Any, node: TabNode) -> None:
    index = node.parent.index(node)
    active = "hx-tabs__panel--active" if index == 0 else ""
    self.body.append(
        f'<div class="hx-tabs__panel {active}" role="tabpanel" data-hx-tab-index="{index}">'
    )


def depart_tab_html(self: Any, node: TabNode) -> None:
    self.body.append("</div>")


def register(app: Any) -> None:
    app.add_node(TabsNode, html=(visit_tabs_html, depart_tabs_html))
    app.add_node(TabNode, html=(visit_tab_html, depart_tab_html))
    app.add_directive("hextra-tabs", TabsDirective)
