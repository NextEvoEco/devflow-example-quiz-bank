"""Release-readiness checks for Question Bank V1.

These tie the objective success criteria together and guard the V1 scope
boundary (no Quiz Builder / Online Exam features).
"""

import pytest

from backend.app import create_app


def full_payload(**overrides):
    payload = {
        "question": "Release check question?",
        "a": "1", "b": "2", "c": "3", "d": "4",
        "correct": "A", "difficulty": "Easy",
    }
    payload.update(overrides)
    return payload


@pytest.fixture
def client(tmp_path):
    db_path = tmp_path / "release_test.db"
    app = create_app(db_path=db_path)
    app.config.update(TESTING=True)
    return app.test_client()


# --- Startup + persistence ---------------------------------------------------


def test_app_starts_and_serves_page_and_api(client):
    assert client.get("/").status_code == 200
    assert client.get("/api/questions").status_code == 200


def test_sqlite_persists_across_app_restart(tmp_path):
    db_path = tmp_path / "persist.db"

    app1 = create_app(db_path=db_path)
    created = app1.test_client().post("/api/questions", json=full_payload()).get_json()

    # A fresh app instance on the same database file simulates a restart.
    app2 = create_app(db_path=db_path)
    items = app2.test_client().get("/api/questions").get_json()

    assert any(q["id"] == created["id"] for q in items)


# --- Objective success criteria (end-to-end) --------------------------------


def test_full_crud_and_search_lifecycle(client):
    # Create
    created = client.post("/api/questions", json=full_payload(question="Alpha topic")).get_json()
    client.post("/api/questions", json=full_payload(question="Beta topic"))

    # List
    assert len(client.get("/api/questions").get_json()) == 2

    # Search
    hits = client.get("/api/questions?search=alpha").get_json()
    assert len(hits) == 1 and hits[0]["question"] == "Alpha topic"

    # Update
    updated = client.put(
        f"/api/questions/{created['id']}",
        json=full_payload(question="Alpha updated", difficulty="Hard"),
    ).get_json()
    assert updated["question"] == "Alpha updated" and updated["difficulty"] == "Hard"

    # Delete
    assert client.delete(f"/api/questions/{created['id']}").status_code == 204
    assert len(client.get("/api/questions").get_json()) == 1


def test_validation_and_difficulty_default_enforced(client):
    # Validation enforced at the API boundary
    bad = client.post("/api/questions", json=full_payload(question="", correct="Z"))
    assert bad.status_code == 400
    assert "question" in bad.get_json()["fields"]

    # Difficulty defaults when omitted
    payload = full_payload()
    del payload["difficulty"]
    created = client.post("/api/questions", json=payload).get_json()
    assert created["difficulty"] == "Medium"


def test_starts_with_empty_question_bank(client):
    assert client.get("/api/questions").get_json() == []

