from dataclasses import dataclass

from .evidence import Evidence
from .status import VerificationStatus


@dataclass(slots=True)
class VerificationDecision:
    status: VerificationStatus
    evidence: Evidence