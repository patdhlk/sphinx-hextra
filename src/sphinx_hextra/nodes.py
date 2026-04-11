"""Custom docutils node types used by sphinx-hextra directives."""

from __future__ import annotations

from docutils import nodes


class HextraNode(nodes.General, nodes.Element):
    """Base class for all sphinx-hextra custom nodes."""


class CalloutNode(HextraNode):
    pass


class CardsNode(HextraNode):
    pass


class CardNode(HextraNode):
    pass


class TabsNode(HextraNode):
    pass


class TabNode(HextraNode):
    pass


class StepsNode(HextraNode):
    pass


class StepNode(HextraNode):
    pass


class FileTreeNode(HextraNode):
    pass


class FileTreeEntryNode(HextraNode):
    pass


class HeroNode(HextraNode):
    pass


class FeatureGridNode(HextraNode):
    pass


class FeatureNode(HextraNode):
    pass
