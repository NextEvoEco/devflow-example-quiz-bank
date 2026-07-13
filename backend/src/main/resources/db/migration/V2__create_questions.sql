-- V1 Question Bank table (shared logical schema contract).

CREATE TABLE questions (
    id              BIGSERIAL PRIMARY KEY,
    question        TEXT NOT NULL,
    option_a        TEXT NOT NULL,
    option_b        TEXT NOT NULL,
    option_c        TEXT NOT NULL,
    option_d        TEXT NOT NULL,
    correct         TEXT NOT NULL CHECK (correct IN ('A', 'B', 'C', 'D')),
    difficulty      TEXT NOT NULL DEFAULT 'Medium'
                        CHECK (difficulty IN ('Easy', 'Medium', 'Hard')),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_questions_question_text ON questions (question);
