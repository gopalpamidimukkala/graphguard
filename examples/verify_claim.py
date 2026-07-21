from pathlib import Path

# from graphguard.detector import GroundingDINODetector
from graphguard.bootstrap import create_verifier_service

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

SEMANTIC_ROLE_RULES = (
    ROOT / "configs" / "semantic_roles.yaml"
)

ENTITY_SYNONYMS = Path(
    "configs/entity_synonyms.yaml"
)

IMAGE = (
    ROOT
    / "data"
    / "images"
    / "test.jpg"
)

service = create_verifier_service(
    detector_config=CONFIG,
    detector_checkpoint=CHECKPOINT,
    relation_rules=RULES,
    semantic_role_rules=SEMANTIC_ROLE_RULES,
    entity_synonyms=ENTITY_SYNONYMS,
)

result = service.verify(
    image_path=IMAGE,
    claim="A man rides a cycle.",
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

    print(f"{source} --{edge.relation.value}--> {target}")

    print(f"Status : {decision.status.value}")
    print(f"Score  : {edge_result.evidence.score:.2f}")

    matched = (
        edge_result.expected_relations
        & edge_result.observed_relations
    )

    missing = (
        edge_result.expected_relations
        - edge_result.observed_relations
    )

    extra = (
        edge_result.observed_relations
        - edge_result.expected_relations
    )

    print("Matched Relations:")

    if matched:
        for relation in sorted(
            matched,
            key=lambda r: r.value,
        ):
            print(f"  ✓ {relation.value}")
    else:
        print("  (No relations matched)")

    print("Missing Relations:")

    if missing:
        for relation in sorted(
            missing,
            key=lambda r: r.value,
        ):
            print(f"  ✗ {relation.value}")
    else:
        print("  ✓ None")

    print("Additional Observed Relations:")

    if extra:
        for relation in sorted(
            extra,
            key=lambda r: r.value,
        ):
            print(f"  • {relation.value} (extra evidence)")
    else:
        print("  None")

    print()