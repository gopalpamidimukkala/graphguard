from dataclasses import dataclass


@dataclass(slots=True)
class Triplet:
    subject: str
    relation: str
    object: str