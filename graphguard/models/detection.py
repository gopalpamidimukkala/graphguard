from dataclasses import dataclass


@dataclass(slots=True)
class Detection:
    label: str
    confidence: float
    bbox: tuple[float, float, float, float]