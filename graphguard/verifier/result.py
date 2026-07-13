from dataclasses import field
from dataclasses import dataclass

from .edge_result import EdgeVerificationResult
from .decision import VerificationDecision
from graphguard.graph import SceneGraph

@dataclass(slots=True)
class VerificationResult:

    claim: str

    image_graph: SceneGraph

    text_graph: SceneGraph

    edge_results: list[EdgeVerificationResult] = field(default_factory=list)

    overall_decision: VerificationDecision | None = None