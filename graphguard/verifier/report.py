from dataclasses import dataclass, field

from graphguard.graph import Edge


@dataclass(slots=True)
class VerificationReport:
    supported: list[Edge] = field(default_factory=list)
    partially_supported: list[Edge] = field(default_factory=list)
    hallucinated: list[Edge] = field(default_factory=list)