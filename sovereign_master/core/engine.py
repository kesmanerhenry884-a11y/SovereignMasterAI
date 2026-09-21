from typing import Any

from .context import RequestContext
from .orchestrator import MasterOrchestrator


class SovereignMasterEngine:
    def __init__(self, **kwargs: Any):
        self.orchestrator = MasterOrchestrator(models=kwargs.get("models"), memory=kwargs.get("memory"))

    def process(self, message, session_id=None, language="auto", mode="general", metadata=None, conversation_id=None):
        identifier = conversation_id or session_id
        context = RequestContext(message=message, session_id=identifier, language=language or "auto", mode=mode, metadata=metadata or {})
        return self.orchestrator.handle(context)

    def chat(self, message, language="auto", conversation_id=None, mode="general", metadata=None):
        result = self.process(message, language=language, mode=mode, metadata=metadata, conversation_id=conversation_id)
        return EngineChatResult(result)

    def status(self) -> dict[str, Any]:
        return {"providers": self.orchestrator.models.health(), "capabilities": self.capabilities(), "memory": {"enabled": self.orchestrator.memory.enabled, "persistent": getattr(self.orchestrator.memory, "repository", None) is not None, "context_limit": getattr(self.orchestrator.memory, "context_limit", 20)}}

    def capabilities(self) -> dict[str, Any]:
        return self.orchestrator.models.metadata()


class EngineChatResult:
    def __init__(self, result: dict[str, Any]):
        self.response = result.get("answer", "")
        self.mode = result.get("mode", "general")
        self.confidence = result.get("confidence", 0.0)
        self.classification = result.get("classification", result.get("verification_status"))
        self.raw = result
