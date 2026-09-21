# Integration status

The repository now exposes one owner-controlled FastAPI surface and one public engine facade.

## Stable engine contract

- `SovereignMasterEngine.process(...)` remains the legacy dictionary-based entry point.
- `SovereignMasterEngine.chat(...)` is the modern orchestration entry point.
- `MasterOrchestrator.handle(...)` remains available for the existing API flow.
- `MasterOrchestrator.execute(...)` returns `OrchestrationResult` for modern callers.
- `TaskRouter.classify(...)` remains available alongside `TaskRouter.route(...)`.

## Capability states

The engine reports capability boundaries honestly:

- chat, planning, routing, memory, verification, jobs, provider abstraction and location consent are implemented foundations;
- media, voice, research and storage are extension points that require configured providers or infrastructure;
- GPS currently accepts consented client-supplied positions and provides distance/bearing preview;
- turn-by-turn navigation, camera capture, media generation, background workers and live RAG are not claimed as complete until configured and tested.

## Owner-controlled API

The API is served by this repository's FastAPI application. Optional external providers are adapters behind the engine, not the control plane. Location endpoints require explicit consent and support position deletion.

Run the verification suite with:

```bash
python -m pytest
```
