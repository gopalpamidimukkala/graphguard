from pathlib import Path

import cv2

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

IMAGE = (
    ROOT
    / "data"
    / "images"
    / "test.jpg"
)

# ✅ IMAGE exists now
image = cv2.imread(str(IMAGE))

if image is None:
    raise FileNotFoundError(f"Could not load image: {IMAGE}")

detector = GroundingDINODetector(
    config_path=CONFIG,
    checkpoint_path=CHECKPOINT,
)

detections = detector.detect(
    image=image,
    classes=["person", "bicycle", "helmet"],
)

print(detections)
