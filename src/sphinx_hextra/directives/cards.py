"""The ``hextra-cards`` + ``hextra-card`` directives."""

from __future__ import annotations

from typing import Any

from docutils import nodes
from docutils.parsers.rst import directives

from ..nodes import CardNode, CardsNode
from ._base import HextraDirective


def _columns(argument: str) -> int:
    value = int(argument)
    if value < 1 or value > 4:
        raise ValueError("columns must be between 1 and 4")
    return value


class CardsDirective(HextraDirective):
    option_spec = {"columns": _columns}

    def run(self) -> list[nodes.Node]:
        cols = self.options.get("columns", 2)
        node = CardsNode(columns=cols)
        self.nested_parse(node)
        return [node]


class CardDirective(HextraDirective):
    required_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        "link": directives.uri,
        "icon": directives.unchanged,
        "image": directives.uri,
    }

    def run(self) -> list[nodes.Node]:
        node = CardNode(
            title=self.arguments[0],
            link=self.options.get("link", ""),
            icon=self.options.get("icon", ""),
            image=self.options.get("image", ""),
        )
        self.nested_parse(node)
        return [node]


def visit_cards_html(self: Any, node: CardsNode) -> None:
    cols = node.get("columns", 2)
    self.body.append(f'<div class="hx-cards hx-cards--cols-{cols}">')


def depart_cards_html(self: Any, node: CardsNode) -> None:
    self.body.append("</div>")


def visit_card_html(self: Any, node: CardNode) -> None:
    href = node["link"] or "#"
    icon_html = (
        f'<span class="hx-cards__icon hx-icon hx-icon--{node["icon"]}" aria-hidden="true"></span>'
        if node["icon"]
        else ""
    )
    image_html = (
        f'<img class="hx-cards__image" src="{node["image"]}" alt="">'
        if node["image"]
        else ""
    )
    self.body.append(
        f'<a class="hx-cards__item" href="{href}">'
        f"{image_html}"
        f'<div class="hx-cards__header">{icon_html}'
        f'<span class="hx-cards__title">{node["title"]}</span>'
        f"</div>"
        f'<div class="hx-cards__body">'
    )


def depart_card_html(self: Any, node: CardNode) -> None:
    self.body.append("</div></a>")


def register(app: Any) -> None:
    app.add_node(CardsNode, html=(visit_cards_html, depart_cards_html))
    app.add_node(CardNode, html=(visit_card_html, depart_card_html))
    app.add_directive("hextra-cards", CardsDirective)
    app.add_directive("hextra-card", CardDirective)
