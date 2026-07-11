from __future__ import annotations

import sqlite3
from pathlib import Path

from .config import DATABASE_PATH


MIGRATIONS: list[tuple[int, str]] = [
    (
        1,
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
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """,
    ),
    (
        2,
        """
        CREATE TABLE IF NOT EXISTS quizzes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS quiz_questions (
            quiz_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            position INTEGER NOT NULL,
            PRIMARY KEY (quiz_id, position),
            FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE,
            FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
        );
        """,
    ),
    (
        3,
        """
        CREATE TABLE IF NOT EXISTS exam_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_id INTEGER NOT NULL,
            score INTEGER NULL,
            total INTEGER NULL,
            started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            submitted_at TEXT NULL,
            FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS exam_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            attempt_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            selected_option TEXT NULL CHECK (selected_option IN ('A', 'B', 'C', 'D')),
            UNIQUE (attempt_id, question_id),
            FOREIGN KEY (attempt_id) REFERENCES exam_attempts(id) ON DELETE CASCADE,
            FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
        );
        """,
    ),
]


def initialize_database(database_path: Path = DATABASE_PATH) -> Path:
    """Create or migrate the SQLite database to the latest local schema version."""
    database_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        _ensure_schema_migrations_table(connection)
        _apply_pending_migrations(connection)
        connection.commit()
    return database_path


def _ensure_schema_migrations_table(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version INTEGER PRIMARY KEY,
            applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """
    )


def _apply_pending_migrations(connection: sqlite3.Connection) -> None:
    applied_versions = {
        row[0]
        for row in connection.execute("SELECT version FROM schema_migrations").fetchall()
    }

    for version, migration_sql in MIGRATIONS:
        if version in applied_versions:
            continue
        connection.executescript(migration_sql)
        connection.execute(
            "INSERT INTO schema_migrations (version) VALUES (?)",
            (version,),
        )
