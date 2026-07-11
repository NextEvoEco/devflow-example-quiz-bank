from __future__ import annotations

import sqlite3


def test_index_serves_shell(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "Quiz Bank" in response.get_data(as_text=True)


def test_health_reports_database_path(client):
    response = client.get("/health")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "ok"
    assert payload["database_path"].endswith("quiz_bank.db")


def test_database_initializes_questions_table(app):
    connection = sqlite3.connect(app.config["DATABASE_PATH"])
    try:
      tables = connection.execute(
          "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'questions'"
      ).fetchall()
    finally:
      connection.close()

    assert tables == [("questions",)]

