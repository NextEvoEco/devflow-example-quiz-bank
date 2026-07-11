from __future__ import annotations

from pathlib import Path

from backend.app import create_app


def make_payload(**overrides):
    payload = {
        "question": "What is 2 + 2?",
        "a": "3",
        "b": "4",
        "c": "5",
        "d": "6",
        "correct": "B",
        "difficulty": "Easy",
    }
    payload.update(overrides)
    return payload


def test_v1_release_flow_persists_across_app_instances(tmp_path: Path):
    database_path = tmp_path / "release-check.db"

    first_app = create_app(
        {
            "TESTING": True,
            "DATABASE_PATH": str(database_path),
        }
    )
    first_client = first_app.test_client()

    created = first_client.post("/api/questions", json=make_payload())
    question_id = created.get_json()["id"]

    updated = first_client.put(
        f"/api/questions/{question_id}",
        json=make_payload(question="What is 3 + 3?", b="6", difficulty="Hard"),
    )

    search = first_client.get("/api/questions?q=3%20%2B%203")

    second_app = create_app(
        {
            "TESTING": True,
            "DATABASE_PATH": str(database_path),
        }
    )
    second_client = second_app.test_client()
    persisted = second_client.get("/api/questions")

    deleted = second_client.delete(f"/api/questions/{question_id}")
    final_list = second_client.get("/api/questions")

    assert created.status_code == 201
    assert updated.status_code == 200
    assert search.status_code == 200
    assert search.get_json()["items"][0]["question"] == "What is 3 + 3?"
    assert persisted.status_code == 200
    assert persisted.get_json()["items"][0]["difficulty"] == "Hard"
    assert deleted.status_code == 200
    assert final_list.get_json()["items"] == []


def test_v1_homepage_and_scope_boundaries(client):
    response = client.get("/")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Question Bank" in html
    assert "Quiz Builder" in html
    assert "Online Exam" in html
    assert 'id="nav-questions"' in html
    assert 'id="nav-quizzes"' in html
    assert 'id="nav-exams"' in html
