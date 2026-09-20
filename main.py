import html
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", "8080"))


PROFILE = {
    "name": "Sovereign Master AI",
    "username": "@sovereignmasterai",
    "role": "AI Builder & Digital Creator",
    "bio": "Building useful, accessible and sovereign digital experiences with artificial intelligence.",
    "location": "Online",
    "status": "Available for collaboration",
}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.send_html(self.profile_page())
        elif self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"ok")
        else:
            self.send_error(404, "Page not found")

    def send_html(self, content):
        body = content.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def profile_page(self):
        p = {key: html.escape(value) for key, value in PROFILE.items()}
        return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{p['name']} profile">
  <title>{p['name']} · Profile</title>
  <style>
    :root {{ color-scheme: dark; --bg: #090d1a; --card: #111a2d; --text: #f6f8ff; --muted: #a9b6d3; --accent: #7c5cff; --accent2: #25d9b1; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; min-height: 100vh; font-family: Inter, ui-sans-serif, system-ui, sans-serif; color: var(--text); background: radial-gradient(circle at 15% 10%, #24336b 0, transparent 35%), var(--bg); display: grid; place-items: center; padding: 24px; }}
    .profile {{ width: min(100%, 720px); overflow: hidden; border: 1px solid #273557; border-radius: 28px; background: rgba(17, 26, 45, .92); box-shadow: 0 24px 80px #0008; }}
    .cover {{ height: 150px; background: linear-gradient(120deg, var(--accent), #36a7e8 55%, var(--accent2)); position: relative; }}
    .cover::after {{ content: ""; position: absolute; inset: 0; background: linear-gradient(135deg, transparent 45%, #fff3 45%, transparent 65%); }}
    .content {{ padding: 0 32px 32px; }}
    .avatar {{ width: 112px; height: 112px; margin-top: -56px; border: 6px solid var(--card); border-radius: 50%; display: grid; place-items: center; position: relative; background: #182444; color: white; font-size: 34px; font-weight: 800; letter-spacing: -2px; }}
    h1 {{ margin: 18px 0 4px; font-size: clamp(26px, 5vw, 40px); }}
    .username, .muted {{ color: var(--muted); }}
    .role {{ display: inline-block; margin: 18px 0 12px; padding: 7px 12px; border: 1px solid #3b4d78; border-radius: 999px; color: #d8d2ff; background: #7c5cff1c; font-size: 14px; }}
    .bio {{ max-width: 600px; color: #d7def0; line-height: 1.7; font-size: 17px; }}
    .details {{ display: flex; flex-wrap: wrap; gap: 16px 24px; margin: 24px 0; color: var(--muted); font-size: 14px; }}
    .status {{ color: var(--accent2); }}
    .actions {{ display: flex; flex-wrap: wrap; gap: 12px; margin-top: 26px; }}
    a {{ text-decoration: none; }}
    .button {{ display: inline-block; padding: 12px 18px; border-radius: 12px; font-weight: 700; background: var(--accent); color: white; }}
    .button.secondary {{ border: 1px solid #3b4d78; background: transparent; color: var(--text); }}
    footer {{ margin-top: 28px; padding-top: 18px; border-top: 1px solid #273557; color: var(--muted); font-size: 13px; }}
    @media (max-width: 480px) {{ .content {{ padding: 0 20px 24px; }} .cover {{ height: 120px; }} }}
  </style>
</head>
<body>
  <main class="profile" aria-labelledby="profile-name">
    <div class="cover" aria-hidden="true"></div>
    <section class="content">
      <div class="avatar" aria-label="Profile initials">SM</div>
      <h1 id="profile-name">{p['name']}</h1>
      <div class="username">{p['username']}</div>
      <div class="role">{p['role']}</div>
      <p class="bio">{p['bio']}</p>
      <div class="details">
        <span>📍 {p['location']}</span>
        <span class="status">● {p['status']}</span>
      </div>
      <div class="actions">
        <a class="button" href="mailto:contact@example.com">Contact me</a>
        <a class="button secondary" href="https://github.com/kesmanerhenry884-a11y/SovereignMasterAI">View project</a>
      </div>
      <footer>Powered by SovereignMasterAI · Accessible web profile</footer>
    </section>
  </main>
</body>
</html>"""


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), Handler)
    print(f"Web app running at http://127.0.0.1:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()
