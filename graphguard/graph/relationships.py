from graphguard.graph import Edge, Node, SpatialRelation
from graphguard.graph.geometry import (
    center,
    distance,
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
    ) -> list[str]:

        relations = []

        sx, sy = center(source)
        tx, ty = center(target)

        if sx < tx:
            relations.append(SpatialRelation.LEFT_OF)
        else:
            relations.append(SpatialRelation.RIGHT_OF)

        if sy < ty:
            relations.append(SpatialRelation.ABOVE)
        else:
            relations.append(SpatialRelation.BELOW)

        if iou(source, target) > self.overlap_threshold:
            relations.append(SpatialRelation.OVERLAPS)

        if distance(source, target) < self.near_threshold:
            relations.append(SpatialRelation.NEAR)

        return relations