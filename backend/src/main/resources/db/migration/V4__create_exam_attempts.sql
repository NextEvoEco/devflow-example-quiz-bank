CREATE TABLE exam_attempts (
    id           BIGSERIAL PRIMARY KEY,
    quiz_id      BIGINT NOT NULL REFERENCES quizzes(id) ON DELETE CASCADE,
    score        INTEGER,
    total        INTEGER,
    started_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    submitted_at TIMESTAMPTZ
);

CREATE TABLE exam_answers (
    id              BIGSERIAL PRIMARY KEY,
    attempt_id      BIGINT NOT NULL REFERENCES exam_attempts(id) ON DELETE CASCADE,
    question_id     BIGINT NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    selected_option TEXT,
    UNIQUE (attempt_id, question_id)
);

CREATE INDEX idx_exam_attempts_quiz_id ON exam_attempts (quiz_id);
CREATE INDEX idx_exam_answers_attempt_id ON exam_answers (attempt_id);
