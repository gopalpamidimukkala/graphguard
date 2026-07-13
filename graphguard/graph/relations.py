from enum import Enum


class SpatialRelation(str, Enum):
    LEFT_OF = "left_of"
    RIGHT_OF = "right_of"
    ABOVE = "above"
    BELOW = "below"
    NEAR = "near"
    OVERLAPS = "overlaps"
    CONTAINS = "contains"
    INSIDE = "inside"