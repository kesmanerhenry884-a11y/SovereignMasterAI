from dataclasses import dataclass
from typing import Any

from .context import RequestContext
from .planner import Planner
from .task_router import TaskRoute, TaskRouter
from sovereign_master.memory.memory_engine import MemoryEngine
from sovereign_master.models.registry import ModelRegistry
from sovereign_master.safety import SafetyEngine
from sovereign_master.spiritual.prophetic_mode import PropheticMode
from sovereign_master.verification.verifier import VerificationEngine


@dataclass
class OrchestrationResult:
    response: str
    mode: str
    confidence: float
    classification: str
    success: bool = True
    route: str | None = None
    modules: list[str] | None = None


class MasterOrchestrator:
    def __init__(self, models=None, memory=None, router=None, planner=None, safety=None, verification=None):
        self.router = router or TaskRouter()
        self.planner = planner or Planner()
        self.models = models or ModelRegistry()
        self.memory = memory or MemoryEngine()
        self.safety = safety or SafetyEngine()
        self.verifier = verification or VerificationEngine()
        self.verification = self.verifier

    def handle(self, context: RequestContext) -> dict[str, Any]:
        if not context.message or not context.message.strip():
            return self.result(False, "Message requis", [], ["empty_input"])

        route = self.router.route(context.message)
        category = route.name
        context.task_type = category
        plan = self.planner.create(category, context.mode)
        previous_messages = self.memory.get(context.session_id)
        self.memory.add(context.session_id, "user", context.message)
        warnings: list[str] = []

        safety = self.safety.check({
            "message": context.message,
            "task_type": category,
            "metadata": context.metadata,
        })
        context.safety_status = "allowed" if safety.allowed else "blocked"
        warnings.extend(safety.reasons)
        if not safety.allowed:
            return self.result(
                False,
                safety.reasons[0] if safety.reasons else "Request refused by safety policy.",
                plan.modules,
                warnings,
                1.0,
                "REFUSED",
                route=route,
            )

        provider = self.models.get()
        if provider is None:
            answer = "Aucun modèle génératif configuré ou le fournisseur configuré est indisponible."
            warnings.append("no_provider")
        else:
            provider_context = {
                "category": category,
                "language": context.language,
                "mode": context.mode,
                "conversation": previous_messages,
                "request": context.to_dict(),
                "route": route.__dict__,
                "plan": plan.steps,
            }
            try:
                answer = provider.generate(context.message, provider_context)
            except Exception as exc:
                answer = "Aucun modèle génératif configuré ou le fournisseur configuré est indisponible."
                warnings.append(str(exc))

        if context.mode == "spiritual" or category == "spiritual":
            answer = PropheticMode().frame(answer)
        checked = self.verifier.verify(answer, category)
        warnings.extend(checked.warnings)
        self.memory.add(context.session_id, "assistant", answer)
        return self.result(True, answer, plan.modules, warnings, checked.confidence, checked.status, route=route)

    def route(self, message: str) -> TaskRoute:
        return self.router.route(message)

    def execute(self, context: RequestContext) -> OrchestrationResult:
        result = self.handle(context)
        return OrchestrationResult(
            response=result["answer"],
            mode=context.mode,
            confidence=result["confidence"],
            classification=result.get("verification_status", "UNCERTAIN"),
            success=result["success"],
            route=result.get("route"),
            modules=result.get("modules_used", []),
        )

    @staticmethod
    def result(success, answer, modules, warnings, confidence=0.0, status="UNCERTAIN", route=None):
        return {
            "success": success,
            "answer": answer,
            "confidence": confidence,
            "verification_status": status,
            "verified": status == "VERIFIED",
            "modules_used": modules,
            "warnings": warnings,
            "engine": "Sovereign Master AI",
            "route": route.name if route else None,
        }
