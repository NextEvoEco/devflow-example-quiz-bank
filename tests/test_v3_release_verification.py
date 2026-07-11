from __future__ import annotations

import sqlite3
from pathlib import Path

from backend.app import create_app


def make_question_payload(index: int, correct: str):
    return {
        "question": f"Question {index}?",
        "a": f"A{index}",
        "b": f"B{index}",
        "c": f"C{index}",
        "d": f"D{index}",
        "correct": correct,
        "difficulty": "Easy" if index % 2 else "Medium",
    }


def seed_quiz(client) -> tuple[int, list[int]]:
    question_ids = []
    for index, correct in enumerate(["A", "B", "C"], start=1):
        response = client.post("/api/questions", json=make_question_payload(index, correct))
        question_ids.append(response.get_json()["id"])

    created = client.post(
        "/api/quizzes",
        json={"name": "Release Exam Quiz", "questionIds": question_ids},
    )
    return created.get_json()["id"], question_ids


def test_v3_online_exam_release_flow(tmp_path: Path):
    database_path = tmp_path / "v3-release-check.db"
    app = create_app(
        {
            "TESTING": True,
            "DATABASE_PATH": str(database_path),
        }
    )
    client = app.test_client()

    quiz_id, question_ids = seed_quiz(client)

    homepage = client.get("/")
    quizzes = client.get("/api/quizzes")
    attempt_created = client.post("/api/exams/attempts", json={"quiz_id": quiz_id})
    attempt_id = attempt_created.get_json()["attempt_id"]

    save_first = client.put(
        f"/api/exams/attempts/{attempt_id}/answers/{question_ids[0]}",
        json={"selected_option": "A"},
    )
    save_second = client.put(
        f"/api/exams/attempts/{attempt_id}/answers/{question_ids[1]}",
        json={"selected_option": "C"},
    )
    save_third = client.put(
        f"/api/exams/attempts/{attempt_id}/answers/{question_ids[2]}",
        json={"selected_option": "C"},
    )

    submitted = client.post(f"/api/exams/attempts/{attempt_id}/submit")
    submitted_payload = submitted.get_json()
    double_submit = client.post(f"/api/exams/attempts/{attempt_id}/submit")

    assert homepage.status_code == 200
    assert 'id="nav-exams"' in homepage.get_data(as_text=True)

    assert quizzes.status_code == 200
    assert quizzes.get_json()["items"][0]["name"] == "Release Exam Quiz"

    assert attempt_created.status_code == 201
    assert save_first.status_code == 204
    assert save_second.status_code == 204
    assert save_third.status_code == 204

    assert submitted.status_code == 200
    assert submitted_payload["quiz_id"] == quiz_id
    assert submitted_payload["score"] == 2
    assert submitted_payload["total"] == 3
    assert submitted_payload["percentage"] == 67
    assert submitted_payload["submitted_at"] is not None
    assert submitted_payload["answers"][0]["is_correct"] is True
    assert submitted_payload["answers"][1]["is_correct"] is False
    assert submitted_payload["answers"][1]["correct_option"] == "B"
    assert submitted_payload["answers"][2]["is_correct"] is True

    assert double_submit.status_code == 409
    assert double_submit.get_json()["error"] == (
        f"Attempt {attempt_id} has already been submitted"
    )


def test_v3_abandoned_attempt_remains_unsubmitted(tmp_path: Path):
    database_path = tmp_path / "v3-abandoned-attempt.db"
    app = create_app(
        {
            "TESTING": True,
            "DATABASE_PATH": str(database_path),
        }
    )
    client = app.test_client()

    quiz_id, question_ids = seed_quiz(client)
    attempt_created = client.post("/api/exams/attempts", json={"quiz_id": quiz_id})
    attempt_id = attempt_created.get_json()["attempt_id"]
    save_answer = client.put(
        f"/api/exams/attempts/{attempt_id}/answers/{question_ids[0]}",
        json={"selected_option": "D"},
    )

    with sqlite3.connect(database_path) as connection:
        row = connection.execute(
            """
            SELECT score, total, submitted_at
            FROM exam_attempts
            WHERE id = ?
            """,
            (attempt_id,),
        ).fetchone()

    assert attempt_created.status_code == 201
    assert save_answer.status_code == 204
    assert row == (None, None, None)
