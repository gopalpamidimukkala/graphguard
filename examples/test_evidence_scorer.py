from graphguard.graph import RelationType
from graphguard.verifier.evidence_scorer import EvidenceScorer

expected = {
    RelationType.ABOVE,
    RelationType.NEAR,
    RelationType.OVERLAPS,
}

observed = {
    RelationType.ABOVE,
    RelationType.LEFT_OF,
    RelationType.NEAR,
    RelationType.OVERLAPS,
}

scorer = EvidenceScorer()

evidence = scorer.score(
    expected,
    observed,
)

print(evidence)