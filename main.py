import json, os
from http.server import BaseHTTPRequestHandler, HTTPServer
from api.routes import chat, json_response, status
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health": json_response(self, {"status":"ok", "engine":"Sovereign Master AI", "version":"0.1.0"})
        elif self.path == "/api/v1/status": json_response(self, status())
        elif self.path == "/api/v1/capabilities": json_response(self, status()["capabilities"])
        else: self.send_error(404, "Not found")
    def do_POST(self):
        if self.path != "/api/v1/chat": self.send_error(404, "Not found"); return
        try:
            length = int(self.headers.get("Content-Length", "0")); payload = json.loads(self.rfile.read(length) or b"{}")
            json_response(self, chat(payload))
        except (ValueError, json.JSONDecodeError): json_response(self, {"success":False,"error":"Invalid JSON"}, 400)
        except Exception: json_response(self, {"success":False,"error":"Internal server error"}, 500)
    def log_message(self, fmt, *args): print("%s - %s" % (self.address_string(), fmt % args))
def create_server(): return HTTPServer(("0.0.0.0", int(os.environ.get("PORT", "8080"))), Handler)
if __name__ == "__main__":
    server = create_server(); print(f"Sovereign Master AI running on port {server.server_port}")
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()
