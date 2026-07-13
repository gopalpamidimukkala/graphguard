from pathlib import Path

import cv2

from graphguard.detector import GroundingDINODetector
from graphguard.graph.builder import SceneGraphBuilder
from graphguard.graph.geometry import distance, iou

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

for i in range(len(graph.nodes)):
    for j in range(i + 1, len(graph.nodes)):
        a = graph.nodes[i]
        b = graph.nodes[j]

        print(f"{a.label} ↔ {b.label}")
        print("IoU      :", iou(a, b))
        print("Distance :", distance(a, b))
        print()