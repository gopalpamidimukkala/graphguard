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

RULES = ROOT / "configs" / "relation_rules.yaml"

SEMANTIC_ROLE_RULES = (
    ROOT / "configs" / "semantic_roles.yaml"
)

IMAGE = ROOT / "data" / "images" / "test.jpg"

detector = GroundingDINODetector(
    config_path=CONFIG,
    checkpoint_path=CHECKPOINT,
)

service = VerifierService(
    detector=detector,
    relation_rules=RULES,
    semantic_role_rules=SEMANTIC_ROLE_RULES,
)

result = service.verify(
    image_path=IMAGE,
    claim="A person rides a bicycle.",
    classes=[
        "person",
        "bicycle",
        "helmet",
    ],
)

print()

print(result.decision.status)
print(result.decision.evidence.score)