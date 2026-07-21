from graphguard.verifier.result import VerificationResult


class GraphConsistencyValidator:

    def validate(
        self,
        results: list[VerificationResult],
    ) -> str:

        if not results:
            return "unsupported"

        supported = sum(
            result.status == "supported"
            for result in results
        )

        if supported == len(results):
            return "supported"

        if supported == 0:
            return "unsupported"

        return "partially_supported"