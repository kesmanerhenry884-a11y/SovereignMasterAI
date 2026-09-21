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
        return SafetyDecision(True, "allow", ["No moderation provider configured; policy review may be required for sensitive workflows."], {"task_type": request.get("task_type")})


# Compatibility name for callers using the proposed service API.
SafetyService = SafetyEngine
