import sqlite3
from pathlib import Path

import pytest

from backend.app import create_app
from backend.database import SCHEMA_VERSION, initialize_database


@pytest.fixture
def db_path(tmp_path: Path) -> Path:
    return tmp_path / "quiz_bank.db"


def test_fresh_database_includes_quiz_tables(db_path: Path) -> None:
    initialize_database(db_path)

    with sqlite3.connect(db_path) as connection:
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
        assert "quizzes" in tables
        assert "quiz_questions" in tables

        versions = {
            row[0]
            for row in connection.execute("SELECT version FROM schema_migrations")
        }
        assert SCHEMA_VERSION in versions


def test_quizzes_table_columns(db_path: Path) -> None:
    initialize_database(db_path)

    with sqlite3.connect(db_path) as connection:
        columns = {
            row[1]
            for row in connection.execute("PRAGMA table_info(quizzes)")
        }
        assert columns == {"id", "name", "created_at"}


def test_quiz_questions_table_columns_and_foreign_keys(db_path: Path) -> None:
    initialize_database(db_path)

    with sqlite3.connect(db_path) as connection:
        columns = {
            row[1]
            for row in connection.execute("PRAGMA table_info(quiz_questions)")
        }
        assert columns == {"quiz_id", "question_id", "position"}

        foreign_keys = connection.execute("PRAGMA foreign_key_list(quiz_questions)").fetchall()
        references = {(row[2], row[4]) for row in foreign_keys}
        assert ("quizzes", "id") in references
        assert ("questions", "id") in references


def test_migration_from_existing_v2_database_preserves_questions(
    db_path: Path,
) -> None:
    from backend.database import _MIGRATIONS, get_connection

    with get_connection(db_path) as connection:
        connection.executescript(_MIGRATIONS[1])
        connection.executescript(_MIGRATIONS[2])
        connection.execute(
            "INSERT INTO schema_migrations (version) VALUES (?)",
            (1,),
        )
        connection.execute(
            "INSERT INTO schema_migrations (version) VALUES (?)",
            (2,),
        )
        connection.execute(
            """
            INSERT INTO questions (
                question, option_a, option_b, option_c, option_d, correct, difficulty
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            ("Existing question", "A1", "B1", "C1", "D1", "A", "Easy"),
        )
        connection.commit()

    initialize_database(db_path)

    with sqlite3.connect(db_path) as connection:
        row = connection.execute("SELECT question FROM questions").fetchone()
        assert row is not None
        assert row[0] == "Existing question"

        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
        assert "quizzes" in tables
        assert "quiz_questions" in tables

        versions = {
            row[0]
            for row in connection.execute("SELECT version FROM schema_migrations")
        }
        assert 3 in versions


def test_app_starts_after_quiz_schema_migration(
    db_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "backend.app.initialize_database",
        lambda path=None: initialize_database(db_path),
    )

    app = create_app(db_path)
    client = app.test_client()

    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
