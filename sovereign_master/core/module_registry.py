"""Canonical module inventory used to keep the engine extensible without overclaiming."""
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ModuleStatus:
    name: str
    state: str
    location: str
    description: str


MODULES = (
    ModuleStatus("core", "active", "sovereign_master/core", "Context, routing, planning and orchestration."),
    ModuleStatus("providers", "active_boundary", "sovereign_master/models and providers", "Legacy and GenerationResult provider contracts."),
    ModuleStatus("memory", "active_boundary", "sovereign_master/memory and database", "Session memory with optional persistence and long-term APIs."),
    ModuleStatus("secrets", "opt_in", "sovereign_master/security/secrets_vault.py", "Encrypted secret storage; never part of conversation memory."),
    ModuleStatus("safety", "active", "sovereign_master/safety", "Safety decision boundary before provider execution."),
    ModuleStatus("verification", "active_boundary", "sovereign_master/verification", "Evidence status and confidence warnings."),
    ModuleStatus("security", "active_boundary", "sovereign_master/security", "Authentication, permissions and rate limiting primitives."),
    ModuleStatus("knowledge", "extension_point", "sovereign_master/knowledge", "Source-aware knowledge and retrieval boundary."),
    ModuleStatus("research", "extension_point", "sovereign_master/research.py", "Research interface; no fabricated live results."),
    ModuleStatus("location", "preview", "sovereign_master/location and api/location_routes.py", "Consent-based position storage and straight-line route preview."),
    ModuleStatus("media", "extension_point", "sovereign_master/media", "Image/video workflow interfaces; provider required."),
    ModuleStatus("voice", "extension_point", "sovereign_master/voice", "Voice workflow boundary; provider and permissions required."),
    ModuleStatus("jobs", "active_boundary", "sovereign_master/jobs", "Queue boundary; worker execution requires deployment infrastructure."),
    ModuleStatus("admin", "active_boundary", "sovereign_master/admin", "Engine and maintenance controls."),
    ModuleStatus("observability", "active", "sovereign_master/observability and diagnostics", "Events, health and operational visibility."),
    ModuleStatus("api", "active", "api", "Owner-controlled FastAPI surface."),
)


def module_inventory() -> list[dict[str, str]]:
    return [asdict(module) for module in MODULES]


def module_states() -> dict[str, str]:
    return {module.name: module.state for module in MODULES}
