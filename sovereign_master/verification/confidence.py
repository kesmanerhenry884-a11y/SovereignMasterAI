from dataclasses import dataclass
from enum import Enum
class EvidenceStatus(str,Enum): VERIFIED="VERIFIED"; INFERENCE="INFERENCE"; INTERPRETATION="INTERPRETATION"; UNCERTAIN="UNCERTAIN"
@dataclass
class VerificationResult:
    status: str
    confidence: float
    warnings: list[str]
