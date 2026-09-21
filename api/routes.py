import json
import os
from database import DatabaseAdapter, MemoryRepository
from sovereign_master.core.engine import SovereignMasterEngine
from sovereign_master.models.registry import ModelRegistry
from sovereign_master.memory.memory_engine import MemoryEngine
from sovereign_master.diagnostics.health import health


def build_memory():
    database_url = os.getenv("DATABASE_URL", "").strip()
    if not database_url:
        return MemoryEngine()
    try:
        return MemoryEngine(repository=MemoryRepository(DatabaseAdapter(database_url)))
    except Exception as exc:
        print(f"Persistent memory unavailable; using temporary memory: {exc}")
        return MemoryEngine()


engine = SovereignMasterEngine(models=ModelRegistry(), memory=build_memory())


def json_response(handler, payload, status=200):
    body = json.dumps(payload, ensure_ascii=False, default=str).encode()
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def status():
    return {
        **health(),
        "providers": engine.orchestrator.models.health(),
        "capabilities": engine.orchestrator.models.metadata(),
        "memory": {
            "enabled": engine.orchestrator.memory.enabled,
            "persistent": engine.orchestrator.memory.repository is not None,
            "context_limit": engine.orchestrator.memory.context_limit,
        },
    }


def chat(payload):
    return engine.process(
        payload.get("message", ""),
        payload.get("session_id"),
        payload.get("language", "auto"),
        payload.get("mode", "general"),
    )
