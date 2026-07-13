from enum import Enum

class RelationProperty(Enum):
    SYMMETRIC = "symmetric"
    DIRECTIONAL = "directional"


class RelationType(str, Enum):
    # Spatial Relations
    LEFT_OF = "left_of"
    RIGHT_OF = "right_of"
    ABOVE = "above"
    BELOW = "below"
    NEAR = "near"
    OVERLAPS = "overlaps"
    CONTAINS = "contains"
    INSIDE = "inside"

    # Semantic Relations
    RIDE = "ride"
    WEAR = "wear"
    HOLD = "hold"
    SIT_ON = "sit_on"
    NEXT_TO = "next_to"

    # Generic
    UNKNOWN = "unknown"

RELATION_PROPERTIES = {
    RelationType.NEAR: RelationProperty.SYMMETRIC,
    RelationType.OVERLAPS: RelationProperty.SYMMETRIC,

    RelationType.ABOVE: RelationProperty.DIRECTIONAL,
    RelationType.BELOW: RelationProperty.DIRECTIONAL,
    RelationType.LEFT_OF: RelationProperty.DIRECTIONAL,
    RelationType.RIGHT_OF: RelationProperty.DIRECTIONAL,
    RelationType.CONTAINS: RelationProperty.DIRECTIONAL,
    RelationType.INSIDE: RelationProperty.DIRECTIONAL,

    # Semantic Relations
    RelationType.RIDE: RelationProperty.DIRECTIONAL,
    RelationType.WEAR: RelationProperty.DIRECTIONAL,
    RelationType.HOLD: RelationProperty.DIRECTIONAL,
    RelationType.SIT_ON: RelationProperty.DIRECTIONAL,
    RelationType.NEXT_TO: RelationProperty.SYMMETRIC,
    RelationType.UNKNOWN: RelationProperty.DIRECTIONAL,
}

INVERSE_RELATIONS = {
    RelationType.LEFT_OF: RelationType.RIGHT_OF,
    RelationType.RIGHT_OF: RelationType.LEFT_OF,

    RelationType.ABOVE: RelationType.BELOW,
    RelationType.BELOW: RelationType.ABOVE,

    RelationType.CONTAINS: RelationType.INSIDE,
    RelationType.INSIDE: RelationType.CONTAINS,
}

def relation_property(
    relation: RelationType,
) -> RelationProperty:
    return RELATION_PROPERTIES[relation]

def inverse_relation(
    relation: RelationType,
) -> RelationType | None:
    return INVERSE_RELATIONS.get(relation)