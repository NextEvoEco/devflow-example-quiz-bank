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


def test_o02_full_quiz_builder_api_lifecycle(client) -> None:
    question_ids = create_questions(client, 4)
    ordered_ids = [question_ids[2], question_ids[0], question_ids[3]]

    create_response = client.post(
        "/api/quizzes",
        data=json.dumps(sample_quiz_payload(ordered_ids, name="Lifecycle Quiz")),
        content_type="application/json",
    )
    assert create_response.status_code == 201
    quiz_id = create_response.get_json()["id"]

    list_response = client.get("/api/quizzes")
    assert list_response.status_code == 200
    summaries = list_response.get_json()["quizzes"]
    assert len(summaries) == 1
    assert summaries[0]["name"] == "Lifecycle Quiz"
    assert summaries[0]["questionCount"] == 3

    detail_response = client.get(f"/api/quizzes/{quiz_id}")
    assert detail_response.status_code == 200
    detail = detail_response.get_json()
    assert detail["questionIds"] == ordered_ids
    assert [question["id"] for question in detail["questions"]] == ordered_ids

    reordered_ids = [question_ids[1], question_ids[3], question_ids[2]]
    update_response = client.put(
        f"/api/quizzes/{quiz_id}",
        data=json.dumps(
            {
                "name": "Renamed Lifecycle Quiz",
                "questionIds": reordered_ids,
            }
        ),
        content_type="application/json",
    )
    assert update_response.status_code == 200
    updated = update_response.get_json()
    assert updated["name"] == "Renamed Lifecycle Quiz"
    assert updated["questionIds"] == reordered_ids

    delete_response = client.delete(f"/api/quizzes/{quiz_id}")
    assert delete_response.status_code == 204
    assert client.get("/api/quizzes").get_json()["quizzes"] == []
    assert client.get(f"/api/quizzes/{quiz_id}").status_code == 404


def test_o02_minimum_three_questions_validation_on_create_and_update(client) -> None:
    question_ids = create_questions(client, 3)

    create_response = client.post(
        "/api/quizzes",
        data=json.dumps(sample_quiz_payload(question_ids[:2])),
        content_type="application/json",
    )
    assert create_response.status_code == 400
    assert create_response.get_json()["field"] == "questionIds"

    valid_create = client.post(
        "/api/quizzes",
        data=json.dumps(sample_quiz_payload(question_ids, name="Valid Quiz")),
        content_type="application/json",
    )
    quiz_id = valid_create.get_json()["id"]

    update_response = client.put(
        f"/api/quizzes/{quiz_id}",
        data=json.dumps({"questionIds": question_ids[:2]}),
        content_type="application/json",
    )
    assert update_response.status_code == 400
    assert update_response.get_json()["field"] == "questionIds"


def test_o02_question_bank_regression_after_quiz_operations(client) -> None:
    question_ids = create_questions(client, 3)
    quiz_response = client.post(
        "/api/quizzes",
        data=json.dumps(sample_quiz_payload(question_ids, name="Regression Quiz")),
        content_type="application/json",
    )
    quiz_id = quiz_response.get_json()["id"]

    list_response = client.get("/api/questions")
    assert list_response.status_code == 200
    assert len(list_response.get_json()["questions"]) == 3

    search_response = client.get("/api/questions?q=Question 2")
    assert len(search_response.get_json()["questions"]) == 1

    update_response = client.put(
        f"/api/questions/{question_ids[0]}",
        data=json.dumps({"question": "Updated regression question", "difficulty": "Hard"}),
        content_type="application/json",
    )
    assert update_response.status_code == 200
    assert update_response.get_json()["difficulty"] == "Hard"

    client.delete(f"/api/quizzes/{quiz_id}")
    assert len(client.get("/api/questions").get_json()["questions"]) == 3

    delete_question = client.delete(f"/api/questions/{question_ids[2]}")
    assert delete_question.status_code == 204
    assert len(client.get("/api/questions").get_json()["questions"]) == 2


def test_o02_frontend_shell_includes_quiz_builder_modules(client) -> None:
    response = client.get("/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)

    assert 'id="page-quiz-list"' in html
    assert 'id="page-quiz-builder"' in html
    assert 'id="quiz-preview-modal"' in html
    assert 'data-nav-target="quizList"' in html
    assert 'src="/js/quiz-list.js"' in html
    assert 'src="/js/quiz-builder.js"' in html
    assert 'src="/js/quiz-preview.js"' in html

    for asset in (
        "/js/quiz-list.js",
        "/js/quiz-builder.js",
        "/js/quiz-preview.js",
    ):
        asset_response = client.get(asset)
        assert asset_response.status_code == 200


def test_o02_online_exam_nav_is_enabled(client) -> None:
    response = client.get("/api/exams")
    assert response.status_code == 404

    html = client.get("/").get_data(as_text=True)
    assert "Online Exam" in html
    assert 'data-nav-target="examList"' in html
    assert 'id="page-exam-list"' in html
    assert 'disabled>Online Exam</button>' not in html.replace("\n", " ")
