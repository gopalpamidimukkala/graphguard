from pathlib import Path

from graphguard.detector import GroundingDINODetector
from graphguard.services.verifier_service import VerifierService

ROOT = Path(__file__).resolve().parent.parent

CONFIG = (
    ROOT
    / "third_party"
    / "GroundingDINO"
    / "groundingdino"
    / "config"
    / "GroundingDINO_SwinT_OGC.py"
)

CHECKPOINT = (
    ROOT
    / "checkpoints"
    / "groundingdino_swint_ogc.pth"
)

RULES = (
    ROOT
    / "configs"
    / "relation_rules.yaml"
)

IMAGE = (
    ROOT
    / "data"
    / "images"
    / "test.jpg"
)

detector = GroundingDINODetector(
    CONFIG,
    CHECKPOINT,
)

service = VerifierService(
    detector=detector,
    relation_rules=RULES,
)

result = service.verify(
    image_path=IMAGE,
    claim="A person wears a helmet.",
    classes=[
        "person",
        "bicycle",
        "helmet",
    ],
)

print("=" * 60)
print("GraphGuard Verification Report")
print("=" * 60)

print(f"\nClaim:\n{result.claim}")

print(f"\nOverall Decision: {result.overall_decision.status.value}")

print()

print("Per Relation Results")
print("-" * 30)

for edge_result in result.edge_results:

    edge = edge_result.edge
    decision = edge_result.decision

    source = result.text_graph.nodes[edge.source].label
    target = result.text_graph.nodes[edge.target].label

    print(
        f"{source} --{edge.relation.value}--> {target}"
    )
    print(
        f"Status : {decision.status.value}"
    )
    print(
        f"Score  : {decision.evidence.score:.2f}"
    )
    print()

print("\nImage Graph")
print(f"Nodes: {len(result.image_graph.nodes)}")
print(f"Edges: {len(result.image_graph.edges)}")

print("\nText Graph")
print(f"Nodes: {len(result.text_graph.nodes)}")
print(f"Edges: {len(result.text_graph.edges)}")