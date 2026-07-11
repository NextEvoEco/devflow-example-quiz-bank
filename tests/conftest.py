import pytest

from backend.app import create_app
from backend.db import init_database


@pytest.fixture
def db_paths(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    db_path = data_dir / "quiz_bank.db"
    monkeypatch.setattr("backend.config.DATA_DIR", data_dir)
    monkeypatch.setattr("backend.config.DATABASE_PATH", db_path)
    monkeypatch.setattr("backend.db.DATA_DIR", data_dir)
    monkeypatch.setattr("backend.db.DATABASE_PATH", db_path)
    init_database()
    return data_dir, db_path


@pytest.fixture
def app(db_paths):
    application = create_app()
    application.config.update({"TESTING": True})
    return application


@pytest.fixture
def client(app):
    return app.test_client()
