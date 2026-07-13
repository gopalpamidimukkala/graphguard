from pathlib import Path

import cv2

from graphguard.detector import GroundingDINODetector
from graphguard.graph.builder import SceneGraphBuilder

ROOT = Path(__file__).resolve().parent.parent

CONFIG = (
    ROOT
    / "third_party"
    / "GroundingDINO"
    / "groundingdino"
    / "config"
    / "GroundingDINO_SwinT_OGC.py"
)

CHECKPOINT = ROOT / "checkpoints" / "groundingdino_swint_ogc.pth"

IMAGE = ROOT / "data" / "images" / "test.jpg"

image = cv2.imread(str(IMAGE))

detector = GroundingDINODetector(
    config_path=CONFIG,
    checkpoint_path=CHECKPOINT,
)

detections = detector.detect(
    image=image,
    classes=[
        "person",
        "bicycle",
        "helmet",
    ],
)

builder = SceneGraphBuilder()

graph = builder.build(detections)

print("\nNodes")
for node in graph.nodes:
    print(node)

print("\nEdges")
for edge in graph.edges:
    print(edge)