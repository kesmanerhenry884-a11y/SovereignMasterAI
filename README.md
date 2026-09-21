# PROPHÈTE KESMANER HENRY
# SOVEREIGN MASTER AI ENGINE

Sovereign Master AI is a modular, multilingual AI orchestration platform foundation for reasoning, research, knowledge retrieval, memory, verification, creative workflows, safety, security, administration and extensible AI providers.

It is intentionally provider-independent. It does not claim perfect or universally superior answers, and it never presents an unconfigured provider as functional.

## Core pipeline

```text
INPUT → API → CONTEXT → TASK ROUTER → PLANNER → ORCHESTRATOR
      → MODEL / TOOLS / KNOWLEDGE / MEMORY → VERIFICATION → SAFETY → RESPONSE
```

The central entry point is `SovereignMasterEngine`. It classifies requests, plans modules, calls a configured provider when available, handles provider failure, records session context and returns evidence status.

## Evidence policy

Responses distinguish:

- `VERIFIED` — supported by an explicitly verified evidence source;
- `INFERENCE` — a reasoned conclusion, not a directly verified fact;
- `INTERPRETATION` — including spiritual interpretation;
- `UNCERTAIN` — insufficient evidence or unavailable provider.

The current foundation does not fabricate sources or external research. Prophetic Spirituality Mode keeps the identity **PROPHÈTE KESMANER HENRY**, while spiritual interpretations are not represented as objectively verified revelations.

## Architecture

- `sovereign_master/core` — context, routing, planning, orchestration and engine.
- `sovereign_master/models` and `providers/` — provider abstraction, registry, local fallback and OpenAI-compatible HTTP adapter.
- `sovereign_master/knowledge` — source-aware knowledge records and retrieval boundary.
- `sovereign_master/verification` — evidence status, confidence and warnings.
- `sovereign_master/memory` and `database/` — session memory and PostgreSQL-aware persistence boundary.
- `sovereign_master/research.py` — provider-independent research interface; no fake results.
- `sovereign_master/security` — authentication, permissions and rate-limiting building blocks.
- `sovereign_master/admin` — engine/module/maintenance/emergency state controls.
- `sovereign_master/media` — safe extension points for image/video workflows.
- `sovereign_master/jobs` — asynchronous job boundary for heavy media work.
- `sovereign_master/observability` — structured event boundary and health diagnostics.
- `api/` — versioned HTTP API.

Media providers are deliberately interfaces only until a real provider is configured and tested. The system must not claim that image, video, voice or identity workflows succeeded when they did not.

## Run locally

```bash
python -m pip install -r requirements.txt
python -m pytest
python main.py
```

The service listens on `0.0.0.0` and uses `PORT` from the environment, defaulting to `8080`. Railway keeps using:

```procfile
web: python main.py
```

## API

- `GET /health`
- `GET /api/v1/status`
- `GET /api/v1/capabilities`
- `POST /api/v1/chat`

Example request:

```json
{"message":"Bonjour","session_id":"demo","language":"auto","mode":"general"}
```

Without a real configured provider, the engine starts normally and returns an explicit fallback/uncertainty response. It does not fake AI generation.

## Environment

Copy `.env.example` to a deployment configuration. Never commit real values.

Important variables include `PORT`, `DATABASE_URL`, `MODEL_PROVIDER`, `MODEL_NAME`, `MODEL_API_KEY`, `MODEL_BASE_URL`, `VOICE_ENABLED`, `VOICE_PROVIDER`, `VOICE_PROFILE_ID` and `ADMIN_SECRET`.

PostgreSQL is the production database target. SQLite is only a local/testing fallback. The migration under `database/migrations/` is additive and must be reviewed, backed up and applied by an operator; the application does not reset or destroy an existing database.

## Honest implementation status

Functional foundation: orchestration, routing, planning, provider abstraction, safe fallback, verification status, local memory, API startup, health endpoint, security primitives and testable database boundary.

Still requiring external infrastructure and separate testing: live LLM credentials, production PostgreSQL wiring/migrations, durable auth sessions, web research connectors, pgVector/embeddings, real image/video/voice providers, background worker deployment and production admin routes.

## Version

Sovereign Master AI Engine v2 foundation.
