from dataclasses import dataclass
@dataclass
class ChatRequest:
    message: str
    session_id: str | None = None
    language: str = "auto"
    mode: str = "general"
