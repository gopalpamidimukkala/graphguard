from pathlib import Path

import cv2

from graphguard.detector import GroundingDINODetector
from graphguard.graph.builder import SceneGraphBuilder
from graphguard.parser.extractor import TripletExtractor
from graphguard.parser.text_graph_builder import TextGraphBuilder
from graphguard.verifier.entity_matcher import EntityMatcher
from graphguard.verifier.relation_mapper import RelationMapper
from graphguard.verifier.relation_matcher import RelationMatcher

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

RULES = ROOT / "configs" / "relation_rules.yaml"

IMAGE = ROOT / "data" / "images" / "test.jpg"

image = cv2.imread(str(IMAGE))

detector = GroundingDINODetector(
    CONFIG,
    CHECKPOINT,
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

entity_matcher = EntityMatcher()

mapping = entity_matcher.match(
    image_graph,
    text_graph,
)

relation_mapper = RelationMapper(RULES)

relation_matcher = RelationMatcher(
    relation_mapper
)

edge = text_graph.edges[0]

expected, observed = relation_matcher.match(
    image_graph=image_graph,
    source_image_id=mapping[edge.source],
    target_image_id=mapping[edge.target],
    semantic_relation=edge.relation,
)

print("Expected")
print(expected)

print()

print("Observed")
print(observed)

print()

print("Matched")
print(expected & observed)