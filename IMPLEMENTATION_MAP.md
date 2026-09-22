# Sovereign Master AI — final integration map

This file is the canonical placement map for the engine. New code must be merged into the listed module instead of creating a parallel implementation.

| Area | Location | State | Rule |
|---|---|---|---|
| Core context, routing, planning, orchestration | `sovereign_master/core/` | active | One engine control flow; preserve `process()` and `chat()`. |
| Providers | `sovereign_master/models/`, `providers/` | active boundary | Keep legacy string providers and normalized `GenerationResult` providers compatible. |
| Session/long-term memory | `sovereign_master/memory/`, `database/` | active boundary | User-scoped, recallable and deletable; persistence depends on configured storage. |
| Secrets | `sovereign_master/security/secrets_vault.py` | opt-in | Encrypted only; never put secrets in chat memory, prompts or logs. |
| Safety and verification | `sovereign_master/safety/`, `sovereign_master/verification/` | active boundary | Run before/after generation; never claim unsupported evidence. |
| Auth, permissions, rate limits | `sovereign_master/security/` | active boundary | Protect privileged operations; deployment still needs real credentials and policy. |
| Knowledge/RAG | `sovereign_master/knowledge/` | extension point | Add source connectors and embeddings here; do not claim live RAG until configured. |
| Research | `sovereign_master/research.py` | extension point | Add verified external connectors here; never fabricate current sources. |
| Location/navigation | `sovereign_master/location/`, `api/location_routes.py` | preview | Consent-first position storage and straight-line preview; maps provider required for navigation. |
| Image/video | `sovereign_master/media/` | extension point | Add provider adapters and moderation; no fake successful output. |
| Voice | `sovereign_master/voice/` | extension point | Add provider adapter and permission flow; keep disabled without configuration. |
| Background jobs | `sovereign_master/jobs/` | active boundary | Queue exists; production workers require deployment infrastructure. |
| Admin controls | `sovereign_master/admin/` | active boundary | Keep operational controls behind authentication. |
| Observability/health | `sovereign_master/observability/`, `diagnostics/` | active | Log status and failures without recording secrets. |
| HTTP API | `api/` | active | The repository API remains the owner-controlled surface. |

## Completion rule

A module is only promoted from `extension_point`, `preview` or `opt_in` after its provider, permissions, persistence, tests and deployment configuration are present. This prevents forgetting planned work while preventing false capability claims.

The machine-readable inventory is available from `sovereign_master.core.module_registry.module_inventory()` and `module_states()`.
