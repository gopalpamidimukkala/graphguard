from dataclasses import dataclass


@dataclass(slots=True)
class Node:
    id: int
    label: str
    bbox: tuple[float, float, float, float]
    confidence: float