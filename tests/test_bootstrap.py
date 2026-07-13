"""Bootstrap and startup smoke tests."""

from pathlib import Path

from backend.database import SCHEMA_VERSION, get_connection, initialize_database


def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_index_serves_html(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Quiz Bank" in response.data


def test_sqlite_initializes_on_first_start(tmp_path):
    db_path = tmp_path / "quiz_bank.db"
    assert not db_path.exists()
    initialize_database(db_path)
    assert db_path.exists()

    conn = get_connection(db_path)
    try:
        version = conn.execute(
            "SELECT MAX(version) AS v FROM schema_migrations"
        ).fetchone()["v"]
        assert version == SCHEMA_VERSION
        tables = {
            row["name"]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }
        assert "questions" in tables
        assert "schema_migrations" in tables
    finally:
        conn.close()
