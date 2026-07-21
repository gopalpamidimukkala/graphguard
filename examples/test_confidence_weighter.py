from graphguard.verifier.confidence_weighter import (
    ConfidenceWeighter,
)
from graphguard.verifier.evidence import Evidence


weighter = ConfidenceWeighter()

evidence = Evidence(
    matched=1,
    expected=1,
    score=1.0,
)

weighted = weighter.weight(
    evidence=evidence,
    source_confidence=0.90,
    target_confidence=0.80,
)

print(weighted)