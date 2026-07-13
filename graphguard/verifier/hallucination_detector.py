from .decision import VerificationDecision
from .evidence import Evidence
from .status import VerificationStatus


class HallucinationDetector:

    def __init__(
        self,
        supported_threshold: float = 0.9,
        partial_threshold: float = 0.5,
    ):
        self.supported_threshold = supported_threshold
        self.partial_threshold = partial_threshold

    def detect(
        self,
        evidence: Evidence,
    ) -> VerificationDecision:

        if evidence.score >= self.supported_threshold:
            status = VerificationStatus.SUPPORTED

        elif evidence.score >= self.partial_threshold:
            status = VerificationStatus.PARTIALLY_SUPPORTED

        else:
            status = VerificationStatus.HALLUCINATED

        return VerificationDecision(
            status=status,
            evidence=evidence,
        )