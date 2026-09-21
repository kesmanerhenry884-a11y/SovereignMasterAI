from fastapi import FastAPI, HTTPException

from database import DatabaseAdapter, MemoryRepository
from sovereign_master.core.engine import SovereignMasterEngine
from sovereign_master.diagnostics.health import HealthService, health
from sovereign_master.jobs.queue import JOB_QUEUE
from sovereign_master.memory.memory_engine import MemoryEngine
from sovereign_master.models.registry import ModelRegistry
from sovereign_master.observability.logger import OBSERVABILITY_LOGGER

from .location_routes import router as location_router
from .schemas import ChatRequest, ChatResponse


def build_memory():
    import os
    database_url = os.getenv("DATABASE_URL", "").strip()
    if not database_url:
        return MemoryEngine()
    try:
        return MemoryEngine(repository=MemoryRepository(DatabaseAdapter(database_url)))
    except Exception as exc:
        print(f"Persistent memory unavailable; using temporary memory: {exc}")
        return MemoryEngine()


engine = SovereignMasterEngine(models=ModelRegistry(), memory=build_memory())
health_service = HealthService()
app = FastAPI(title="PROPHÈTE KESMANER HENRY — Sovereign Master AI", version="2.0.0", description="Modular AI orchestration engine for reasoning, knowledge, memory, research, media, location and multilingual workflows.")
app.include_router(location_router)


@app.get("/")
async def root():
    OBSERVABILITY_LOGGER.record("api.root", {"status": "ok"})
    return {**health_service.check(), "message": "Sovereign Master AI"}


@app.get("/health")
def health_endpoint():
    result = health_service.check()
    OBSERVABILITY_LOGGER.record("health.check", result)
    return result


@app.get("/api/v1/status")
def status_endpoint():
    return {**health(), **engine.status(), "jobs": JOB_QUEUE.list(), "location": {"enabled": True, "consent_required": True, "navigation_ready": False}}


@app.get("/api/v1/capabilities")
def capabilities_endpoint():
    return {**engine.capabilities(), "location": {"enabled": True, "consent_required": True, "navigation_ready": False}}


@app.get("/api/v1/jobs")
async def list_jobs():
    OBSERVABILITY_LOGGER.record("jobs.list", {"count": len(JOB_QUEUE.list())})
    return {"jobs": JOB_QUEUE.list()}


@app.get("/api/v1/observability")
async def observability_route():
    return {"events": OBSERVABILITY_LOGGER.recent(limit=20), "jobs": JOB_QUEUE.list()}


@app.post("/api/v1/jobs/queue")
async def enqueue_job(payload: dict):
    kind = payload.get("kind", "generic")
    job = JOB_QUEUE.enqueue(kind=kind, payload=payload.get("payload", {}))
    OBSERVABILITY_LOGGER.record("jobs.enqueued", {"job_id": job.id, "kind": job.kind})
    return {"success": True, "job": {"id": job.id, "kind": job.kind, "status": job.status}}


@app.post("/api/v1/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    conversation_id = request.conversation_id or request.session_id
    try:
        result = engine.process(message=request.message, session_id=conversation_id, language=request.language, mode=request.mode, metadata=request.metadata)
        result.update({"response": result.get("answer", ""), "mode": request.mode, "conversation_id": conversation_id})
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result)
        OBSERVABILITY_LOGGER.record("chat.success", {"conversation_id": conversation_id})
        return ChatResponse(**result)
    except HTTPException:
        raise
    except Exception as exc:
        OBSERVABILITY_LOGGER.record("chat.error", {"error": str(exc)})
        raise HTTPException(status_code=500, detail={"error": "ENGINE_ERROR", "message": str(exc)}) from exc
