from dataclasses import dataclass

from .relations import SpatialRelation

@dataclass(slots=True)
class Edge:
    source: int
    target: int
    relation: SpatialRelation