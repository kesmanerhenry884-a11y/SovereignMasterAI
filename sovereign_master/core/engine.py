from typing import Any

from .context import RequestContext
from .orchestrator import MasterOrchestrator


class SovereignMasterEngine:
    def __init__(self, **kwargs: Any):
        self.orchestrator = MasterOrchestrator(
            models=kwargs.get("models"),
            memory=kwargs.get("memory"),
        )

    def process(self, message, session_id=None, language="auto", mode="general", metadata=None):
        return self.orchestrator.handle(
            RequestContext(message, session_id, language, mode, metadata or {})
        )

    # Stable public aliases for API consumers, while process() remains backward compatible.
    def chat(self, message, language="auto", conversation_id=None, mode="general", metadata=None):
        result = self.process(message, conversation_id, language, mode, metadata)
        return EngineChatResult(result)

    def status(self) -> dict[str, Any]:
        return {
            "providers": self.orchestrator.models.health(),
            "capabilities": self.capabilities(),
            "memory": {
                "enabled": self.orchestrator.memory.enabled,
                "persistent": getattr(self.orchestrator.memory, "repository", None) is not None,
                "context_limit": getattr(self.orchestrator.memory, "context_limit", 20),
            },
        }

    def capabilities(self) -> dict[str, Any]:
        return self.orchestrator.models.metadata()


class EngineChatResult:
    def __init__(self, result: dict[str, Any]):
        self.response = result.get("answer", "")
        self.mode = result.get("mode", "general")
        self.confidence = result.get("confidence", 0.0)
        self.classification = result.get("classification")
        self.raw = result
