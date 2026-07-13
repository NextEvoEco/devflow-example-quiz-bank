"""V3 release verification tests."""

from __future__ import annotations


def _seed(client):
    ids = [
        client.post(
            "/api/questions",
            json={
                "question": f"V3Q{i}",
                "a": "A",
                "b": "B",
                "c": "C",
                "d": "D",
                "correct": "A",
                "difficulty": "Easy",
            },
        ).get_json()["id"]
        for i in range(3)
    ]
    quiz_id = client.post(
        "/api/quizzes",
        json={"name": "V3 Quiz", "question_ids": ids},
    ).get_json()["id"]
    return quiz_id, ids


def test_v3_full_exam_flow(client):
    quiz_id, ids = _seed(client)
    attempt_id = client.post(
        "/api/exams/attempts", json={"quiz_id": quiz_id}
    ).get_json()["attempt_id"]
    for qid in ids:
        client.put(
            f"/api/exams/attempts/{attempt_id}/answers/{qid}",
            json={"selected_option": "A"},
        )
    result = client.post(f"/api/exams/attempts/{attempt_id}/submit").get_json()
    assert result["score"] == 3
    assert result["percentage"] == 100


def test_v3_abandoned_attempt_unscored(app, client):
    quiz_id, ids = _seed(client)
    attempt_id = client.post(
        "/api/exams/attempts", json={"quiz_id": quiz_id}
    ).get_json()["attempt_id"]
    client.put(
        f"/api/exams/attempts/{attempt_id}/answers/{ids[0]}",
        json={"selected_option": "A"},
    )
    from backend.exam_repository import ExamAttemptRepository

    repo = ExamAttemptRepository(app.config.get("DB_PATH"))
    attempt, _ = repo.get_attempt_with_answers(attempt_id)
    assert attempt.submitted_at is None
    assert attempt.score is None


def test_v3_double_submit_conflict(client):
    quiz_id, ids = _seed(client)
    attempt_id = client.post(
        "/api/exams/attempts", json={"quiz_id": quiz_id}
    ).get_json()["attempt_id"]
    assert client.post(f"/api/exams/attempts/{attempt_id}/submit").status_code == 200
    assert client.post(f"/api/exams/attempts/{attempt_id}/submit").status_code == 409
