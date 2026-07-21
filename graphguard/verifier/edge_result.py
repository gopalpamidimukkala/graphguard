from dataclasses import dataclass

from graphguard.graph import Edge

from .decision import VerificationDecision
from .evidence import Evidence
from graphguard.graph.relation_type import RelationType


@dataclass(slots=True)
class EdgeVerificationResult:
    edge: Edge
    decision: VerificationDecision
    evidence: Evidence
    expected_relations: set[RelationType]
    observed_relations: set[RelationType]