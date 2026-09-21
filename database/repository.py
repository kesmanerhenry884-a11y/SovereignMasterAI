import os
from .connection import DatabaseAdapter


class MemoryRepository:
    def __init__(self, adapter=None):
        self.adapter = adapter or DatabaseAdapter()
        self.initialize()

    def initialize(self):
        if self.adapter.backend == "postgresql":
            sql = """
            CREATE TABLE IF NOT EXISTS conversations (
                id BIGSERIAL PRIMARY KEY,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMPTZ DEFAULT NOW()
            )
            """
            with self.adapter.connect() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                connection.commit()
            return

        with self.adapter.connect() as connection:
            connection.execute(
                """CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )"""
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS conversations_session_idx ON conversations(session_id, id)"
            )
            connection.commit()

    def add_message(self, sid, role, content):
        if not sid or not content:
            return
        if self.adapter.backend == "postgresql":
            with self.adapter.connect() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO conversations(session_id, role, content) VALUES (%s, %s, %s)",
                        (sid, role, content),
                    )
                connection.commit()
            return

        with self.adapter.connect() as connection:
            connection.execute(
                "INSERT INTO conversations(session_id, role, content) VALUES (?, ?, ?)",
                (sid, role, content),
            )
            connection.commit()

    def get_messages(self, sid, limit=None):
        limit = max(1, min(int(limit or os.getenv("MEMORY_CONTEXT_LIMIT", "20")), 100))
        if self.adapter.backend == "postgresql":
            with self.adapter.connect() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """SELECT role, content, created_at FROM conversations
                           WHERE session_id=%s ORDER BY id DESC LIMIT %s""",
                        (sid, limit),
                    )
                    rows = cursor.fetchall()
            return [
                {"role": row[0], "content": row[1], "created_at": row[2].isoformat() if row[2] else None}
                for row in reversed(rows)
            ]

        with self.adapter.connect() as connection:
            rows = connection.execute(
                """SELECT role, content, created_at FROM conversations
                   WHERE session_id=? ORDER BY id DESC LIMIT ?""",
                (sid, limit),
            ).fetchall()
        return [dict(row) for row in reversed(rows)]
