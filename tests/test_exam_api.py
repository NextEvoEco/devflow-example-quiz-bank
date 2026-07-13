"""Exam API tests."""

from __future__ import annotations


def _setup_quiz(client):
    ids = []
    for i in range(3):
        ids.append(
            client.post(
                "/api/questions",
                json={
                    "question": f"EQ{i}",
                    "a": "A",
                    "b": "B",
                    "c": "C",
                    "d": "D",
                    "correct": "A",
                    "difficulty": "Easy",
                },
            ).get_json()["id"]
        )
    quiz = client.post(
        "/api/quizzes",
        json={"name": "API Exam", "question_ids": ids},
    ).get_json()
    return quiz["id"], ids


def test_exam_api_happy_path_and_errors(client):
    quiz_id, ids = _setup_quiz(client)

    bad = client.post("/api/exams/attempts", json={"quiz_id": 999999})
    assert bad.status_code == 404

    created = client.post("/api/exams/attempts", json={"quiz_id": quiz_id})
    assert created.status_code == 201
    attempt_id = created.get_json()["attempt_id"]

    saved = client.put(
        f"/api/exams/attempts/{attempt_id}/answers/{ids[0]}",
        json={"selected_option": "A"},
    )
    assert saved.status_code == 204
    client.put(
        f"/api/exams/attempts/{attempt_id}/answers/{ids[1]}",
        json={"selected_option": "B"},
    )

    submitted = client.post(f"/api/exams/attempts/{attempt_id}/submit")
    assert submitted.status_code == 200
    body = submitted.get_json()
    assert body["score"] == 1
    assert body["total"] == 3
    assert body["percentage"] == 33
    assert len(body["answers"]) == 3

    again = client.post(f"/api/exams/attempts/{attempt_id}/submit")
    assert again.status_code == 409

    missing = client.put(
        "/api/exams/attempts/999999/answers/1",
        json={"selected_option": "A"},
    )
    assert missing.status_code == 404
