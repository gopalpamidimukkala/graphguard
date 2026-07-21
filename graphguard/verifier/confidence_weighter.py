from .evidence import Evidence


class ConfidenceWeighter:

    def weight(
        self,
        evidence: Evidence,
        source_confidence: float,
        target_confidence: float,
    ) -> Evidence:

        average_confidence = (
            source_confidence + target_confidence
        ) / 2.0

        return Evidence(
            matched=evidence.matched,
            expected=evidence.expected,
            score=evidence.score * average_confidence,
        )