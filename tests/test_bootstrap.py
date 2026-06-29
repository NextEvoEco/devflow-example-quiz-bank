import sqlite3
from pathlib import Path

import pytest

from backend.app import create_app
from backend.database import database_exists, initialize_database


@pytest.fixture
def temp_db_path(tmp_path: Path) -> Path:
    return tmp_path / "quiz_bank.db"


def test_initialize_database_creates_schema(temp_db_path: Path) -> None:
    initialize_database(temp_db_path)

    assert temp_db_path.exists()

    with sqlite3.connect(temp_db_path) as connection:
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
        assert "schema_migrations" in tables
        assert "questions" in tables

        versions = {
            row[0]
            for row in connection.execute("SELECT version FROM schema_migrations")
        }
        assert 1 in versions
        assert 2 in versions


def test_create_app_initializes_database_on_first_run(
    temp_db_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("backend.app.initialize_database", lambda db_path=None: initialize_database(temp_db_path))

    app = create_app(temp_db_path)
    client = app.test_client()

    assert database_exists(temp_db_path)

    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_index_page_is_served(temp_db_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("backend.app.initialize_database", lambda db_path=None: initialize_database(temp_db_path))

    app = create_app(temp_db_path)
    client = app.test_client()

    response = client.get("/")
    assert response.status_code == 200
    assert b'id="question-table"' in response.data
    assert b'id="search-input"' in response.data
