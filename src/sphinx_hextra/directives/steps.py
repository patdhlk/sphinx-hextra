"""The ``hextra-steps`` directive."""

from __future__ import annotations

from typing import Any

from docutils import nodes

from ..nodes import StepNode, StepsNode
from ._base import HextraDirective


class StepsDirective(HextraDirective):
    def run(self) -> list[nodes.Node]:
        wrapper = nodes.section()
        self.nested_parse(wrapper)

        steps = StepsNode()
        sections = [c for c in wrapper.children if isinstance(c, nodes.section)]
        if sections:
            for section in sections:
                title_node = section.next_node(nodes.title)
                title = title_node.astext() if title_node else ""
                if title_node is not None:
                    title_node.parent.remove(title_node)
                step = StepNode(title=title)
                for child in list(section.children):
                    section.remove(child)
                    step += child
                steps += step
        else:
            # Fallback: manually split self.content on lines starting with "### ".
            from docutils.statemachine import ViewList

            groups: list[tuple[str, list[tuple[str, int]]]] = []
            current_title: str | None = None
            current_lines: list[tuple[str, int]] = []
            for idx, line in enumerate(self.content):
                stripped = line.lstrip()
                if stripped.startswith("### "):
                    if current_title is not None:
                        groups.append((current_title, current_lines))
                    current_title = stripped[4:].strip()
                    current_lines = []
                else:
                    if current_title is not None:
                        current_lines.append(
                            (line, self.content_offset + idx)
                        )
            if current_title is not None:
                groups.append((current_title, current_lines))

            for title, lines in groups:
                step = StepNode(title=title)
                vl = ViewList()
                for text, offset in lines:
                    vl.append(text, "<hextra-steps>", offset)
                self.state.nested_parse(vl, self.content_offset, step)
                steps += step

        return [steps]


def visit_steps_html(self: Any, node: StepsNode) -> None:
    self.body.append('<ol class="hx-steps">')


def depart_steps_html(self: Any, node: StepsNode) -> None:
    self.body.append("</ol>")


def visit_step_html(self: Any, node: StepNode) -> None:
    self.body.append(
        '<li class="hx-steps__item">'
        '<span class="hx-steps__marker" aria-hidden="true"></span>'
        '<div class="hx-steps__content">'
        f'<h3 class="hx-steps__title">{node["title"]}</h3>'
        '<div class="hx-steps__body">'
    )


def depart_step_html(self: Any, node: StepNode) -> None:
    self.body.append("</div></div></li>")


def register(app: Any) -> None:
    app.add_node(StepsNode, html=(visit_steps_html, depart_steps_html))
    app.add_node(StepNode, html=(visit_step_html, depart_step_html))
    app.add_directive("hextra-steps", StepsDirective)
