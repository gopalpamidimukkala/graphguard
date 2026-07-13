from dataclasses import dataclass

from .relation_type import RelationType

@dataclass(slots=True)
class Edge:
    source: int
    target: int
    relation: RelationType