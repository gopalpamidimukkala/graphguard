from graphguard.graph import Node, SceneGraph
from graphguard.graph.relationships import SpatialRelationshipEngine
from graphguard.models import Detection


class SceneGraphBuilder:

    def __init__(self):
        self.relationship_engine = SpatialRelationshipEngine()

    def build(
        self,
        detections: list[Detection],
    ) -> SceneGraph:

        graph = SceneGraph()

        for index, detection in enumerate(detections):
            graph.nodes.append(
                Node(
                    id=index,
                    label=detection.label,
                    bbox=detection.bbox,
                    confidence=detection.confidence,
                )
            )

        graph.edges = self.relationship_engine.build_edges(graph.nodes)

        return graph