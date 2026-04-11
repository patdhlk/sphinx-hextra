"""Landing-page directives: hero and feature grid."""

from __future__ import annotations

from html import escape
from typing import Any

from docutils import nodes
from docutils.parsers.rst import directives

from ..nodes import FeatureGridNode, FeatureNode, HeroNode
from ._base import HextraDirective


class HeroDirective(HextraDirective):
    has_content = False
    option_spec = {
        "title": directives.unchanged_required,
        "tagline": directives.unchanged,
        "cta-text": directives.unchanged,
        "cta-link": directives.uri,
    }

    def run(self) -> list[nodes.Node]:
        node = HeroNode(
            title=self.options["title"],
            tagline=self.options.get("tagline", ""),
            cta_text=self.options.get("cta-text", ""),
            cta_link=self.options.get("cta-link", ""),
        )
        return [node]


class FeatureGridDirective(HextraDirective):
    def run(self) -> list[nodes.Node]:
        node = FeatureGridNode()
        self.nested_parse(node)
        return [node]


class FeatureDirective(HextraDirective):
    required_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        "subtitle": directives.unchanged,
        "image": directives.uri,
        "link": directives.uri,
    }

    def run(self) -> list[nodes.Node]:
        node = FeatureNode(
            title=self.arguments[0],
            subtitle=self.options.get("subtitle", ""),
            image=self.options.get("image", ""),
            link=self.options.get("link", ""),
        )
        self.nested_parse(node)
        return [node]


def visit_hero_html(self: Any, node: HeroNode) -> None:
    cta = ""
    if node["cta_text"] and node["cta_link"]:
        cta = (
            f'<a class="hx-hero__cta" href="{escape(node["cta_link"])}">'
            f'{escape(node["cta_text"])}</a>'
        )
    self.body.append(
        '<section class="hx-hero">'
        '<div class="hx-hero__inner">'
        f'<h1 class="hx-hero__title">{escape(node["title"])}</h1>'
        f'<p class="hx-hero__tagline">{escape(node["tagline"])}</p>'
        f"{cta}"
        "</div></section>"
    )
    raise nodes.SkipNode


def visit_feature_grid_html(self: Any, node: FeatureGridNode) -> None:
    self.body.append('<div class="hx-feature-grid">')


def depart_feature_grid_html(self: Any, node: FeatureGridNode) -> None:
    self.body.append("</div>")


def visit_feature_html(self: Any, node: FeatureNode) -> None:
    image = (
        f'<img class="hx-feature__image" src="{escape(node["image"])}" alt="">'
        if node["image"] else ""
    )
    wrapper_open = (
        f'<a class="hx-feature hx-feature--link" href="{escape(node["link"])}">'
        if node["link"] else '<div class="hx-feature">'
    )
    self.body.append(
        f"{wrapper_open}"
        f"{image}"
        f'<h3 class="hx-feature__title">{escape(node["title"])}</h3>'
        f'<p class="hx-feature__subtitle">{escape(node["subtitle"])}</p>'
        f'<div class="hx-feature__body">'
    )


def depart_feature_html(self: Any, node: FeatureNode) -> None:
    close = "</a>" if node["link"] else "</div>"
    self.body.append(f"</div>{close}")


def register(app: Any) -> None:
    app.add_node(HeroNode, html=(visit_hero_html, lambda s, n: None))
    app.add_node(FeatureGridNode, html=(visit_feature_grid_html, depart_feature_grid_html))
    app.add_node(FeatureNode, html=(visit_feature_html, depart_feature_html))
    app.add_directive("hextra-hero", HeroDirective)
    app.add_directive("hextra-feature-grid", FeatureGridDirective)
    app.add_directive("hextra-feature", FeatureDirective)
