import json
import os
from .connection import DatabaseAdapter


class MemoryRepository:
    """Durable repository for conversations, memories, reminders and ciphertext."""

    def __init__(self, adapter=None):
        self.adapter = adapter or DatabaseAdapter()
        self.initialize()

    def initialize(self):
        if self.adapter.backend == "postgresql":
            statements = [
                "CREATE TABLE IF NOT EXISTS conversations (id BIGSERIAL PRIMARY KEY, session_id TEXT NOT NULL, role TEXT NOT NULL, content TEXT NOT NULL, created_at TIMESTAMPTZ DEFAULT NOW())",
                "CREATE INDEX IF NOT EXISTS conversations_session_idx ON conversations(session_id, id)",
                "CREATE TABLE IF NOT EXISTS long_term_memories (user_id TEXT NOT NULL, memory_key TEXT NOT NULL, value TEXT NOT NULL, memory_type TEXT NOT NULL, importance INTEGER NOT NULL, tags TEXT NOT NULL, source TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL, PRIMARY KEY (user_id, memory_key))",
                "CREATE TABLE IF NOT EXISTS reminders (id TEXT PRIMARY KEY, user_id TEXT NOT NULL, message TEXT NOT NULL, due_at TEXT NOT NULL, status TEXT NOT NULL, notify BOOLEAN NOT NULL, sound BOOLEAN NOT NULL, created_at TEXT NOT NULL, delivered_at TEXT)",
                "CREATE TABLE IF NOT EXISTS encrypted_secrets (user_id TEXT NOT NULL, secret_name TEXT NOT NULL, ciphertext BYTEA NOT NULL, PRIMARY KEY (user_id, secret_name))",
            ]
            with self.adapter.connect() as connection:
                with connection.cursor() as cursor:
                    for statement in statements:
                        cursor.execute(statement)
                connection.commit()
            return

        statements = [
            "CREATE TABLE IF NOT EXISTS conversations (id INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT NOT NULL, role TEXT NOT NULL, content TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP)",
            "CREATE INDEX IF NOT EXISTS conversations_session_idx ON conversations(session_id, id)",
            "CREATE TABLE IF NOT EXISTS long_term_memories (user_id TEXT NOT NULL, memory_key TEXT NOT NULL, value TEXT NOT NULL, memory_type TEXT NOT NULL, importance INTEGER NOT NULL, tags TEXT NOT NULL, source TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL, PRIMARY KEY (user_id, memory_key))",
            "CREATE TABLE IF NOT EXISTS reminders (id TEXT PRIMARY KEY, user_id TEXT NOT NULL, message TEXT NOT NULL, due_at TEXT NOT NULL, status TEXT NOT NULL, notify INTEGER NOT NULL, sound INTEGER NOT NULL, created_at TEXT NOT NULL, delivered_at TEXT)",
            "CREATE TABLE IF NOT EXISTS encrypted_secrets (user_id TEXT NOT NULL, secret_name TEXT NOT NULL, ciphertext BLOB NOT NULL, PRIMARY KEY (user_id, secret_name))",
        ]
        with self.adapter.connect() as connection:
            for statement in statements:
                connection.execute(statement)
            connection.commit()

    def add_message(self, sid, role, content):
        if not sid or not content:
            return
        with self.adapter.connect() as connection:
            if self.adapter.backend == "postgresql":
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO conversations(session_id, role, content) VALUES (%s, %s, %s)", (sid, role, content))
            else:
                connection.execute("INSERT INTO conversations(session_id, role, content) VALUES (?, ?, ?)", (sid, role, content))
            connection.commit()

    def get_messages(self, sid, limit=None):
        limit = max(1, min(int(limit or os.getenv("MEMORY_CONTEXT_LIMIT", "20")), 100))
        with self.adapter.connect() as connection:
            if self.adapter.backend == "postgresql":
                with connection.cursor() as cursor:
                    cursor.execute("SELECT role, content, created_at FROM conversations WHERE session_id=%s ORDER BY id DESC LIMIT %s", (sid, limit))
                    rows = cursor.fetchall()
                return [{"role": row[0], "content": row[1], "created_at": row[2].isoformat() if row[2] else None} for row in reversed(rows)]
            rows = connection.execute("SELECT role, content, created_at FROM conversations WHERE session_id=? ORDER BY id DESC LIMIT ?", (sid, limit)).fetchall()
        return [dict(row) for row in reversed(rows)]

    def upsert_memory(self, user_id, record):
        values = (user_id, record["key"], record["value"], record["memory_type"], record["importance"], json.dumps(record.get("tags", [])), record["source"], record["created_at"], record["updated_at"])
        with self.adapter.connect() as connection:
            if self.adapter.backend == "postgresql":
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO long_term_memories(user_id,memory_key,value,memory_type,importance,tags,source,created_at,updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT(user_id,memory_key) DO UPDATE SET value=EXCLUDED.value,memory_type=EXCLUDED.memory_type,importance=EXCLUDED.importance,tags=EXCLUDED.tags,source=EXCLUDED.source,updated_at=EXCLUDED.updated_at", values)
            else:
                connection.execute("INSERT INTO long_term_memories(user_id,memory_key,value,memory_type,importance,tags,source,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?,?) ON CONFLICT(user_id,memory_key) DO UPDATE SET value=excluded.value,memory_type=excluded.memory_type,importance=excluded.importance,tags=excluded.tags,source=excluded.source,updated_at=excluded.updated_at", values)
            connection.commit()

    def get_memories(self, user_id, key=None, limit=50):
        limit = max(1, min(int(limit), 100))
        with self.adapter.connect() as connection:
            if self.adapter.backend == "postgresql":
                with connection.cursor() as cursor:
                    query = "SELECT memory_key,value,memory_type,importance,tags,source,created_at,updated_at FROM long_term_memories WHERE user_id=%s"
                    params = [user_id]
                    if key:
                        query += " AND memory_key=%s"; params.append(key)
                    query += " ORDER BY importance DESC, updated_at DESC LIMIT %s"; params.append(limit)
                    cursor.execute(query, params); rows = cursor.fetchall()
            else:
                query = "SELECT memory_key,value,memory_type,importance,tags,source,created_at,updated_at FROM long_term_memories WHERE user_id=?"
                params = [user_id]
                if key:
                    query += " AND memory_key=?"; params.append(key)
                query += " ORDER BY importance DESC, updated_at DESC LIMIT ?"; params.append(limit)
                rows = connection.execute(query, params).fetchall()
        def convert(row):
            tags = row[4]
            try: tags = json.loads(tags)
            except (TypeError, json.JSONDecodeError): tags = [tag for tag in str(tags).split(",") if tag]
            return {"key": row[0], "value": row[1], "memory_type": row[2], "importance": row[3], "tags": tags, "source": row[5], "created_at": row[6].isoformat() if hasattr(row[6], "isoformat") else row[6], "updated_at": row[7].isoformat() if hasattr(row[7], "isoformat") else row[7]}
        return [convert(row) for row in rows]

    def delete_memories(self, user_id, key=None):
        with self.adapter.connect() as connection:
            if self.adapter.backend == "postgresql":
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM long_term_memories WHERE user_id=%s" + (" AND memory_key=%s" if key else ""), (user_id, key) if key else (user_id,)); count = cursor.rowcount
            else:
                result = connection.execute("DELETE FROM long_term_memories WHERE user_id=?" + (" AND memory_key=?" if key else ""), (user_id, key) if key else (user_id,)); count = result.rowcount
            connection.commit()
        return count

    def save_reminder(self, reminder):
        values = (reminder.id, reminder.user_id, reminder.message, reminder.due_at, reminder.status, reminder.notify, reminder.sound, reminder.created_at, reminder.delivered_at)
        with self.adapter.connect() as connection:
            if self.adapter.backend == "postgresql":
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO reminders(id,user_id,message,due_at,status,notify,sound,created_at,delivered_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT(id) DO UPDATE SET status=EXCLUDED.status,delivered_at=EXCLUDED.delivered_at", values)
            else:
                connection.execute("INSERT INTO reminders(id,user_id,message,due_at,status,notify,sound,created_at,delivered_at) VALUES (?,?,?,?,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET status=excluded.status,delivered_at=excluded.delivered_at", values)
            connection.commit()

    def get_reminders(self, user_id, include_delivered=False):
        with self.adapter.connect() as connection:
            query = "SELECT id,user_id,message,due_at,status,notify,sound,created_at,delivered_at FROM reminders WHERE user_id=%s" if self.adapter.backend == "postgresql" else "SELECT id,user_id,message,due_at,status,notify,sound,created_at,delivered_at FROM reminders WHERE user_id=?"
            if not include_delivered: query += " AND status NOT IN ('delivered','cancelled')"
            query += " ORDER BY due_at"
            if self.adapter.backend == "postgresql":
                with connection.cursor() as cursor: cursor.execute(query, (user_id,)); rows = cursor.fetchall()
            else: rows = connection.execute(query, (user_id,)).fetchall()
        return [dict(zip(("id","user_id","message","due_at","status","notify","sound","created_at","delivered_at"), row)) for row in rows]

    def set_secret(self, user_id, name, ciphertext):
        with self.adapter.connect() as connection:
            if self.adapter.backend == "postgresql":
                with connection.cursor() as cursor: cursor.execute("INSERT INTO encrypted_secrets(user_id,secret_name,ciphertext) VALUES (%s,%s,%s) ON CONFLICT(user_id,secret_name) DO UPDATE SET ciphertext=EXCLUDED.ciphertext", (user_id, name, ciphertext))
            else: connection.execute("INSERT INTO encrypted_secrets(user_id,secret_name,ciphertext) VALUES (?,?,?) ON CONFLICT(user_id,secret_name) DO UPDATE SET ciphertext=excluded.ciphertext", (user_id, name, ciphertext))
            connection.commit()

    def get_secret(self, user_id, name):
        with self.adapter.connect() as connection:
            if self.adapter.backend == "postgresql":
                with connection.cursor() as cursor: cursor.execute("SELECT ciphertext FROM encrypted_secrets WHERE user_id=%s AND secret_name=%s", (user_id, name)); row = cursor.fetchone()
            else: row = connection.execute("SELECT ciphertext FROM encrypted_secrets WHERE user_id=? AND secret_name=?", (user_id, name)).fetchone()
        return row[0] if row else None

    def delete_secret(self, user_id, name):
        with self.adapter.connect() as connection:
            if self.adapter.backend == "postgresql":
                with connection.cursor() as cursor: cursor.execute("DELETE FROM encrypted_secrets WHERE user_id=%s AND secret_name=%s", (user_id, name)); count = cursor.rowcount
            else: count = connection.execute("DELETE FROM encrypted_secrets WHERE user_id=? AND secret_name=?", (user_id, name)).rowcount
            connection.commit()
        return count > 0
