from graphguard.graph import SceneGraph, RelationType, relation_property, RelationProperty

from .relation_mapper import RelationMapper


class RelationMatcher:

    def __init__(self, mapper: RelationMapper):
        self.mapper = mapper

    def match(
        self,
        image_graph: SceneGraph,
        source_image_id: int,
        target_image_id: int,
        semantic_relation: RelationType,
    ) -> tuple[set[RelationType], set[RelationType]]:

        expected = self.mapper.required_relations(
            semantic_relation
        )

        observed = set()

        for edge in image_graph.edges:

            # Forward direction
            if (
                edge.source == source_image_id
                and edge.target == target_image_id
            ):
                observed.add(edge.relation)

            # Symmetric relations
            elif (
                relation_property(edge.relation)
                == RelationProperty.SYMMETRIC
                and edge.source == target_image_id
                and edge.target == source_image_id
            ):
                observed.add(edge.relation)

        return expected, observed