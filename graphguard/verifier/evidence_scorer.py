from graphguard.graph import RelationType

from .evidence import Evidence


class EvidenceScorer:

    def score(
        self,
        expected: set[RelationType],
        observed: set[RelationType],
    ) -> Evidence:

        matched = len(expected & observed)
        total = len(expected)

        if total == 0:
            value = 0.0
        else:
            value = matched / total

        return Evidence(
            matched=matched,
            expected=total,
            score=value,
        )