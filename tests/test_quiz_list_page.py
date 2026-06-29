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


def test_quiz_list_page_includes_shell_and_navigation(client) -> None:
    response = client.get("/")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'id="page-quiz-list"' in html
    assert 'id="quiz-grid"' in html
    assert 'id="quiz-empty-state"' in html
    assert 'data-nav-target="quizList"' in html
    assert "New Quiz" in html
    assert "Create Quiz" in html


def test_quiz_list_assets_are_served(client) -> None:
    navigation_response = client.get("/js/navigation.js")
    quiz_list_response = client.get("/js/quiz-list.js")

    assert navigation_response.status_code == 200
    assert quiz_list_response.status_code == 200
    assert "navigateToPage" in navigation_response.get_data(as_text=True)
    assert "fetchQuizzes" in quiz_list_response.get_data(as_text=True)


def test_quiz_list_api_supports_page_rendering(client) -> None:
    question_ids = create_questions(client, 3)
    create_response = client.post(
        "/api/quizzes",
        data=json.dumps(sample_quiz_payload(question_ids, name="Science Quiz")),
        content_type="application/json",
    )
    assert create_response.status_code == 201

    list_response = client.get("/api/quizzes")
    assert list_response.status_code == 200
    quizzes = list_response.get_json()["quizzes"]
    assert len(quizzes) == 1
    assert quizzes[0]["name"] == "Science Quiz"
    assert quizzes[0]["questionCount"] == 3

    delete_response = client.delete(f"/api/quizzes/{quizzes[0]['id']}")
    assert delete_response.status_code == 204
    assert client.get("/api/quizzes").get_json()["quizzes"] == []


def test_question_bank_shell_remains_available(client) -> None:
    response = client.get("/")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'id="page-questions"' in html
    assert 'id="question-table"' in html
    assert 'data-nav-target="questions"' in html
