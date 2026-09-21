from fastapi import FastAPI

from database import DatabaseAdapter, MemoryRepository
from sovereign_master.core.engine import SovereignMasterEngine
from sovereign_master.models.registry import ModelRegistry
from sovereign_master.memory.memory_engine import MemoryEngine
from sovereign_master.diagnostics.health import health
from sovereign_master.jobs.queue import JOB_QUEUE
from sovereign_master.observability.logger import OBSERVABILITY_LOGGER

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

app = FastAPI(
    title="Sovereign Master AI",
    version="2.0.0",
    description="Modular orchestration platform for reasoning, knowledge, memory, safety and verification.",
)


@app.get("/")
async def root():
    OBSERVABILITY_LOGGER.record("api.root", {"status": "ok"})
    return {
        "message": "Sovereign Master AI",
        "status": "ok",
        "engine": "Sovereign Master AI",
        "version": "2.0.0",
    }


@app.get("/health")
async def health_route():
    OBSERVABILITY_LOGGER.record("health.check", {"status": "ok"})
    return {"status": "ok", "engine": "Sovereign Master AI", "version": "2.0.0"}


@app.get("/api/v1/status")
async def status_route():
    return {
        **health(),
        "providers": engine.orchestrator.models.health(),
        "capabilities": engine.orchestrator.models.metadata(),
        "memory": {
            "enabled": engine.orchestrator.memory.enabled,
            "persistent": getattr(engine.orchestrator.memory, "repository", None) is not None,
            "context_limit": getattr(engine.orchestrator.memory, "context_limit", 20),
        },
        "jobs": JOB_QUEUE.list(),
    }


@app.get("/api/v1/capabilities")
async def capabilities_route():
    return engine.orchestrator.models.metadata()


@app.get("/api/v1/jobs")
async def list_jobs():
    OBSERVABILITY_LOGGER.record("jobs.list", {"count": len(JOB_QUEUE.list())})
    return {"jobs": JOB_QUEUE.list()}


@app.get("/api/v1/observability")
async def observability_route():
    return {
        "events": OBSERVABILITY_LOGGER.recent(limit=20),
        "jobs": JOB_QUEUE.list(),
    }


@app.post("/api/v1/jobs/queue")
async def enqueue_job(payload: dict):
    kind = payload.get("kind", "generic")
    job = JOB_QUEUE.enqueue(kind=kind, payload=payload.get("payload", {}))
    OBSERVABILITY_LOGGER.record("jobs.enqueued", {"job_id": job.id, "kind": job.kind})
    return {"success": True, "job": {"id": job.id, "kind": job.kind, "status": job.status}}


@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat_route(payload: ChatRequest):
    OBSERVABILITY_LOGGER.record("chat.request", {"session_id": payload.session_id, "mode": payload.mode})
    result = engine.process(
        payload.message,
        payload.session_id,
        payload.language,
        payload.mode,
    )
    if not result.get("success"):
        OBSERVABILITY_LOGGER.record("chat.failed", {"session_id": payload.session_id, "warnings": result.get("warnings", [])})
        return {**result, "answer": result.get("answer", "")}

    OBSERVABILITY_LOGGER.record("chat.success", {"session_id": payload.session_id, "verification_status": result.get("verification_status")})
    return ChatResponse(**result)
