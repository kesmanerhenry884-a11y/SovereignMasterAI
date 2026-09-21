from typing import Any

from .context import RequestContext
from .orchestrator import MasterOrchestrator, OrchestrationResult


class SovereignMasterEngine:
    """Public compatibility facade for the Sovereign Master AI runtime."""

    def __init__(self, **kwargs: Any):
        self.orchestrator = MasterOrchestrator(
            models=kwargs.get("models"),
            memory=kwargs.get("memory"),
            router=kwargs.get("router"),
            planner=kwargs.get("planner"),
            safety=kwargs.get("safety"),
            verification=kwargs.get("verification"),
        )

    def process(
        self,
        message: str,
        session_id: str | None = None,
        language: str | None = "auto",
        mode: str = "general",
        metadata: dict[str, Any] | None = None,
        conversation_id: str | None = None,
    ) -> dict[str, Any]:
        identifier = conversation_id or session_id
        context = RequestContext(
            message=message,
            session_id=identifier,
            language=language or "auto",
            mode=mode,
            metadata=metadata or {},
        )
        return self.orchestrator.handle(context)

    def chat(
        self,
        message: str,
        language: str | None = None,
        conversation_id: str | None = None,
        mode: str = "general",
        metadata: dict[str, Any] | None = None,
    ) -> OrchestrationResult:
        context = RequestContext(
            message=message,
            language=language or "auto",
            conversation_id=conversation_id,
            mode=mode,
            metadata=metadata or {},
        )
        return self.orchestrator.execute(context)

    def status(self) -> dict[str, Any]:
        memory = self.orchestrator.memory
        return {
            "name": "PROPHÈTE KESMANER HENRY — Sovereign Master AI",
            "version": "2.0.0",
            "status": "online",
            "architecture": "modular",
            "providers": self.orchestrator.models.health(),
            "memory": {
                "enabled": memory.enabled,
                "persistent": getattr(memory, "repository", None) is not None,
                "context_limit": getattr(memory, "context_limit", 20),
            },
        }

    def capabilities(self) -> dict[str, Any]:
        """Report implemented boundaries without claiming unconfigured integrations."""
        provider_metadata = self.orchestrator.models.metadata()
        return {
            "reasoning": True,
            "planning": True,
            "memory": self.orchestrator.memory.enabled,
            "knowledge": True,
            "rag": False,
            "pgvector": False,
            "research": True,
            "verification": True,
            "security": True,
            "multilingual": True,
            "image_pipeline": True,
            "video_pipeline": True,
            "voice_pipeline": True,
            "prophetic_mode": True,
            "background_jobs": True,
            "provider_abstraction": True,
            "location": {
                "enabled": True,
                "consent_required": True,
                "position_storage": True,
                "route_preview": True,
                "turn_by_turn_navigation": False,
            },
            "providers": provider_metadata,
        }
