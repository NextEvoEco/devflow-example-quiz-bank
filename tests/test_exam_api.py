import json
from pathlib import Path

import pytest

from backend.app import create_app
from backend.database import initialize_database
from tests.test_quizzes_api import create_questions, sample_quiz_payload


@pytest.fixture
def client(tmp_path: Path):
    db_path = tmp_path / "quiz_bank.db"
    initialize_database(db_path)
    app = create_app(db_path)
    return app.test_client()


def create_quiz(client, question_count: int = 3) -> tuple[int, list[int]]:
    question_ids = create_questions(client, question_count)
    response = client.post(
        "/api/quizzes",
        data=json.dumps(sample_quiz_payload(question_ids)),
        content_type="application/json",
    )
    assert response.status_code == 201
    quiz = response.get_json()
    return quiz["id"], quiz["questionIds"]


def test_create_attempt_returns_attempt_id(client) -> None:
    quiz_id, _ = create_quiz(client)

    response = client.post(
        "/api/exams/attempts",
        data=json.dumps({"quiz_id": quiz_id}),
        content_type="application/json",
    )

    assert response.status_code == 201
    assert "attempt_id" in response.get_json()
    assert isinstance(response.get_json()["attempt_id"], int)


def test_create_attempt_with_invalid_quiz_id_returns_404(client) -> None:
    response = client.post(
        "/api/exams/attempts",
        data=json.dumps({"quiz_id": 999}),
        content_type="application/json",
    )

    assert response.status_code == 404


def test_save_answer_returns_204(client) -> None:
    quiz_id, question_ids = create_quiz(client)
    attempt_id = client.post(
        "/api/exams/attempts",
        data=json.dumps({"quiz_id": quiz_id}),
        content_type="application/json",
    ).get_json()["attempt_id"]

    response = client.put(
        f"/api/exams/attempts/{attempt_id}/answers/{question_ids[0]}",
        data=json.dumps({"selected_option": "A"}),
        content_type="application/json",
    )

    assert response.status_code == 204
    assert response.data == b""


def test_save_answer_with_invalid_attempt_id_returns_404(client) -> None:
    response = client.put(
        "/api/exams/attempts/999/answers/1",
        data=json.dumps({"selected_option": "A"}),
        content_type="application/json",
    )

    assert response.status_code == 404


def test_submit_attempt_returns_score_summary(client) -> None:
    quiz_id, question_ids = create_quiz(client)
    attempt_id = client.post(
        "/api/exams/attempts",
        data=json.dumps({"quiz_id": quiz_id}),
        content_type="application/json",
    ).get_json()["attempt_id"]

    client.put(
        f"/api/exams/attempts/{attempt_id}/answers/{question_ids[0]}",
        data=json.dumps({"selected_option": "B"}),
        content_type="application/json",
    )
    client.put(
        f"/api/exams/attempts/{attempt_id}/answers/{question_ids[1]}",
        data=json.dumps({"selected_option": "A"}),
        content_type="application/json",
    )
    client.put(
        f"/api/exams/attempts/{attempt_id}/answers/{question_ids[2]}",
        data=json.dumps({"selected_option": "B"}),
        content_type="application/json",
    )

    response = client.post(f"/api/exams/attempts/{attempt_id}/submit")

    assert response.status_code == 200
    summary = response.get_json()
    assert summary["score"] == 2
    assert summary["total"] == 3
    assert summary["percentage"] == 67
    assert len(summary["answers"]) == 3

    first_answer = summary["answers"][0]
    assert first_answer["question_id"] == question_ids[0]
    assert first_answer["selected_option"] == "B"
    assert first_answer["correct_option"] == "B"
    assert first_answer["is_correct"] is True
    assert first_answer["question_text"]
    assert {"a", "b", "c", "d"} <= set(first_answer)


def test_submit_already_submitted_attempt_returns_409(client) -> None:
    quiz_id, question_ids = create_quiz(client)
    attempt_id = client.post(
        "/api/exams/attempts",
        data=json.dumps({"quiz_id": quiz_id}),
        content_type="application/json",
    ).get_json()["attempt_id"]

    client.put(
        f"/api/exams/attempts/{attempt_id}/answers/{question_ids[0]}",
        data=json.dumps({"selected_option": "B"}),
        content_type="application/json",
    )
    client.put(
        f"/api/exams/attempts/{attempt_id}/answers/{question_ids[1]}",
        data=json.dumps({"selected_option": "B"}),
        content_type="application/json",
    )
    client.put(
        f"/api/exams/attempts/{attempt_id}/answers/{question_ids[2]}",
        data=json.dumps({"selected_option": "B"}),
        content_type="application/json",
    )

    first_submit = client.post(f"/api/exams/attempts/{attempt_id}/submit")
    assert first_submit.status_code == 200

    second_submit = client.post(f"/api/exams/attempts/{attempt_id}/submit")
    assert second_submit.status_code == 409


def test_submit_with_invalid_attempt_id_returns_404(client) -> None:
    response = client.post("/api/exams/attempts/999/submit")
    assert response.status_code == 404


def test_save_answer_after_submit_returns_409(client) -> None:
    quiz_id, question_ids = create_quiz(client)
    attempt_id = client.post(
        "/api/exams/attempts",
        data=json.dumps({"quiz_id": quiz_id}),
        content_type="application/json",
    ).get_json()["attempt_id"]

    for question_id in question_ids:
        client.put(
            f"/api/exams/attempts/{attempt_id}/answers/{question_id}",
            data=json.dumps({"selected_option": "B"}),
            content_type="application/json",
        )

    client.post(f"/api/exams/attempts/{attempt_id}/submit")

    response = client.put(
        f"/api/exams/attempts/{attempt_id}/answers/{question_ids[0]}",
        data=json.dumps({"selected_option": "A"}),
        content_type="application/json",
    )
    assert response.status_code == 409
