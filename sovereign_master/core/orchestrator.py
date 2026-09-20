from .context import RequestContext
from .planner import Planner
from .task_router import TaskRouter
from sovereign_master.models.registry import ModelRegistry
from sovereign_master.memory.memory_engine import MemoryEngine
from sovereign_master.verification.verifier import VerificationEngine
from sovereign_master.spiritual.prophetic_mode import PropheticMode
class MasterOrchestrator:
    def __init__(self, models=None, memory=None):
        self.router=TaskRouter(); self.planner=Planner(); self.models=models or ModelRegistry(); self.memory=memory or MemoryEngine(); self.verifier=VerificationEngine()
    def handle(self, context: RequestContext):
        if not context.message.strip(): return self.result(False,"Message requis",[],["empty_input"])
        category=self.router.classify(context.message); plan=self.planner.create(category,context.mode); self.memory.add(context.session_id,"user",context.message)
        provider=self.models.get(); warnings=[]
        try: answer=provider.generate(context.message,{"category":category,"language":context.language,"mode":context.mode})
        except Exception as exc:
            answer="Aucun modèle génératif configuré ou le fournisseur configuré est indisponible."
            warnings.append(str(exc))
        if context.mode=="spiritual" or category=="spiritual": answer=PropheticMode().frame(answer)
        checked=self.verifier.verify(answer,category); warnings.extend(checked.warnings); self.memory.add(context.session_id,"assistant",answer)
        return self.result(True,answer,plan.modules,warnings,checked.confidence,checked.status)
    @staticmethod
    def result(success,answer,modules,warnings,confidence=0.0,status="UNCERTAIN"):
        return {"success":success,"answer":answer,"confidence":confidence,"verification_status":status,"verified":status=="VERIFIED","modules_used":modules,"warnings":warnings,"engine":"Sovereign Master AI"}
