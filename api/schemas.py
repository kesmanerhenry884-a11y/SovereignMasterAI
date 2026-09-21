from typing import Any

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User message to process")
    session_id: str | None = Field(default=None, description="Optional session identifier")
    conversation_id: str | None = Field(default=None, description="Compatibility alias for session_id")
    language: str = Field(default="auto", description="Preferred language for the response")
    mode: str = Field(default="general", description="Execution mode")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Optional structured metadata")


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
