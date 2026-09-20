import os, sqlite3
class DatabaseAdapter:
    def __init__(self, dsn=None): self.dsn=dsn or os.getenv("DATABASE_URL", ":memory:"); self.backend="postgresql" if self.dsn.startswith("postgres") else "sqlite"
    def connect(self):
        if self.backend=="postgresql":
            try:
                import psycopg
                return psycopg.connect(self.dsn)
            except ImportError as exc: raise RuntimeError("Install psycopg to use PostgreSQL") from exc
        conn=sqlite3.connect(self.dsn); conn.row_factory=sqlite3.Row; return conn
    def health(self):
        try:
            with self.connect() as c: c.execute("SELECT 1")
            return {"available":True,"backend":self.backend}
        except Exception as exc: return {"available":False,"backend":self.backend,"error":str(exc)}
