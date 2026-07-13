from graphguard.parser.extractor import TripletExtractor
from graphguard.parser.text_graph_builder import TextGraphBuilder

extractor = TripletExtractor()

triplets = extractor.extract(
    "A person rides a bicycle while wearing a helmet."
)

builder = TextGraphBuilder()

graph = builder.build(triplets)

print("\nNodes")
for node in graph.nodes:
    print(node)

print("\nEdges")
for edge in graph.edges:
    print(edge)