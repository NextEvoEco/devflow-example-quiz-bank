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


def test_exam_taking_page_includes_shell_and_controls(client) -> None:
    response = client.get("/")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'id="page-exam-taking"' in html
    assert 'id="exam-question-card"' in html
    assert 'id="exam-option-list"' in html
    assert 'id="exam-question-jump"' in html
    assert 'id="exam-prev-btn"' in html
    assert 'id="exam-next-btn"' in html
    assert 'id="exam-exit-btn"' in html
    assert 'id="page-exam-results"' in html


def test_exam_taking_assets_are_served(client) -> None:
    navigation_response = client.get("/js/navigation.js")
    exam_taking_response = client.get("/js/exam-taking.js")

    assert navigation_response.status_code == 200
    assert exam_taking_response.status_code == 200

    navigation_js = navigation_response.get_data(as_text=True)
    exam_taking_js = exam_taking_response.get_data(as_text=True)

    assert "examResults" in navigation_js
    assert "refreshExamTaking" in navigation_js
    assert "abandonExamSession" in navigation_js
    assert "createExamAttempt" in exam_taking_js
    assert "saveExamAnswer" in exam_taking_js
    assert "submitExamAttempt" in exam_taking_js
    assert "exam-option-btn" in exam_taking_js


def test_exam_flow_api_supports_taking_view(client) -> None:
    question_ids = create_questions(client, 3)
    quiz_id = client.post(
        "/api/quizzes",
        data=json.dumps(sample_quiz_payload(question_ids, name="History Exam")),
        content_type="application/json",
    ).get_json()["id"]

    attempt_response = client.post(
        "/api/exams/attempts",
        data=json.dumps({"quiz_id": quiz_id}),
        content_type="application/json",
    )
    assert attempt_response.status_code == 201
    attempt_id = attempt_response.get_json()["attempt_id"]

    save_response = client.put(
        f"/api/exams/attempts/{attempt_id}/answers/{question_ids[0]}",
        data=json.dumps({"selected_option": "B"}),
        content_type="application/json",
    )
    assert save_response.status_code == 204

    submit_response = client.post(f"/api/exams/attempts/{attempt_id}/submit")
    assert submit_response.status_code == 200
    summary = submit_response.get_json()
    assert summary["total"] == 3
    assert len(summary["answers"]) == 3
