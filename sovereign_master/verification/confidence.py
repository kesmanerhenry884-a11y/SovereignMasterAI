from dataclasses import dataclass
from enum import Enum
class EvidenceType(str, Enum): FACT="FACT"; SOURCE="SOURCE"; INTERPRETATION="INTERPRETATION"; HYPOTHESIS="HYPOTHESIS"; UNKNOWN="UNKNOWN"
@dataclass
class Confidence:
    value: float; evidence: EvidenceType; reason: str = ""
