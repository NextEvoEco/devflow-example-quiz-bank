import sqlite3

import pytest

from backend.db import get_connection, init_database


def _table_columns(connection: sqlite3.Connection, table_name: str) -> list[str]:
    rows = connection.execute(f"PRAGMA table_info({table_name})").fetchall()
    return [row[1] for row in rows]


def test_quiz_tables_are_created(db_paths):
    data_dir, db_path = db_paths

    with sqlite3.connect(db_path) as connection:
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }

    assert "quizzes" in tables
    assert "quiz_questions" in tables


def test_quizzes_table_has_required_columns(db_paths):
    _, db_path = db_paths

    with sqlite3.connect(db_path) as connection:
        columns = _table_columns(connection, "quizzes")

    assert columns == ["id", "name", "created_at"]


def test_quiz_questions_table_has_required_columns(db_paths):
    _, db_path = db_paths

    with sqlite3.connect(db_path) as connection:
        columns = _table_columns(connection, "quiz_questions")

    assert columns == ["quiz_id", "question_id", "position"]


def test_existing_questions_table_is_unaffected(db_paths):
    _, db_path = db_paths

    with sqlite3.connect(db_path) as connection:
        columns = _table_columns(connection, "questions")

    assert "question" in columns
    assert "option_a" in columns
    assert "correct" in columns


def test_quiz_questions_foreign_keys_are_enforced(db_paths):
    init_database()

    with get_connection() as connection:
        connection.execute("INSERT INTO quizzes (name) VALUES (?)", ("Sample Quiz",))
        quiz_id = connection.execute("SELECT id FROM quizzes").fetchone()[0]

        connection.execute(
            """
            INSERT INTO questions (
                question, option_a, option_b, option_c, option_d, correct, difficulty
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            ("Schema test question", "A1", "B1", "C1", "D1", "A", "Easy"),
        )
        question_id = connection.execute("SELECT id FROM questions").fetchone()[0]

        connection.execute(
            """
            INSERT INTO quiz_questions (quiz_id, question_id, position)
            VALUES (?, ?, ?)
            """,
            (quiz_id, question_id, 0),
        )
        connection.commit()

        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                """
                INSERT INTO quiz_questions (quiz_id, question_id, position)
                VALUES (?, ?, ?)
                """,
                (quiz_id, 9999, 1),
            )


def test_app_starts_after_quiz_schema_migration(client):
    response = client.get("/api/health")
    assert response.status_code == 200
