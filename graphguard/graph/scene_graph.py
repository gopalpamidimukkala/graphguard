from dataclasses import dataclass, field

from .edge import Edge
from .node import Node


@dataclass(slots=True)
class SceneGraph:
    nodes: list[Node] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)