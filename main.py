import json,os
from http.server import BaseHTTPRequestHandler,HTTPServer
from api.routes import chat,json_response,status
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path=self.path.split("?",1)[0]
        if path=="/health": json_response(self,{"status":"ok","engine":"Sovereign Master AI","version":"0.1.0"})
        elif path=="/api/v1/status": json_response(self,status())
        elif path=="/api/v1/capabilities": json_response(self,status()["capabilities"])
        else: self.send_error(404,"Not found")
    def do_POST(self):
        if self.path!="/api/v1/chat": self.send_error(404,"Not found"); return
        try:
            data=json.loads(self.rfile.read(int(self.headers.get("Content-Length",0))) or b"{}"); result=chat(data); json_response(self,result,200 if result.get("success") else 400)
        except (ValueError,json.JSONDecodeError): json_response(self,{"success":False,"error":"Invalid JSON"},400)
        except Exception: json_response(self,{"success":False,"error":"Internal server error"},500)
    def log_message(self,fmt,*args): print(fmt%args)
def create_server(): return HTTPServer(("0.0.0.0",int(os.getenv("PORT","8080"))),Handler)
if __name__=="__main__":
    server=create_server(); print(f"Sovereign Master AI listening on {server.server_port}")
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()
