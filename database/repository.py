from .connection import DatabaseAdapter
class MemoryRepository:
    def __init__(self, adapter=None): self.adapter=adapter or DatabaseAdapter(); self.initialize()
    def initialize(self):
        if self.adapter.backend=="postgresql": return
        with self.adapter.connect() as c:
            c.execute("CREATE TABLE IF NOT EXISTS conversations (id INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT, role TEXT, content TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP)"); c.commit()
    def add_message(self,sid,role,content):
        with self.adapter.connect() as c: c.execute("INSERT INTO conversations(session_id,role,content) VALUES(?,?,?)",(sid,role,content)); c.commit()
    def get_messages(self,sid):
        with self.adapter.connect() as c: return [dict(r) for r in c.execute("SELECT role,content,created_at FROM conversations WHERE session_id=? ORDER BY id",(sid,)).fetchall()]
