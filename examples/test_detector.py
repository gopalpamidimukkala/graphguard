from pathlib import Path

from graphguard.detector.grounding_dino import GroundingDINODetector


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


detector = GroundingDINODetector(
    config_path=CONFIG,
    checkpoint_path=CHECKPOINT,
    device="cpu",
)

print("Detector initialized successfully!")