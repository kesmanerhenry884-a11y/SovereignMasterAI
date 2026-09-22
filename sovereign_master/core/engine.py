"""Public engine facade."""
from typing import Any
from sovereign_master.core.context import RequestContext
from sovereign_master.core.orchestrator import MasterOrchestrator, OrchestrationResult
from sovereign_master.core.module_registry import module_inventory

class SovereignMasterEngine:
    def __init__(self, **kwargs: Any):
        self.orchestrator = MasterOrchestrator(models=kwargs.get("models"), memory=kwargs.get("memory"), router=kwargs.get("router"), planner=kwargs.get("planner"), safety=kwargs.get("safety"), verification=kwargs.get("verification"))

    def process(self, message, session_id=None, language="auto", mode="general", metadata=None, conversation_id=None):
        context = RequestContext(message=message, session_id=conversation_id or session_id, language=language or "auto", mode=mode, metadata=metadata or {})
        return self.orchestrator.handle(context)

    def chat(self, message, language=None, conversation_id=None, mode="general", metadata=None) -> OrchestrationResult:
        return self.orchestrator.execute(RequestContext(message=message, language=language or "auto", conversation_id=conversation_id, mode=mode, metadata=metadata or {}))

    def status(self):
        memory = self.orchestrator.memory
        return {"name": "PROPHÈTE KESMANER HENRY — Sovereign Master AI", "version": "2.0.0", "status": "online", "architecture": "modular", "providers": self.orchestrator.models.health(), "memory": {"enabled": memory.enabled, "persistent": getattr(memory, "repository", None) is not None, "context_limit": getattr(memory, "context_limit", 20)}, "reminders": {"enabled": True, "client_delivery_required": True}}

    def capabilities(self):
        return {"reasoning": True, "planning": True, "memory": self.orchestrator.memory.enabled, "knowledge": True, "rag": False, "pgvector": False, "research": True, "verification": True, "security": True, "multilingual": True, "image_pipeline": True, "video_pipeline": True, "voice_pipeline": True, "prophetic_mode": True, "background_jobs": True, "provider_abstraction": True, "reminders": {"enabled": True, "sound_brand": "PROPHÈTE KESMANER HENRY", "client_delivery_required": True}, "module_inventory": module_inventory()}
