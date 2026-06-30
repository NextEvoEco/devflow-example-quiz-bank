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


def test_exam_list_page_includes_shell_and_navigation(client) -> None:
    response = client.get("/")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'id="page-exam-list"' in html
    assert 'id="exam-grid"' in html
    assert 'id="exam-empty-state"' in html
    assert 'id="page-exam-taking"' in html
    assert 'data-nav-target="examList"' in html
    assert "Available Exams" in html
    assert 'disabled>Online Exam</button>' not in html.replace("\n", " ")

    exam_list_js = client.get("/js/exam-list.js").get_data(as_text=True)
    assert "Start Exam" in exam_list_js


def test_exam_list_assets_are_served(client) -> None:
    navigation_response = client.get("/js/navigation.js")
    exam_list_response = client.get("/js/exam-list.js")

    assert navigation_response.status_code == 200
    assert exam_list_response.status_code == 200
    assert "examList" in navigation_response.get_data(as_text=True)
    assert "fetchQuizzes" in exam_list_response.get_data(as_text=True)
    assert "startExam" in exam_list_response.get_data(as_text=True)
    assert "attemptId" in exam_list_response.get_data(as_text=True)


def test_exam_list_api_supports_page_rendering(client) -> None:
    question_ids = create_questions(client, 3)
    create_response = client.post(
        "/api/quizzes",
        data=json.dumps(sample_quiz_payload(question_ids, name="Geography Exam")),
        content_type="application/json",
    )
    assert create_response.status_code == 201

    list_response = client.get("/api/quizzes")
    assert list_response.status_code == 200
    quizzes = list_response.get_json()["quizzes"]
    assert len(quizzes) == 1
    assert quizzes[0]["name"] == "Geography Exam"
    assert quizzes[0]["questionCount"] == 3


def test_question_bank_and_quiz_builder_navigation_remain_available(client) -> None:
    response = client.get("/")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'id="page-questions"' in html
    assert 'id="page-quiz-list"' in html
    assert 'data-nav-target="questions"' in html
    assert 'data-nav-target="quizList"' in html
    assert "New Quiz" in html
