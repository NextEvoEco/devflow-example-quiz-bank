import sqlite3
from pathlib import Path

from backend.config import DATABASE_PATH, DATA_DIR

SCHEMA_VERSION = 4

_MIGRATIONS: dict[int, str] = {
    1: """
    CREATE TABLE IF NOT EXISTS schema_migrations (
        version INTEGER PRIMARY KEY,
        applied_at TEXT NOT NULL DEFAULT (datetime('now'))
    );
    """,
    2: """
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
    );
    """,
    3: """
    CREATE TABLE IF NOT EXISTS quizzes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        created_at TEXT NOT NULL DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS quiz_questions (
        quiz_id INTEGER NOT NULL,
        question_id INTEGER NOT NULL,
        position INTEGER NOT NULL,
        PRIMARY KEY (quiz_id, question_id),
        UNIQUE (quiz_id, position),
        FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE,
        FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
    );
    """,
    4: """
    CREATE TABLE IF NOT EXISTS exam_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_id INTEGER NOT NULL,
        score INTEGER,
        total INTEGER,
        started_at TEXT NOT NULL DEFAULT (datetime('now')),
        submitted_at TEXT,
        FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
    );

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
    );
    """,
}


def ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_connection(db_path: Path | None = None) -> sqlite3.Connection:
    path = db_path or DATABASE_PATH
    ensure_data_dir()
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def _get_applied_versions(connection: sqlite3.Connection) -> set[int]:
    table_exists = connection.execute(
        """
        SELECT name FROM sqlite_master
        WHERE type = 'table' AND name = 'schema_migrations'
        """
    ).fetchone()
    if table_exists is None:
        return set()

    rows = connection.execute("SELECT version FROM schema_migrations").fetchall()
    return {row["version"] for row in rows}


def _apply_migrations(connection: sqlite3.Connection) -> None:
    applied_versions = _get_applied_versions(connection)

    for version in sorted(_MIGRATIONS):
        if version in applied_versions:
            continue
        connection.executescript(_MIGRATIONS[version])
        connection.execute(
            "INSERT OR IGNORE INTO schema_migrations (version) VALUES (?)",
            (version,),
        )


def initialize_database(db_path: Path | None = None) -> Path:
    """Create the SQLite database and apply pending schema migrations."""
    path = db_path or DATABASE_PATH
    ensure_data_dir()

    with get_connection(path) as connection:
        _apply_migrations(connection)
        connection.commit()

    return path


def database_exists(db_path: Path | None = None) -> bool:
    path = db_path or DATABASE_PATH
    return path.exists()
