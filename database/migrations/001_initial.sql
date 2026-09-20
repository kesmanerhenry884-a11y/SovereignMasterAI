# Initial PostgreSQL schema. Apply only after inspecting the target database and taking a backup.
CREATE TABLE IF NOT EXISTS users (id BIGSERIAL PRIMARY KEY, username TEXT UNIQUE, created_at TIMESTAMPTZ DEFAULT NOW());
CREATE TABLE IF NOT EXISTS sessions (id TEXT PRIMARY KEY, user_id BIGINT REFERENCES users(id), created_at TIMESTAMPTZ DEFAULT NOW(), language TEXT DEFAULT 'auto', mode TEXT DEFAULT 'general');
CREATE TABLE IF NOT EXISTS conversations (id BIGSERIAL PRIMARY KEY, session_id TEXT REFERENCES sessions(id), role TEXT NOT NULL, content TEXT NOT NULL, created_at TIMESTAMPTZ DEFAULT NOW());
CREATE TABLE IF NOT EXISTS memories (id BIGSERIAL PRIMARY KEY, session_id TEXT REFERENCES sessions(id), key TEXT NOT NULL, value TEXT, created_at TIMESTAMPTZ DEFAULT NOW());
CREATE TABLE IF NOT EXISTS knowledge (id BIGSERIAL PRIMARY KEY, source TEXT, domain TEXT, content TEXT NOT NULL, reliability REAL DEFAULT 0, metadata JSONB, created_at TIMESTAMPTZ DEFAULT NOW());
CREATE TABLE IF NOT EXISTS engine_events (id BIGSERIAL PRIMARY KEY, event_type TEXT, payload JSONB, created_at TIMESTAMPTZ DEFAULT NOW());
CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT, updated_at TIMESTAMPTZ DEFAULT NOW());
