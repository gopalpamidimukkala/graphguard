from graphguard.graph import Edge, Node, RelationType, SceneGraph  # Added RelationType
from graphguard.parser import Triplet

RELATION_MAP = {
    "ride": RelationType.RIDE,
    "wear": RelationType.WEAR,
    "hold": RelationType.HOLD,
    "sit": RelationType.SIT_ON,
}


class TextGraphBuilder:

    def build(self, triplets: list[Triplet]) -> SceneGraph:
        graph = SceneGraph()
        node_ids = {}
        next_id = 0

        for triplet in triplets:
            for entity in (triplet.subject, triplet.object):
                if entity not in node_ids:
                    node_ids[entity] = next_id
                    
                    graph.nodes.append(
                        Node(
                            id=next_id,
                            label=entity,
                            bbox=(0, 0, 0, 0),
                            confidence=1.0,
                        )
                    )
                    next_id += 1

            graph.edges.append(
                Edge(
                    source=node_ids[triplet.subject],
                    target=node_ids[triplet.object],
                    relation=RELATION_MAP.get(
                        triplet.relation,
                        RelationType.UNKNOWN,
                    ),
                )
            )

        return graph
