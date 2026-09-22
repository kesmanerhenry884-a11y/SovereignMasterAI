from fastapi import FastAPI, HTTPException
from database import DatabaseAdapter, MemoryRepository
from sovereign_master.core.engine import SovereignMasterEngine
from sovereign_master.diagnostics.health import HealthService, health
from sovereign_master.jobs.queue import JOB_QUEUE
from sovereign_master.jobs.reminders import ReminderService
from sovereign_master.memory.memory_engine import MemoryEngine
from sovereign_master.models.registry import ModelRegistry
from sovereign_master.observability.logger import OBSERVABILITY_LOGGER
from .location_routes import router as location_router
from .reminder_routes import router as reminder_router
from .schemas import ChatRequest, ChatResponse


def build_storage():
    dsn = __import__("os").getenv("DATABASE_URL", "").strip()
    if not dsn: return None
    try: return MemoryRepository(DatabaseAdapter(dsn))
    except Exception as exc:
        print(f"Persistent storage unavailable; using temporary memory: {exc}")
        return None

storage = build_storage()
memory = MemoryEngine(repository=storage)
engine = SovereignMasterEngine(models=ModelRegistry(), memory=memory)
# The default service remains safe in tests; production code can replace it with ReminderService(storage).
reminder_service = ReminderService(storage) if storage else None
health_service = HealthService()
app = FastAPI(title="PROPHÈTE KESMANER HENRY — Sovereign Master AI", version="2.0.0", description="Modular AI orchestration engine.")
app.include_router(location_router)
app.include_router(reminder_router)

@app.get("/")
async def root(): return {**health_service.check(), "message": "Sovereign Master AI"}

@app.get("/health")
def health_endpoint(): return health_service.check()

@app.get("/api/v1/status")
def status_endpoint(): return {**health(), **engine.status(), "jobs": JOB_QUEUE.list(), "location": {"enabled": True, "consent_required": True, "navigation_ready": False}, "reminders": {"enabled": True, "client_delivery_required": True}}

@app.get("/api/v1/capabilities")
def capabilities_endpoint(): return {**engine.capabilities(), "location": {"enabled": True, "consent_required": True, "navigation_ready": False}}

@app.get("/api/v1/jobs")
async def list_jobs(): return {"jobs": JOB_QUEUE.list()}

@app.get("/api/v1/observability")
async def observability_route(): return {"events": OBSERVABILITY_LOGGER.recent(limit=20), "jobs": JOB_QUEUE.list()}

@app.post("/api/v1/jobs/queue")
async def enqueue_job(payload: dict):
    job = JOB_QUEUE.enqueue(kind=payload.get("kind", "generic"), payload=payload.get("payload", {}))
    return {"success": True, "job": {"id": job.id, "kind": job.kind, "status": job.status}}

@app.post("/api/v1/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    conversation_id = request.conversation_id or request.session_id
    try:
        result = engine.process(message=request.message, session_id=conversation_id, language=request.language, mode=request.mode, metadata=request.metadata)
        result.update({"response": result.get("answer", ""), "mode": request.mode, "conversation_id": conversation_id})
        if not result.get("success"): raise HTTPException(status_code=400, detail=result)
        return ChatResponse(**result)
    except HTTPException: raise
    except Exception as exc: raise HTTPException(status_code=500, detail={"error": "ENGINE_ERROR", "message": str(exc)}) from exc
