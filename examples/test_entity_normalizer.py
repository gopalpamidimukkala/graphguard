from pathlib import Path

from graphguard.verifier.entity_normalizer import (
    EntityNormalizer,
)

normalizer = EntityNormalizer(
    Path("configs/entity_synonyms.yaml")
)

labels = [
    "human",
    "person",
    "bike",
    "bicycle",
    "automobile",
    "car",
    "helmet",
]

for label in labels:
    print(
        f"{label:12} -> {normalizer.normalize(label)}"
    )