"""The ``hextra-filetree`` directive."""

from __future__ import annotations

from typing import Any

from docutils import nodes

from ..nodes import FileTreeEntryNode, FileTreeNode
from ._base import HextraDirective


def _parse_tree(lines: list[str]) -> list[dict]:
    """Parse an indented bullet list into a nested entry tree.

    Each entry is a dict: {"name": str, "is_folder": bool, "children": [...]}.
    """
    stack: list[tuple[int, list[dict]]] = [(-1, [])]
    for raw in lines:
        stripped = raw.rstrip()
        if not stripped.strip():
            continue
        indent = len(stripped) - len(stripped.lstrip(" "))
        content = stripped.strip()
        if content.startswith("- "):
            content = content[2:]
        name = content.strip()
        is_folder = name.endswith("/")
        entry = {"name": name, "is_folder": is_folder, "children": []}
        while stack and stack[-1][0] >= indent:
            stack.pop()
        stack[-1][1].append(entry)
        if is_folder:
            stack.append((indent, entry["children"]))
    return stack[0][1]


class FileTreeDirective(HextraDirective):
    def run(self) -> list[nodes.Node]:
        tree = _parse_tree(list(self.content))
        root = FileTreeNode(tree=tree)
        return [root]


def _render_entries(entries: list[dict], body: list[str]) -> None:
    for entry in entries:
        cls = "hx-filetree__folder" if entry["is_folder"] else "hx-filetree__file"
        body.append(f'<li class="{cls}">')
        body.append(f'<span class="hx-filetree__name">{entry["name"]}</span>')
        if entry["is_folder"] and entry["children"]:
            body.append('<ul class="hx-filetree__children">')
            _render_entries(entry["children"], body)
            body.append("</ul>")
        body.append("</li>")


def visit_filetree_html(self: Any, node: FileTreeNode) -> None:
    self.body.append('<ul class="hx-filetree">')
    _render_entries(node["tree"], self.body)


def depart_filetree_html(self: Any, node: FileTreeNode) -> None:
    self.body.append("</ul>")


def register(app: Any) -> None:
    app.add_node(FileTreeNode, html=(visit_filetree_html, depart_filetree_html))
    app.add_node(FileTreeEntryNode, html=(lambda s, n: None, lambda s, n: None))
    app.add_directive("hextra-filetree", FileTreeDirective)
