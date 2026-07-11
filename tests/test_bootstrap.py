import sqlite3

import pytest

from backend.app import create_app
from backend.db import init_database


@pytest.fixture
def app(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    db_path = data_dir / "quiz_bank.db"
    monkeypatch.setattr("backend.config.DATA_DIR", data_dir)
    monkeypatch.setattr("backend.config.DATABASE_PATH", db_path)
    monkeypatch.setattr("backend.db.DATA_DIR", data_dir)
    monkeypatch.setattr("backend.db.DATABASE_PATH", db_path)

    application = create_app()
    application.config.update({"TESTING": True})
    return application


@pytest.fixture
def client(app):
    return app.test_client()


def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_index_page_is_served(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Questions" in response.data
    assert b'id="question-table"' in response.data


def test_database_initializes_on_startup(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    db_path = data_dir / "quiz_bank.db"
    monkeypatch.setattr("backend.config.DATA_DIR", data_dir)
    monkeypatch.setattr("backend.config.DATABASE_PATH", db_path)
    monkeypatch.setattr("backend.db.DATA_DIR", data_dir)
    monkeypatch.setattr("backend.db.DATABASE_PATH", db_path)

    init_database()

    assert db_path.exists()

    with sqlite3.connect(db_path) as connection:
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }

    assert "schema_migrations" in tables
