"""SQLite bootstrap and versioned schema migrations."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from backend.config import DATA_DIR, DATABASE_PATH

SCHEMA_VERSION = 3


def get_connection(db_path: Path | str | None = None) -> sqlite3.Connection:
    path = Path(db_path) if db_path is not None else DATABASE_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _current_version(conn: sqlite3.Connection) -> int:
    conn.execute(
        "CREATE TABLE IF NOT EXISTS schema_migrations ("
        "version INTEGER PRIMARY KEY,"
        "applied_at TEXT NOT NULL DEFAULT (datetime('now'))"
        ")"
    )
    row = conn.execute("SELECT MAX(version) AS v FROM schema_migrations").fetchone()
    return int(row["v"] or 0)


def _apply_v1(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct TEXT NOT NULL CHECK (correct IN ('A', 'B', 'C', 'D')),
            difficulty TEXT NOT NULL DEFAULT 'Medium'
                CHECK (difficulty IN ('Easy', 'Medium', 'Hard')),
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
        """
    )


def _apply_v2(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS quizzes (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS quiz_questions (
            quiz_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            position INTEGER NOT NULL,
            PRIMARY KEY (quiz_id, question_id),
            FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE,
            FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
        )
        """
    )


def _apply_v3(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS exam_attempts (
            id INTEGER PRIMARY KEY,
            quiz_id INTEGER NOT NULL,
            score INTEGER,
            total INTEGER,
            started_at TEXT NOT NULL DEFAULT (datetime('now')),
            submitted_at TEXT,
            FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS exam_answers (
            id INTEGER PRIMARY KEY,
            attempt_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            selected_option TEXT,
            UNIQUE (attempt_id, question_id),
            FOREIGN KEY (attempt_id) REFERENCES exam_attempts(id) ON DELETE CASCADE,
            FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
        )
        """
    )


MIGRATIONS = {
    1: _apply_v1,
    2: _apply_v2,
    3: _apply_v3,
}


def initialize_database(db_path: Path | str | None = None) -> Path:
    """Create the database file and apply pending migrations."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = Path(db_path) if db_path is not None else DATABASE_PATH
    conn = get_connection(path)
    try:
        version = _current_version(conn)
        for target in range(version + 1, SCHEMA_VERSION + 1):
            migrate = MIGRATIONS[target]
            migrate(conn)
            conn.execute(
                "INSERT INTO schema_migrations (version) VALUES (?)",
                (target,),
            )
        conn.commit()
    finally:
        conn.close()
    return path


def reset_database(db_path: Path | str | None = None) -> Path:
    """Delete and recreate the database (for tests)."""
    path = Path(db_path) if db_path is not None else DATABASE_PATH
    if path.exists():
        path.unlink()
    return initialize_database(path)
