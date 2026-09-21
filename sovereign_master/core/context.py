from dataclasses import dataclass, field
from typing import Any


@dataclass
class RequestContext:
    message: str
    session_id: str | None = None
    language: str = "auto"
    mode: str = "general"
    conversation_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    task_type: str | None = None
    safety_status: str = "not_checked"
    retrieved_context: list[str] = field(default_factory=list)
    user_preferences: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.conversation_id is None and self.session_id is not None:
            self.conversation_id = self.session_id
        if self.session_id is None and self.conversation_id is not None:
            self.session_id = self.conversation_id

    def add_context(self, value: str) -> None:
        if value and value not in self.retrieved_context:
            self.retrieved_context.append(value)

    def to_dict(self) -> dict[str, Any]:
        return {
            "message": self.message,
            "session_id": self.session_id,
            "language": self.language,
            "mode": self.mode,
            "conversation_id": self.conversation_id,
            "metadata": self.metadata,
            "task_type": self.task_type,
            "safety_status": self.safety_status,
            "retrieved_context": self.retrieved_context,
            "user_preferences": self.user_preferences,
        }
