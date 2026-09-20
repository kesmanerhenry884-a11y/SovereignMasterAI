import json
from sovereign_master.core.engine import SovereignMasterEngine
from sovereign_master.diagnostics.health import health
engine = SovereignMasterEngine()
def json_response(handler, payload, status=200):
    body = json.dumps(payload, ensure_ascii=False).encode(); handler.send_response(status); handler.send_header("Content-Type", "application/json; charset=utf-8"); handler.send_header("Content-Length", str(len(body))); handler.end_headers(); handler.wfile.write(body)
def status(): return {**health(), "capabilities": ["orchestration", "verification", "memory", "model-provider-abstraction", "spiritual-mode"]}
def chat(payload): return engine.process(payload.get("message", ""), payload.get("session_id"), payload.get("language", "auto"), payload.get("mode", "general"))
