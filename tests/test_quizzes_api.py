import json
from pathlib import Path

import pytest

from backend.app import create_app
from backend.database import initialize_database


@pytest.fixture
def client(tmp_path: Path):
    db_path = tmp_path / "quiz_bank.db"
    initialize_database(db_path)
    app = create_app(db_path)
    return app.test_client()


def sample_question_payload(**overrides) -> dict[str, str]:
    payload = {
        "question": "What is 2 + 2?",
        "a": "3",
        "b": "4",
        "c": "5",
        "d": "6",
        "correct": "B",
    }
    payload.update(overrides)
    return payload


def create_questions(client, count: int) -> list[int]:
    question_ids: list[int] = []
    for index in range(count):
        response = client.post(
            "/api/questions",
            data=json.dumps(
                sample_question_payload(question=f"Question {index + 1}?")
            ),
            content_type="application/json",
        )
        assert response.status_code == 201
        question_ids.append(response.get_json()["id"])
    return question_ids


def sample_quiz_payload(question_ids: list[int], **overrides) -> dict:
    payload = {
        "name": "Sample Quiz",
        "questionIds": question_ids,
    }
    payload.update(overrides)
    return payload


def test_create_quiz_returns_201(client) -> None:
    question_ids = create_questions(client, 3)

    response = client.post(
        "/api/quizzes",
        data=json.dumps(sample_quiz_payload(question_ids)),
        content_type="application/json",
    )

    assert response.status_code == 201
    quiz = response.get_json()
    assert quiz["name"] == "Sample Quiz"
    assert quiz["questionIds"] == question_ids
    assert len(quiz["questions"]) == 3
    assert quiz["questions"][0]["question"] == "Question 1?"


def test_create_quiz_with_fewer_than_three_questions_returns_400(client) -> None:
    question_ids = create_questions(client, 2)

    response = client.post(
        "/api/quizzes",
        data=json.dumps(sample_quiz_payload(question_ids)),
        content_type="application/json",
    )

    assert response.status_code == 400
    payload = response.get_json()
    assert payload["field"] == "questionIds"
    assert "at least 3" in payload["error"].lower()


def test_create_quiz_with_missing_question_id_returns_400(client) -> None:
    question_ids = create_questions(client, 3)
    question_ids[2] = 999

    response = client.post(
        "/api/quizzes",
        data=json.dumps(sample_quiz_payload(question_ids)),
        content_type="application/json",
    )

    assert response.status_code == 400
    payload = response.get_json()
    assert payload["field"] == "questionIds"
    assert "999" in payload["error"]


def test_create_quiz_rejects_duplicate_question_ids(client) -> None:
    question_ids = create_questions(client, 2)
    duplicate_ids = [question_ids[0], question_ids[1], question_ids[0]]

    response = client.post(
        "/api/quizzes",
        data=json.dumps(sample_quiz_payload(duplicate_ids)),
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.get_json()["field"] == "questionIds"


def test_list_quizzes_returns_summaries(client) -> None:
    question_ids = create_questions(client, 3)
    create_response = client.post(
        "/api/quizzes",
        data=json.dumps(sample_quiz_payload(question_ids, name="Quiz A")),
        content_type="application/json",
    )
    quiz_id = create_response.get_json()["id"]

    response = client.get("/api/quizzes")
    assert response.status_code == 200
    quizzes = response.get_json()["quizzes"]
    assert len(quizzes) == 1
    assert quizzes[0]["id"] == quiz_id
    assert quizzes[0]["name"] == "Quiz A"
    assert quizzes[0]["questionCount"] == 3


def test_get_quiz_returns_ordered_question_details(client) -> None:
    question_ids = create_questions(client, 3)
    create_response = client.post(
        "/api/quizzes",
        data=json.dumps(
            sample_quiz_payload(
                [question_ids[2], question_ids[0], question_ids[1]],
                name="Ordered Quiz",
            )
        ),
        content_type="application/json",
    )
    quiz_id = create_response.get_json()["id"]

    response = client.get(f"/api/quizzes/{quiz_id}")
    assert response.status_code == 200
    quiz = response.get_json()
    assert quiz["name"] == "Ordered Quiz"
    assert quiz["questionIds"] == [question_ids[2], question_ids[0], question_ids[1]]
    assert [item["id"] for item in quiz["questions"]] == quiz["questionIds"]
    assert all("a" in item and "correct" in item for item in quiz["questions"])


def test_update_quiz_name_and_question_list(client) -> None:
    question_ids = create_questions(client, 4)
    create_response = client.post(
        "/api/quizzes",
        data=json.dumps(sample_quiz_payload(question_ids[:3], name="Original Quiz")),
        content_type="application/json",
    )
    quiz_id = create_response.get_json()["id"]

    update_response = client.put(
        f"/api/quizzes/{quiz_id}",
        data=json.dumps(
            {
                "name": "Updated Quiz",
                "questionIds": [question_ids[3], question_ids[1], question_ids[0]],
            }
        ),
        content_type="application/json",
    )
    assert update_response.status_code == 200
    updated = update_response.get_json()
    assert updated["name"] == "Updated Quiz"
    assert updated["questionIds"] == [question_ids[3], question_ids[1], question_ids[0]]


def test_update_quiz_with_fewer_than_three_questions_returns_400(client) -> None:
    question_ids = create_questions(client, 3)
    create_response = client.post(
        "/api/quizzes",
        data=json.dumps(sample_quiz_payload(question_ids)),
        content_type="application/json",
    )
    quiz_id = create_response.get_json()["id"]

    response = client.put(
        f"/api/quizzes/{quiz_id}",
        data=json.dumps({"questionIds": question_ids[:2]}),
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.get_json()["field"] == "questionIds"


def test_delete_quiz_removes_quiz_and_question_references(client) -> None:
    question_ids = create_questions(client, 3)
    create_response = client.post(
        "/api/quizzes",
        data=json.dumps(sample_quiz_payload(question_ids)),
        content_type="application/json",
    )
    quiz_id = create_response.get_json()["id"]

    delete_response = client.delete(f"/api/quizzes/{quiz_id}")
    assert delete_response.status_code == 204

    list_response = client.get("/api/quizzes")
    assert list_response.get_json()["quizzes"] == []

    missing_response = client.get(f"/api/quizzes/{quiz_id}")
    assert missing_response.status_code == 404

    questions_response = client.get("/api/questions")
    assert len(questions_response.get_json()["questions"]) == 3


def test_get_missing_quiz_returns_404(client) -> None:
    response = client.get("/api/quizzes/999")
    assert response.status_code == 404
