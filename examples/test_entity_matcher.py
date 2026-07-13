from pathlib import Path

import cv2

from graphguard.detector import GroundingDINODetector
from graphguard.graph.builder import SceneGraphBuilder
from graphguard.parser.extractor import TripletExtractor
from graphguard.parser.text_graph_builder import TextGraphBuilder
from graphguard.verifier.entity_matcher import EntityMatcher

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

image_graph = SceneGraphBuilder().build(detections)

triplets = TripletExtractor().extract(
    "A person rides a bicycle."
)

text_graph = TextGraphBuilder().build(triplets)

matcher = EntityMatcher()

mapping = matcher.match(
    image_graph,
    text_graph,
)

print(mapping)