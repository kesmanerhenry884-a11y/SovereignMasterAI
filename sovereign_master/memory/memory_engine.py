class MemoryEngine:
    def __init__(self, enabled=True): self.enabled = enabled; self.sessions = {}
    def add(self, session_id, role, content):
        if self.enabled and session_id: self.sessions.setdefault(session_id, []).append({"role": role, "content": content})
    def get(self, session_id): return self.sessions.get(session_id, []) if self.enabled else []
    def delete(self, session_id): self.sessions.pop(session_id, None)
