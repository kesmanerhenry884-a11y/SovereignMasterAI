class MemoryEngine:
    def __init__(self, enabled=True, repository=None): self.enabled=enabled; self.repository=repository; self.sessions={}
    def add(self, session_id, role, content):
        if not self.enabled or not session_id: return
        self.sessions.setdefault(session_id,[]).append({"role":role,"content":content})
        if self.repository: self.repository.add_message(session_id,role,content)
    def get(self, session_id):
        if not self.enabled: return []
        if self.repository: return self.repository.get_messages(session_id)
        return self.sessions.get(session_id,[])
    def delete(self,session_id): self.sessions.pop(session_id,None)
