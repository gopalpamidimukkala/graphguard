from graphguard.graph import Edge, Node, RelationType
from graphguard.graph.geometry import (
    center,
    contains,
    distance,
    inside,
    iou,
)


class SpatialRelationshipEngine:

    def __init__(
        self,
        overlap_threshold: float = 0.10,
        near_threshold: float = 300.0,
    ):
        self.overlap_threshold = overlap_threshold
        self.near_threshold = near_threshold

    def build_edges(
    self,
    nodes: list[Node],
    ) -> list[Edge]:

        edges = []

        for i, source in enumerate(nodes):
            for j, target in enumerate(nodes):

                if i >= j:
                    continue

                forward = self.relationships(source, target)
                backward = self.relationships(target, source)

                # Symmetric relationships (store once)
                if RelationType.NEAR in forward:
                    edges.append(
                        Edge(
                            source=source.id,
                            target=target.id,
                            relation=RelationType.NEAR,
                        )
                    )

                if RelationType.OVERLAPS in forward:
                    edges.append(
                        Edge(
                            source=source.id,
                            target=target.id,
                            relation=RelationType.OVERLAPS,
                        )
                    )

                # Directional relationships
                for relation in (
                    RelationType.LEFT_OF,
                    RelationType.RIGHT_OF,
                    RelationType.ABOVE,
                    RelationType.BELOW,
                    RelationType.CONTAINS,
                    RelationType.INSIDE,
                ):
                    if relation in forward:
                        edges.append(
                            Edge(
                                source=source.id,
                                target=target.id,
                                relation=relation,
                            )
                        )

                    if relation in backward:
                        edges.append(
                            Edge(
                                source=target.id,
                                target=source.id,
                                relation=relation,
                            )
                        )

        return edges

        edges = []

        for source in nodes:
            for target in nodes:

                if source.id == target.id:
                    continue

                for relation in self.relationships(source, target):
                    edges.append(
                        Edge(
                            source=source.id,
                            target=target.id,
                            relation=relation,
                        )
                    )

        return edges
        
    def relationships(
    self,
    source: Node,
    target: Node,
) -> list[RelationType]:

        relations = []

        sx, sy = center(source)
        tx, ty = center(target)

        # Directional relationships
        if sx < tx:
            relations.append(RelationType.LEFT_OF)
        else:
            relations.append(RelationType.RIGHT_OF)

        if sy < ty:
            relations.append(RelationType.ABOVE)
        else:
            relations.append(RelationType.BELOW)

        # Geometric relationships
        if iou(source, target) > self.overlap_threshold:
            relations.append(RelationType.OVERLAPS)

        if distance(source, target) < self.near_threshold:
            relations.append(RelationType.NEAR)

        if contains(source, target):
            relations.append(RelationType.CONTAINS)

        if inside(source, target):
            relations.append(RelationType.INSIDE)

        return relations