from dataclasses import dataclass


@dataclass(slots=True)
class Detection:
    """
    Represents one detected object.
    """

    label: str

    confidence: float

    bbox: tuple[float, float, float, float]

    detector: str = "groundingdino"