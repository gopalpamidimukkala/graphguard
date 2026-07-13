from dataclasses import dataclass


@dataclass(slots=True)
class Evidence:
    matched: int
    expected: int
    score: float