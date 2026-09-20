# PROPHÈTE KESMANER HENRY — SOVEREIGN MASTER AI ENGINE

This is a modular, provider-independent AI engine foundation. It is not a finished general intelligence and does not claim perfect or universally superior answers.

## Pipeline

`INPUT → CONTEXT → TASK ROUTER → PLANNER → MODEL/TOOLS → VERIFICATION → MEMORY → RESPONSE`

The core is `SovereignMasterEngine`. Providers implement `BaseModelProvider`; `ModelRegistry` discovers the configured provider. Without credentials, the engine starts safely and reports that no generative model is configured. It never fabricates external research or verification.

## Run

```bash
python -m unittest discover -s tests
python main.py
```

Railway uses `web: python main.py` and supplies `PORT`.

## API

- `GET /health`
- `GET /api/v1/status`
- `GET /api/v1/capabilities`
- `POST /api/v1/chat` with `message`, optional `session_id`, `language`, and `mode`

## Provider configuration

`MODEL_PROVIDER=openai_compatible`, `MODEL_NAME=...`, `MODEL_BASE_URL=...`, and `MODEL_API_KEY=...` enable the generic compatible adapter. These values belong in Railway secrets/environment settings, never GitHub. Other adapters can be registered without changing the orchestrator.

## Persistence

`database/` provides a PostgreSQL-aware adapter and a SQLite test fallback. `database/migrations/001_initial.sql` is additive and must be reviewed, backed up, and applied by an operator; this implementation does not connect to or alter production PostgreSQL automatically.

## Security and controls

Authentication, permissions, rate-limit building blocks, and `AdminControl` are present. A production deployment still needs HTTPS, durable token/session management, secret rotation, audit logging, and protected admin routes before exposing administration publicly.

## Evidence policy and spiritual mode

Responses carry `VERIFIED`, `INFERENCE`, `INTERPRETATION`, or `UNCERTAIN` status. Current model responses are `UNCERTAIN` unless an independent verification system is implemented. `PROPHÈTE KESMANER HENRY` is a public identity/style configuration; spiritual interpretations are not presented as objectively verified revelations.

## Not yet implemented

Real web research connectors, document/vector retrieval, voice providers, vision, durable PostgreSQL repository wiring, full admin API, and production authentication require external infrastructure and separate testing. No claim is made that these placeholders are functional.
