import sqlite3
from pathlib import Path

from backend.config import DATABASE_PATH, DATA_DIR

SCHEMA_VERSION = 3


def get_connection() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def _apply_migration_v1(connection: sqlite3.Connection) -> None:
    connection.execute(
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


def _apply_migration_v3(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS exam_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_id INTEGER NOT NULL,
            score INTEGER,
            total INTEGER,
            started_at TEXT NOT NULL DEFAULT (datetime('now')),
            submitted_at TEXT,
            FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS exam_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            attempt_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            selected_option TEXT CHECK (
                selected_option IS NULL OR selected_option IN ('A', 'B', 'C', 'D')
            ),
            UNIQUE (attempt_id, question_id),
            FOREIGN KEY (attempt_id) REFERENCES exam_attempts(id) ON DELETE CASCADE,
            FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
        )
        """
    )


def _apply_migration_v2(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS quizzes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
        """
    )
    connection.execute(
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


def _get_current_schema_version(connection: sqlite3.Connection) -> int:
    row = connection.execute(
        "SELECT version FROM schema_migrations ORDER BY version DESC LIMIT 1"
    ).fetchone()
    return row["version"] if row else -1


def init_database() -> Path:
    """Create the SQLite database and apply schema migrations on first run."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version INTEGER PRIMARY KEY,
                applied_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )

        current_version = _get_current_schema_version(connection)

        if current_version < 1:
            _apply_migration_v1(connection)
            connection.execute(
                "INSERT INTO schema_migrations (version) VALUES (?)",
                (1,),
            )

        current_version = _get_current_schema_version(connection)

        if current_version < 2:
            _apply_migration_v2(connection)
            connection.execute(
                "INSERT INTO schema_migrations (version) VALUES (?)",
                (2,),
            )

        current_version = _get_current_schema_version(connection)

        if current_version < 3:
            _apply_migration_v3(connection)
            connection.execute(
                "INSERT INTO schema_migrations (version) VALUES (?)",
                (3,),
            )

        connection.commit()

    return DATABASE_PATH
