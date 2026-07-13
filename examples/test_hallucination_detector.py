from graphguard.verifier.evidence import Evidence
from graphguard.verifier.hallucination_detector import HallucinationDetector

detector = HallucinationDetector()

examples = [
    Evidence(matched=3, expected=3, score=1.0),
    Evidence(matched=2, expected=3, score=0.67),
    Evidence(matched=0, expected=3, score=0.0),
]

for evidence in examples:

    decision = detector.detect(evidence)

    print(decision)