-- Quiz Bank Flyway baseline.
-- Domain tables (questions, quizzes, exam_*) are added by later migrations.
-- This migration confirms automatic schema management is active.

CREATE TABLE IF NOT EXISTS schema_bootstrap (
    id INTEGER PRIMARY KEY DEFAULT 1 CHECK (id = 1),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO schema_bootstrap (id)
VALUES (1)
ON CONFLICT (id) DO NOTHING;
