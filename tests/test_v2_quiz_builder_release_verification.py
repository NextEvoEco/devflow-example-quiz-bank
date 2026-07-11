from __future__ import annotations

from pathlib import Path

from backend.app import create_app


def make_question_payload(index: int):
    return {
        "question": f"Question {index}?",
        "a": f"A{index}",
        "b": f"B{index}",
        "c": f"C{index}",
        "d": f"D{index}",
        "correct": "A",
        "difficulty": "Easy" if index % 2 else "Medium",
    }


def seed_questions(client, count: int = 4) -> list[int]:
    question_ids = []
    for index in range(1, count + 1):
        response = client.post("/api/questions", json=make_question_payload(index))
        question_ids.append(response.get_json()["id"])
    return question_ids


def test_v2_quiz_builder_release_flow(tmp_path: Path):
    database_path = tmp_path / "v2-release-check.db"
    app = create_app(
        {
            "TESTING": True,
            "DATABASE_PATH": str(database_path),
        }
    )
    client = app.test_client()

    question_ids = seed_questions(client, 4)

    invalid_create = client.post(
        "/api/quizzes",
        json={"name": "Too Small", "questionIds": question_ids[:2]},
    )

    created = client.post(
        "/api/quizzes",
        json={"name": "Starter Quiz", "questionIds": question_ids[:3]},
    )
    quiz_id = created.get_json()["id"]

    listed = client.get("/api/quizzes")
    loaded = client.get(f"/api/quizzes/{quiz_id}")
    updated = client.put(
        f"/api/quizzes/{quiz_id}",
        json={
            "name": "Updated Quiz",
            "questionIds": [question_ids[3], question_ids[1], question_ids[0]],
        },
    )
    reloaded = client.get(f"/api/quizzes/{quiz_id}")
    deleted = client.delete(f"/api/quizzes/{quiz_id}")
    question_bank = client.get("/api/questions")

    assert invalid_create.status_code == 400
    assert invalid_create.get_json()["error"] == "A quiz must contain at least 3 questions"

    assert created.status_code == 201
    assert listed.status_code == 200
    assert listed.get_json()["items"][0]["name"] == "Starter Quiz"
    assert listed.get_json()["items"][0]["questionCount"] == 3

    assert loaded.status_code == 200
    assert loaded.get_json()["questionIds"] == question_ids[:3]
    assert len(loaded.get_json()["questions"]) == 3

    assert updated.status_code == 200
    assert updated.get_json()["name"] == "Updated Quiz"
    assert updated.get_json()["questionIds"] == [question_ids[3], question_ids[1], question_ids[0]]

    assert reloaded.status_code == 200
    assert reloaded.get_json()["questionIds"] == [question_ids[3], question_ids[1], question_ids[0]]
    assert [item["id"] for item in reloaded.get_json()["questions"]] == [
        question_ids[3],
        question_ids[1],
        question_ids[0],
    ]

    assert deleted.status_code == 200
    assert client.get(f"/api/quizzes/{quiz_id}").status_code == 404

    assert question_bank.status_code == 200
    assert len(question_bank.get_json()["items"]) == 4


def test_v2_homepage_contains_quiz_builder_and_preview_shell(client):
    response = client.get("/")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert 'id="nav-quizzes"' in html
    assert 'id="quiz-list-view"' in html
    assert 'id="quiz-builder-form"' in html
    assert 'id="quiz-preview-list"' in html
    assert 'id="nav-exams"' in html
