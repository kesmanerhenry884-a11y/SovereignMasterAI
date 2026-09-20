from dataclasses import dataclass, field
from typing import Any
@dataclass
class RequestContext:
    message: str
    session_id: str | None = None
    language: str = "auto"
    mode: str = "general"
    metadata: dict[str, Any] = field(default_factory=dict)
