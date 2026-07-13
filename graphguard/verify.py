from pathlib import Path

from graphguard.services.verifier_service import VerifierService


class GraphGuard:

    def __init__(
        self,
        service: VerifierService,
    ):
        self.service = service

    def verify(
        self,
        image: Path,
        claim: str,
        classes: list[str],
    ):
        return self.service.verify(
            image,
            claim,
            classes,
        )