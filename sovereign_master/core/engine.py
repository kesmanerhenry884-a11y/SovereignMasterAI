from typing import Any
from .context import RequestContext
from .orchestrator import MasterOrchestrator

class SovereignMasterEngine:
    def __init__(self, **kwargs: Any):
        self.orchestrator = MasterOrchestrator(**kwargs)
    def process(self, message: str, session_id: str | None = None, language: str = "auto", mode: str = "general") -> dict[str, Any]:
        return self.orchestrator.handle(RequestContext(message, session_id, language, mode))
