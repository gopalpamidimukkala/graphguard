from pathlib import Path

from graphguard.graph import RelationType
from graphguard.verifier.relation_mapper import RelationMapper

ROOT = Path(__file__).resolve().parent.parent

mapper = RelationMapper(
    ROOT / "configs" / "relation_rules.yaml"
)

print(
    mapper.required_relations(
        RelationType.RIDE
    )
)

print(
    mapper.required_relations(
        RelationType.WEAR
    )
)