from __future__ import annotations

import sqlite3
from pathlib import Path

from backend.db import initialize_database


def fetch_table_columns(database_path: Path, table_name: str) -> list[str]:
    with sqlite3.connect(database_path) as connection:
        rows = connection.execute(f"PRAGMA table_info({table_name})").fetchall()
    return [row[1] for row in rows]


def test_quiz_schema_tables_are_created(tmp_path: Path):
    database_path = tmp_path / "quiz-schema.db"

    initialize_database(database_path)

    assert fetch_table_columns(database_path, "quizzes") == [
        "id",
        "name",
        "created_at",
    ]
    assert fetch_table_columns(database_path, "quiz_questions") == [
        "quiz_id",
        "question_id",
        "position",
    ]


def test_quiz_schema_migration_preserves_existing_question_data(tmp_path: Path):
    database_path = tmp_path / "existing-questions.db"
    with sqlite3.connect(database_path) as connection:
        connection.executescript(
            """
            CREATE TABLE questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                option_a TEXT NOT NULL,
                option_b TEXT NOT NULL,
                option_c TEXT NOT NULL,
                option_d TEXT NOT NULL,
                correct_answer TEXT NOT NULL,
                difficulty TEXT NOT NULL DEFAULT 'Medium',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            INSERT INTO questions (
                question, option_a, option_b, option_c, option_d, correct_answer, difficulty
            ) VALUES (
                'What is 2 + 2?', '3', '4', '5', '6', 'B', 'Easy'
            );
            """
        )
        connection.commit()

    initialize_database(database_path)

    with sqlite3.connect(database_path) as connection:
        question_count = connection.execute(
            "SELECT COUNT(*) FROM questions"
        ).fetchone()[0]
        migration_versions = connection.execute(
            "SELECT version FROM schema_migrations ORDER BY version"
        ).fetchall()

    assert question_count == 1
    assert migration_versions == [(1,), (2,), (3,)]
