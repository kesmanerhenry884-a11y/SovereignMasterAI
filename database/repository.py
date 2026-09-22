import os
from .connection import DatabaseAdapter


class MemoryRepository:
    def __init__(self, adapter=None):
        self.adapter = adapter or DatabaseAdapter()
        self.initialize()

    def initialize(self):
        conversation_sql = """
            CREATE TABLE IF NOT EXISTS conversations (
                id {id_type} PRIMARY KEY,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at {timestamp_default}
            )
        """
        memory_sql = """
            CREATE TABLE IF NOT EXISTS long_term_memories (
                user_id TEXT NOT NULL,
                memory_key TEXT NOT NULL,
                value TEXT NOT NULL,
                memory_type TEXT NOT NULL,
                importance INTEGER NOT NULL,
                tags TEXT NOT NULL,
                source TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                PRIMARY KEY (user_id, memory_key)
            )
        """
        if self.adapter.backend == "postgresql":
            with self.adapter.connect() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(conversation_sql.format(id_type="BIGSERIAL", timestamp_default="TIMESTAMPTZ DEFAULT NOW()"))
                    cursor.execute(memory_sql)
                connection.commit()
            return
        with self.adapter.connect() as connection:
            connection.execute(conversation_sql.format(id_type="INTEGER AUTOINCREMENT", timestamp_default="TEXT DEFAULT CURRENT_TIMESTAMP"))
            connection.execute("CREATE INDEX IF NOT EXISTS conversations_session_idx ON conversations(session_id, id)")
            connection.execute(memory_sql)
            connection.commit()

    def add_message(self, sid, role, content):
        if not sid or not content:
            return
        if self.adapter.backend == "postgresql":
            with self.adapter.connect() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO conversations(session_id, role, content) VALUES (%s, %s, %s)", (sid, role, content))
                connection.commit()
            return
        with self.adapter.connect() as connection:
            connection.execute("INSERT INTO conversations(session_id, role, content) VALUES (?, ?, ?)", (sid, role, content))
            connection.commit()

    def get_messages(self, sid, limit=None):
        limit = max(1, min(int(limit or os.getenv("MEMORY_CONTEXT_LIMIT", "20")), 100))
        if self.adapter.backend == "postgresql":
            with self.adapter.connect() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT role, content, created_at FROM conversations WHERE session_id=%s ORDER BY id DESC LIMIT %s", (sid, limit))
                    rows = cursor.fetchall()
            return [{"role": row[0], "content": row[1], "created_at": row[2].isoformat() if row[2] else None} for row in reversed(rows)]
        with self.adapter.connect() as connection:
            rows = connection.execute("SELECT role, content, created_at FROM conversations WHERE session_id=? ORDER BY id DESC LIMIT ?", (sid, limit)).fetchall()
        return [dict(row) for row in reversed(rows)]

    def upsert_memory(self, user_id, record):
        tags = ",".join(record.get("tags", []))
        values = (user_id, record["key"], record["value"], record["memory_type"], record["importance"], tags, record["source"], record["created_at"], record["updated_at"])
        with self.adapter.connect() as connection:
            if self.adapter.backend == "postgresql":
                with connection.cursor() as cursor:
                    cursor.execute("""INSERT INTO long_term_memories(user_id,memory_key,value,memory_type,importance,tags,source,created_at,updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT(user_id,memory_key) DO UPDATE SET value=EXCLUDED.value,memory_type=EXCLUDED.memory_type,importance=EXCLUDED.importance,tags=EXCLUDED.tags,source=EXCLUDED.source,updated_at=EXCLUDED.updated_at""", values)
            else:
                connection.execute("""INSERT INTO long_term_memories(user_id,memory_key,value,memory_type,importance,tags,source,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?,?) ON CONFLICT(user_id,memory_key) DO UPDATE SET value=excluded.value,memory_type=excluded.memory_type,importance=excluded.importance,tags=excluded.tags,source=excluded.source,updated_at=excluded.updated_at""", values)
            connection.commit()

    def get_memories(self, user_id, key=None, limit=50):
        limit = max(1, min(int(limit), 100))
        with self.adapter.connect() as connection:
            if self.adapter.backend == "postgresql":
                with connection.cursor() as cursor:
                    query = "SELECT memory_key,value,memory_type,importance,tags,source,created_at,updated_at FROM long_term_memories WHERE user_id=%s"
                    params = [user_id]
                    if key:
                        query += " AND memory_key=%s"
                        params.append(key)
                    query += " ORDER BY importance DESC, updated_at DESC LIMIT %s"
                    params.append(limit)
                    cursor.execute(query, params)
                    rows = cursor.fetchall()
            else:
                query = "SELECT memory_key,value,memory_type,importance,tags,source,created_at,updated_at FROM long_term_memories WHERE user_id=?"
                params = [user_id]
                if key:
                    query += " AND memory_key=?"
                    params.append(key)
                query += " ORDER BY importance DESC, updated_at DESC LIMIT ?"
                params.append(limit)
                rows = connection.execute(query, params).fetchall()
        return [{"key": row[0], "value": row[1], "memory_type": row[2], "importance": row[3], "tags": [tag for tag in row[4].split(",") if tag], "source": row[5], "created_at": row[6].isoformat() if hasattr(row[6], "isoformat") else row[6], "updated_at": row[7].isoformat() if hasattr(row[7], "isoformat") else row[7]} for row in rows]

    def delete_memories(self, user_id, key=None):
        with self.adapter.connect() as connection:
            if self.adapter.backend == "postgresql":
                with connection.cursor() as cursor:
                    if key:
                        cursor.execute("DELETE FROM long_term_memories WHERE user_id=%s AND memory_key=%s", (user_id, key))
                    else:
                        cursor.execute("DELETE FROM long_term_memories WHERE user_id=%s", (user_id,))
                    count = cursor.rowcount
            else:
                if key:
                    result = connection.execute("DELETE FROM long_term_memories WHERE user_id=? AND memory_key=?", (user_id, key))
                else:
                    result = connection.execute("DELETE FROM long_term_memories WHERE user_id=?", (user_id,))
                count = result.rowcount
            connection.commit()
        return count
