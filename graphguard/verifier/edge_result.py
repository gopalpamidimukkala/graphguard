from dataclasses import dataclass

from graphguard.graph import Edge

from .decision import VerificationDecision


@dataclass(slots=True)
class EdgeVerificationResult:
    edge: Edge
    decision: VerificationDecision