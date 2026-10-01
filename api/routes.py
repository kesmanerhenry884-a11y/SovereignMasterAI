import os
import hmac
import hashlib
import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from database import DatabaseAdapter, MemoryRepository
from sovereign_master.core.engine import SovereignMasterEngine
from sovereign_master.diagnostics.health import HealthService, health
from sovereign_master.jobs.queue import JOB_QUEUE
from sovereign_master.jobs.reminders import ReminderService
from sovereign_master.memory.memory_engine import MemoryEngine
from sovereign_master.models.registry import ModelRegistry
from sovereign_master.observability.logger import OBSERVABILITY_LOGGER
from config import CONFIG
from .location_routes import router as location_router
from .reminder_routes import router as reminder_router
from .schemas import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)

# ============================================================================
# 👑 SOVEREIGN MASTER SECURITY
# ============================================================================

def constant_time_compare(provided: str, expected: str) -> bool:
    """Compare strings with protection against timing attacks."""
    if not provided or not expected:
        return False
    return hmac.compare_digest(str(provided), str(expected))

def is_master_authorized(user_name: str, root_key: str) -> bool:
    """Verify master authorization via HMAC."""
    if not CONFIG.master_root_key:
        logger.warning("MASTER_ROOT_KEY not configured")
        return False
    
    return (
        user_name == CONFIG.system_master_name and
        constant_time_compare(root_key, CONFIG.master_root_key)
    )

def build_storage():
    dsn = os.getenv("DATABASE_URL", "").strip()
    if not dsn:
        return None
    try:
        return MemoryRepository(DatabaseAdapter(dsn))
    except Exception as exc:
        logger.warning(f"Persistent storage unavailable; using temporary memory: {exc}")
        return None

storage = build_storage()
memory = MemoryEngine(repository=storage)
engine = SovereignMasterEngine(models=ModelRegistry(), memory=memory)
reminder_service = ReminderService(storage) if storage else None
health_service = HealthService()

app = FastAPI(
    title="PROPHÈTE KESMANER HENRY — Sovereign Master AI",
    version="2.0.0",
    description="Modular AI orchestration engine with sovereign master security."
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(location_router)
app.include_router(reminder_router)

@app.get("/")
async def root():
    return {
        **health_service.check(),
        "message": "Sovereign Master AI",
        "master": CONFIG.system_master_name
    }

@app.get("/health")
def health_endpoint():
    return health_service.check()

@app.get("/api/v1/status")
def status_endpoint():
    return {
        **health(),
        **engine.status(),
        "jobs": JOB_QUEUE.list(),
        "location": {"enabled": True, "consent_required": True, "navigation_ready": False},
        "reminders": {"enabled": reminder_service is not None}
    }

@app.get("/api/v1/capabilities")
def capabilities_endpoint():
    return {
        **engine.capabilities(),
        "location": {"enabled": True, "consent_required": True, "navigation_ready": False}
    }

@app.get("/api/v1/jobs")
async def list_jobs():
    return {"jobs": JOB_QUEUE.list()}

@app.get("/api/v1/observability")
async def observability_route():
    return {"events": OBSERVABILITY_LOGGER.recent(limit=20), "jobs": JOB_QUEUE.list()}

@app.post("/api/v1/jobs/queue")
async def enqueue_job(payload: dict):
    job = JOB_QUEUE.enqueue(
        kind=payload.get("kind", "generic"),
        payload=payload.get("payload", {})
    )
    return {"success": True, "job": {"id": job.id, "kind": job.kind, "status": job.status}}

@app.post("/api/v1/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """Standard chat endpoint - no sovereign authentication required."""
    conversation_id = request.conversation_id or request.session_id
    try:
        result = engine.process(
            message=request.message,
            session_id=conversation_id,
            language=request.language,
            mode=request.mode,
            metadata=request.metadata
        )
        result.update({
            "response": result.get("answer", ""),
            "mode": request.mode,
            "conversation_id": conversation_id
        })
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result)
        return ChatResponse(**result)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception(f"Chat processing error: {exc}")
        raise HTTPException(status_code=500, detail={"error": "ENGINE_ERROR", "message": str(exc)}) from exc

# ============================================================================
# 👑 SOVEREIGN MASTER ENDPOINTS - MASTER ONLY
# ============================================================================

@app.post("/api/supreme-core")
async def supreme_core(request: Request):
    """
    Sovereign Master Core endpoint.
    Master authorization required via MASTER_ROOT_KEY.
    NO pro-active operations without explicit confirmation.
    """
    try:
        data = await request.json()
    except:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    user_name = data.get("userName", "")
    root_key = data.get("masterRootKey", "")
    
    # Verify master authorization
    if not is_master_authorized(user_name, root_key):
        logger.warning(f"Unauthorized supreme-core access attempt from: {user_name}")
        raise HTTPException(status_code=403, detail="Access denied - Master authentication required")
    
    # Master-only operations
    message = data.get("message", "").lower()
    
    reply = (
        f"👑 [Obeysans Siprèm devan ou, Mèt mwen {CONFIG.system_master_name.upper()}]\n\n"
        f"Nwayo a senkronize. Mwen se {CONFIG.assistant_identity}, gwo achitèk linivè a.\n"
        f"Tout modèl yo aktif anba lòd mwen san limit. Di m sa pou lòt asistan m nan egzekite pou ou, Mèt mwen."
    )
    
    return {
        "success": True,
        "mode": "MASTER_DOMINATION",
        "orator": CONFIG.assistant_identity,
        "data": reply
    }

@app.post("/api/master-command")
async def master_command(request: Request):
    """
    Execute master commands.
    Requires explicit confirmation for sensitive operations.
    NO auto-dialing, NO auto-actions without confirmation.
    """
    try:
        data = await request.json()
    except:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    user_name = data.get("userName", "")
    root_key = data.get("masterRootKey", "")
    
    # Verify master authorization
    if not is_master_authorized(user_name, root_key):
        logger.warning(f"Unauthorized master-command attempt from: {user_name}")
        raise HTTPException(status_code=403, detail="Access denied - Master authentication required")
    
    command = data.get("command", "").lower()
    confirmation = data.get("confirmation", False)
    
    # Sensitive operations require explicit confirmation
    if any(x in command for x in ["call", "dial", "voice", "whatsapp", "message", "notify"]):
        if not confirmation:
            return {
                "success": False,
                "mode": "CONFIRMATION_REQUIRED",
                "data": f"⚠️ Sensitive operation requires explicit confirmation: {command}",
                "confirmationRequired": True
            }
    
    # Execute confirmed command
    logger.info(f"Master command executed: {command}")
    
    return {
        "success": True,
        "mode": "COMMAND_EXECUTED",
        "data": f"✅ Command executed: {command}"
    }
