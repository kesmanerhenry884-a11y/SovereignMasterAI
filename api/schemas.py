from typing import Any

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=50000, description="User message to process")
    session_id: str | None = None
    conversation_id: str | None = None
    language: str = "auto"
    mode: str = "general"
    metadata: dict[str, Any] = Field(default_factory=dict)


class ChatResponse(BaseModel):
    success: bool
    answer: str = ""
    response: str | None = None
    confidence: float = 0.0
    verification_status: str = "UNCERTAIN"
    verified: bool = False
    modules_used: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    engine: str = "Sovereign Master AI"
    mode: str = "general"
    classification: str | None = None
    conversation_id: str | None = None
