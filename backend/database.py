import sqlite3
from pathlib import Path

from . import config

# Bump this and add a migration step in _migrate() when the schema changes.
SCHEMA_VERSION = 3

_CREATE_QUESTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS questions (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    question   TEXT NOT NULL,
    option_a   TEXT NOT NULL,
    option_b   TEXT NOT NULL,
    option_c   TEXT NOT NULL,
    option_d   TEXT NOT NULL,
    correct    TEXT NOT NULL,
    difficulty TEXT NOT NULL
)
"""

# Schema v2 (o02 Quiz Builder): quizzes and the ordered join table.
_CREATE_QUIZZES_TABLE = """
CREATE TABLE IF NOT EXISTS quizzes (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
)
"""

# quiz_questions holds only ordered references (no question content).
# Cascades keep join rows consistent when a quiz or a referenced question is deleted.
_CREATE_QUIZ_QUESTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS quiz_questions (
    quiz_id     INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    position    INTEGER NOT NULL,
    FOREIGN KEY (quiz_id) REFERENCES quizzes (id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions (id) ON DELETE CASCADE
)
"""

# Schema v3 (o03 Online Exam): exam attempts and their per-question answers.
# A pending attempt has score/total/submitted_at NULL until submit.
_CREATE_EXAM_ATTEMPTS_TABLE = """
CREATE TABLE IF NOT EXISTS exam_attempts (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_id      INTEGER NOT NULL,
    score        INTEGER,
    total        INTEGER,
    started_at   TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    submitted_at TEXT,
    FOREIGN KEY (quiz_id) REFERENCES quizzes (id) ON DELETE CASCADE
)
"""

# selected_option is nullable so unanswered questions can be recorded at submit.
# UNIQUE(attempt_id, question_id) lets save_answer use INSERT OR REPLACE.
_CREATE_EXAM_ANSWERS_TABLE = """
CREATE TABLE IF NOT EXISTS exam_answers (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    attempt_id      INTEGER NOT NULL,
    question_id     INTEGER NOT NULL,
    selected_option TEXT,
    UNIQUE (attempt_id, question_id),
    FOREIGN KEY (attempt_id) REFERENCES exam_attempts (id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions (id) ON DELETE CASCADE
)
"""


def get_connection(db_path=None) -> sqlite3.Connection:
    path = Path(db_path) if db_path is not None else config.DATABASE_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path=None) -> None:
    """Create the SQLite file and apply schema migrations on first start."""
    conn = get_connection(db_path)
    try:
        _migrate(conn)
    finally:
        conn.close()


def _migrate(conn: sqlite3.Connection) -> None:
    version = conn.execute("PRAGMA user_version").fetchone()[0]

    if version < 1:
        conn.execute(_CREATE_QUESTIONS_TABLE)
        conn.execute("PRAGMA user_version = 1")

    if version < 2:
        conn.execute(_CREATE_QUIZZES_TABLE)
        conn.execute(_CREATE_QUIZ_QUESTIONS_TABLE)
        conn.execute("PRAGMA user_version = 2")

    if version < 3:
        conn.execute(_CREATE_EXAM_ATTEMPTS_TABLE)
        conn.execute(_CREATE_EXAM_ANSWERS_TABLE)
        conn.execute("PRAGMA user_version = 3")

    conn.commit()
