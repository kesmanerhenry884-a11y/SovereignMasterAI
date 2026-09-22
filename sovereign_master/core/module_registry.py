"""Canonical module status, including memory reminders and notification delivery."""
from dataclasses import asdict, dataclass

@dataclass(frozen=True)
class ModuleStatus:
    name: str
    state: str
    location: str
    description: str

MODULES = (
    ModuleStatus("core", "active", "sovereign_master/core", "Context, routing, planning and orchestration."),
    ModuleStatus("providers", "active_boundary", "sovereign_master/models and providers", "Legacy and normalized provider contracts."),
    ModuleStatus("memory", "active_boundary", "sovereign_master/memory and database", "Session, durable user memory and deletion controls."),
    ModuleStatus("secrets", "opt_in", "sovereign_master/security/secrets_vault.py", "Encrypted secret storage, never prompt memory."),
    ModuleStatus("reminders", "active_boundary", "sovereign_master/jobs/reminders.py and api/reminder_routes.py", "Scheduled branded events; client delivery required."),
    ModuleStatus("safety", "active", "sovereign_master/safety", "Safety decision boundary."),
    ModuleStatus("verification", "active_boundary", "sovereign_master/verification", "Evidence status and confidence."),
    ModuleStatus("security", "active_boundary", "sovereign_master/security", "Authentication, permissions and rate limits."),
    ModuleStatus("knowledge", "extension_point", "sovereign_master/knowledge", "Source-aware retrieval boundary."),
    ModuleStatus("research", "extension_point", "sovereign_master/research.py", "Verified external research boundary."),
    ModuleStatus("location", "preview", "sovereign_master/location and api/location_routes.py", "Consent-based position and route preview."),
    ModuleStatus("media", "extension_point", "sovereign_master/media", "Provider-backed image/video workflows."),
    ModuleStatus("voice", "extension_point", "sovereign_master/voice", "Provider-backed voice workflows."),
    ModuleStatus("jobs", "active_boundary", "sovereign_master/jobs", "Queue and scheduler boundaries."),
    ModuleStatus("admin", "active_boundary", "sovereign_master/admin", "Operational controls."),
    ModuleStatus("observability", "active", "sovereign_master/observability and diagnostics", "Health and events without secrets."),
    ModuleStatus("api", "active", "api", "Owner-controlled FastAPI surface."),
)

def module_inventory():
    return [asdict(module) for module in MODULES]

def module_states():
    return {module.name: module.state for module in MODULES}
