from pathlib import Path

from graphguard.graph import RelationType, SceneGraph

from .relation_mapper import RelationMapper
from .report import VerificationReport


class GraphMatcher:

    def __init__(self, config_path: Path):
        self.mapper = RelationMapper(config_path)

    def match(
        self,
        image_graph: SceneGraph,
        text_graph: SceneGraph,
    ) -> VerificationReport:

        report = VerificationReport()

        # Map node IDs to labels in the image graph
        image_nodes = {
            node.id: node.label.lower()
            for node in image_graph.nodes
        }

        # Build a lookup of image edges:
        # (source_label, target_label) -> set(relations)
        image_lookup = {}

        for edge in image_graph.edges:
            source = image_nodes.get(edge.source)
            target = image_nodes.get(edge.target)

            if source is None or target is None:
                continue

            key = (source, target)

            image_lookup.setdefault(key, set()).add(edge.relation)

        # Check each text edge
        for edge in text_graph.edges:

            source = text_graph.nodes[edge.source].label.lower()
            target = text_graph.nodes[edge.target].label.lower()

            expected = self.mapper.required_relations(edge.relation)

            actual = image_lookup.get((source, target), set())

            matches = expected & actual

            if len(matches) == len(expected) and expected:
                report.supported.append(edge)

            elif len(matches) > 0:
                report.partially_supported.append(edge)

            else:
                report.hallucinated.append(edge)

        return report