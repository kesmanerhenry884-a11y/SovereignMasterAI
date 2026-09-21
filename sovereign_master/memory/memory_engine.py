import os


class MemoryEngine:
    def __init__(self, enabled=True, repository=None):
        self.enabled = enabled
        self.repository = repository
        self.sessions = {}
        self.context_limit = max(1, min(int(os.getenv("MEMORY_CONTEXT_LIMIT", "20")), 100))

    def add(self, session_id, role, content):
        if not self.enabled or not session_id or not content:
            return
        self.sessions.setdefault(session_id, []).append({"role": role, "content": content})
        self.sessions[session_id] = self.sessions[session_id][-self.context_limit :]
        if self.repository:
            self.repository.add_message(session_id, role, content)

    def get(self, session_id):
        if not self.enabled or not session_id:
            return []
        if self.repository:
            return self.repository.get_messages(session_id, self.context_limit)
        return self.sessions.get(session_id, [])[-self.context_limit :]

    def delete(self, session_id):
        self.sessions.pop(session_id, None)
