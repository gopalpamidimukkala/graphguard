from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx

from graphguard.graph import SceneGraph


class SceneGraphVisualizer:

    def visualize(
        self,
        graph: SceneGraph,
        output_path: Path,
    ) -> None:

        G = nx.DiGraph()

        for node in graph.nodes:
            G.add_node(node.id, label=node.label)

        for edge in graph.edges:
            G.add_edge(
                edge.source,
                edge.target,
                label=edge.relation.value,
            )

        labels = {
            node.id: node.label
            for node in graph.nodes
        }

        edge_labels = {
            (u, v): data["label"]
            for u, v, data in G.edges(data=True)
        }

        plt.figure(figsize=(10, 8))

        pos = nx.spring_layout(
            G,
            seed=42,
        )

        nx.draw_networkx_nodes(
            G,
            pos,
            node_size=2500,
        )

        nx.draw_networkx_labels(
            G,
            pos,
            labels,
            font_size=11,
            font_weight="bold",
        )

        nx.draw_networkx_edges(
            G,
            pos,
            arrows=True,
            arrowsize=20,
        )

        nx.draw_networkx_edge_labels(
            G,
            pos,
            edge_labels=edge_labels,
            font_size=8,
        )

        plt.axis("off")
        plt.tight_layout()

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        plt.savefig(output_path)
        plt.close()