from graphguard.graph import SceneGraph


class EntityMatcher:

    def match(
        self,
        image_graph: SceneGraph,
        text_graph: SceneGraph,
    ) -> dict[int, int]:
        """
        Returns:

        text_node_id -> image_node_id
        """

        image_lookup = {
            node.label.lower(): node.id
            for node in image_graph.nodes
        }

        mapping = {}

        for node in text_graph.nodes:

            image_id = image_lookup.get(node.label.lower())

            if image_id is not None:
                mapping[node.id] = image_id

        return mapping