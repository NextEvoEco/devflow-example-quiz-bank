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


def test_quiz_builder_page_includes_shell_and_controls(client) -> None:
    response = client.get("/")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'id="page-quiz-builder"' in html
    assert 'id="quiz-name-input"' in html
    assert 'id="selected-questions-list"' in html
    assert 'id="available-questions-list"' in html
    assert 'id="quiz-builder-save-btn"' in html
    assert 'id="quiz-builder-preview-btn"' in html
    assert 'id="quiz-preview-modal"' in html


def test_quiz_builder_assets_are_served(client) -> None:
    navigation_response = client.get("/js/navigation.js")
    builder_response = client.get("/js/quiz-builder.js")

    assert navigation_response.status_code == 200
    assert builder_response.status_code == 200
    assert "refreshQuizBuilder" in navigation_response.get_data(as_text=True)
    builder_js = builder_response.get_data(as_text=True)
    assert "loadQuizBuilder" in builder_js
    assert "openQuizPreview" in builder_js
    assert "MIN_QUIZ_QUESTIONS = 3" in builder_js


def test_quiz_builder_api_supports_create_and_edit_flow(client) -> None:
    question_ids = create_questions(client, 4)
    payload = sample_quiz_payload(question_ids[:3], name="Builder Quiz")

    create_response = client.post(
        "/api/quizzes",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert create_response.status_code == 201
    quiz_id = create_response.get_json()["id"]

    detail_response = client.get(f"/api/quizzes/{quiz_id}")
    assert detail_response.status_code == 200
    detail = detail_response.get_json()
    assert detail["name"] == "Builder Quiz"
    assert detail["questionIds"] == question_ids[:3]

    update_payload = sample_quiz_payload(question_ids, name="Updated Builder Quiz")
    update_response = client.put(
        f"/api/quizzes/{quiz_id}",
        data=json.dumps(update_payload),
        content_type="application/json",
    )
    assert update_response.status_code == 200
    updated = client.get(f"/api/quizzes/{quiz_id}").get_json()
    assert updated["name"] == "Updated Builder Quiz"
    assert updated["questionIds"] == question_ids


def test_quiz_builder_api_blocks_fewer_than_three_questions(client) -> None:
    question_ids = create_questions(client, 2)
    payload = sample_quiz_payload(question_ids, name="Too Short")

    response = client.post(
        "/api/quizzes",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert response.status_code == 400
    assert "at least 3" in response.get_json()["error"].lower()


def test_question_bank_api_remains_available_for_builder(client) -> None:
    create_questions(client, 3)

    response = client.get("/api/questions")
    assert response.status_code == 200
    questions = response.get_json()["questions"]
    assert len(questions) == 3
    assert "question" in questions[0]
    assert "difficulty" in questions[0]
