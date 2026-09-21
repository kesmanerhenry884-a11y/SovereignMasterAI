# Optional pgVector extension migration. Apply only after PostgreSQL inspection and backup.
CREATE EXTENSION IF NOT EXISTS vector;
ALTER TABLE knowledge ADD COLUMN IF NOT EXISTS embedding vector(1536);
