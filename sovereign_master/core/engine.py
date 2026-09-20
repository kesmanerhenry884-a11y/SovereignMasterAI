from typing import Any
from .context import RequestContext
from .orchestrator import MasterOrchestrator
class SovereignMasterEngine:
    def __init__(self, **kwargs: Any): self.orchestrator=MasterOrchestrator(models=kwargs.get("models"),memory=kwargs.get("memory"))
    def process(self,message,session_id=None,language="auto",mode="general"): return self.orchestrator.handle(RequestContext(message,session_id,language,mode))
