from dataclasses import dataclass, field
from typing import Any

@dataclass
class SafetyDecision:
    allowed: bool
    action: str = "allow"
    reasons: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

class SafetyEngine:
    def check(self, request: dict[str, Any]) -> SafetyDecision:
        # Provider-specific moderation is intentionally not claimed here.
        return SafetyDecision(True, "allow", ["No moderation provider configured; policy review may be required for sensitive workflows."])
