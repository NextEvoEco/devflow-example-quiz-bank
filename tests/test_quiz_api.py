"""Quiz API and schema tests."""

from __future__ import annotations

from backend.database import SCHEMA_VERSION, get_connection, initialize_database


def _question(client, text: str):
    response = client.post(
        "/api/questions",
        json={
            "question": text,
            "a": "A1",
            "b": "B1",
            "c": "C1",
            "d": "D1",
            "correct": "A",
            "difficulty": "Easy",
        },
    )
    assert response.status_code == 201
    return response.get_json()["id"]


def test_quiz_schema_migration(tmp_path):
    db_path = tmp_path / "quiz.db"
    initialize_database(db_path)
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
            )
        }
        assert "quizzes" in tables
        assert "quiz_questions" in tables
    finally:
        conn.close()


def test_quiz_api_crud_and_validation(client):
    ids = [_question(client, f"Q{i}") for i in range(3)]
    too_few = client.post(
        "/api/quizzes",
        json={"name": "Short", "question_ids": ids[:2]},
    )
    assert too_few.status_code == 400

    missing = client.post(
        "/api/quizzes",
        json={"name": "Bad", "question_ids": ids + [999999]},
    )
    assert missing.status_code == 400

    created = client.post(
        "/api/quizzes",
        json={"name": "Geo", "question_ids": ids},
    )
    assert created.status_code == 201
    quiz_id = created.get_json()["id"]
    assert created.get_json()["question_count"] == 3

    listed = client.get("/api/quizzes")
    assert listed.status_code == 200
    assert any(q["id"] == quiz_id for q in listed.get_json())

    detail = client.get(f"/api/quizzes/{quiz_id}")
    assert detail.status_code == 200
    assert [q["id"] for q in detail.get_json()["questions"]] == ids

    fourth = _question(client, "Q3")
    updated = client.put(
        f"/api/quizzes/{quiz_id}",
        json={"name": "Geo 2", "question_ids": [ids[2], ids[1], ids[0], fourth]},
    )
    assert updated.status_code == 200
    assert updated.get_json()["name"] == "Geo 2"
    assert updated.get_json()["question_ids"][0] == ids[2]

    assert client.delete(f"/api/quizzes/{quiz_id}").status_code == 204
    assert client.get(f"/api/quizzes/{quiz_id}").status_code == 404
