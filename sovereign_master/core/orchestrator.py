from typing import Any
from .context import RequestContext
from .planner import Planner
from .task_router import TaskRouter
from sovereign_master.language.language_engine import LanguageEngine
from sovereign_master.memory.memory_engine import MemoryEngine
from sovereign_master.models.registry import ModelRegistry
from sovereign_master.verification.verifier import VerificationEngine
from sovereign_master.spiritual.prophetic_mode import PropheticMode

class MasterOrchestrator:
    def __init__(self, router=None, planner=None, memory=None, models=None):
        self.router = router or TaskRouter(); self.planner = planner or Planner()
        self.memory = memory or MemoryEngine(); self.models = models or ModelRegistry()
        self.language = LanguageEngine(); self.verifier = VerificationEngine()
    def handle(self, context: RequestContext) -> dict[str, Any]:
        if not context.message.strip():
            return self._result(False, "Le message ne peut pas être vide.", [], ["empty_input"])
        category = self.router.classify(context.message)
        plan = self.planner.create(category, context.mode)
        self.memory.add(context.session_id, "user", context.message)
        provider = self.models.default()
        warnings = []
        answer = None
        if provider:
            answer = provider.generate(context.message, {"category": category, "language": context.language, "mode": context.mode})
        if answer is None:
            warnings.append("Aucun modèle génératif n'est configuré; réponse locale limitée.")
            answer = self._local_response(context, category)
        if context.mode == "spiritual" or category == "spiritual": answer = PropheticMode().frame(answer)
        verification = self.verifier.verify(answer, category)
        result = self._result(True, answer, plan.modules, warnings + verification["warnings"], verification["confidence"], verification["verified"])
        self.memory.add(context.session_id, "assistant", answer)
        return result
    def _local_response(self, context, category):
        return (f"Je peux traiter cette demande dans la catégorie « {category} », mais aucun modèle génératif n'est configuré. "
                "Ajoutez explicitement un fournisseur compatible pour obtenir une réponse générée et vérifiée.")
    @staticmethod
    def _result(success, answer, modules, warnings, confidence=0.0, verified=False):
        return {"success": success, "answer": answer, "confidence": confidence, "verified": verified, "modules_used": modules, "warnings": warnings, "engine": "Sovereign Master AI"}
