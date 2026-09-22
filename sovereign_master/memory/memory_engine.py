"""Session and user-scoped long-term memory."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
import os
from typing import Any


@dataclass
class MemoryRecord:
    key: str
    value: str
    memory_type: str = "fact"
    importance: int = 50
    tags: list[str] = field(default_factory=list)
    source: str = "user"
    created_at: str = ""
    updated_at: str = ""

    def __post_init__(self):
        now = datetime.now(timezone.utc).isoformat()
        self.created_at = self.created_at or now
        self.updated_at = self.updated_at or now
        self.importance = max(0, min(int(self.importance), 100))

    def to_dict(self):
        return {"key": self.key, "value": self.value, "memory_type": self.memory_type, "importance": self.importance, "tags": list(self.tags), "source": self.source, "created_at": self.created_at, "updated_at": self.updated_at}


class MemoryEngine:
    def __init__(self, enabled=True, repository=None):
        self.enabled = enabled
        self.repository = repository
        self.sessions = {}
        self.memories: dict[str, dict[str, MemoryRecord]] = {}
        self.context_limit = max(1, min(int(os.getenv("MEMORY_CONTEXT_LIMIT", "20")), 100))

    def add(self, session_id, role, content):
        if not self.enabled or not session_id or not content:
            return
        self.sessions.setdefault(session_id, []).append({"role": role, "content": content})
        self.sessions[session_id] = self.sessions[session_id][-self.context_limit:]
        if self.repository:
            self.repository.add_message(session_id, role, content)

    def get(self, session_id):
        if not self.enabled or not session_id:
            return []
        if self.repository:
            return self.repository.get_messages(session_id, self.context_limit)
        return self.sessions.get(session_id, [])[-self.context_limit:]

    def remember(self, user_id, key, value, *, memory_type="fact", importance=50, tags=None, source="user"):
        if not self.enabled:
            raise RuntimeError("memory is disabled")
        if not user_id.strip() or not key.strip() or not value.strip():
            raise ValueError("user_id, key, and value are required")
        record = MemoryRecord(key.strip(), value.strip(), memory_type, importance, list(tags or []), source)
        self.memories.setdefault(user_id, {})[record.key] = record
        if self.repository and hasattr(self.repository, "upsert_memory"):
            self.repository.upsert_memory(user_id, record.to_dict())
        return record.to_dict()

    def recall(self, user_id, key=None, *, limit=50):
        if not self.enabled or not user_id:
            return []
        if self.repository and hasattr(self.repository, "get_memories"):
            return self.repository.get_memories(user_id, key, limit)
        records = self.memories.get(user_id, {})
        selected = [records[key]] if key and key in records else list(records.values()) if not key else []
        selected.sort(key=lambda item: (item.importance, item.updated_at), reverse=True)
        return [item.to_dict() for item in selected[:max(1, min(int(limit), 100))]]

    def forget(self, user_id, key=None):
        removed = self.repository.delete_memories(user_id, key) if self.repository and hasattr(self.repository, "delete_memories") else 0
        records = self.memories.get(user_id, {})
        if key is None:
            removed = max(removed, len(records))
            self.memories.pop(user_id, None)
        elif records.pop(key, None) is not None:
            removed = max(removed, 1)
        return removed

    def delete(self, session_id):
        self.sessions.pop(session_id, None)
