import json
import sqlite3
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
    return app.test_client(), db_path


def create_quiz(client, question_count: int = 3, name: str = "Release Exam Quiz") -> tuple[int, list[int]]:
    question_ids = create_questions(client, question_count)
    response = client.post(
        "/api/quizzes",
        data=json.dumps(sample_quiz_payload(question_ids, name=name)),
        content_type="application/json",
    )
    assert response.status_code == 201
    quiz = response.get_json()
    return quiz["id"], quiz["questionIds"]


def test_v3_full_exam_api_lifecycle(client) -> None:
    test_client, db_path = client
    quiz_id, question_ids = create_quiz(test_client)

    attempt_response = test_client.post(
        "/api/exams/attempts",
        data=json.dumps({"quiz_id": quiz_id}),
        content_type="application/json",
    )
    assert attempt_response.status_code == 201
    attempt_id = attempt_response.get_json()["attempt_id"]

    answers = {
        question_ids[0]: "B",
        question_ids[1]: "A",
        question_ids[2]: "B",
    }
    for question_id, selected_option in answers.items():
        save_response = test_client.put(
            f"/api/exams/attempts/{attempt_id}/answers/{question_id}",
            data=json.dumps({"selected_option": selected_option}),
            content_type="application/json",
        )
        assert save_response.status_code == 204

    submit_response = test_client.post(f"/api/exams/attempts/{attempt_id}/submit")
    assert submit_response.status_code == 200
    summary = submit_response.get_json()
    assert summary["score"] == 2
    assert summary["total"] == 3
    assert summary["percentage"] == 67
    assert len(summary["answers"]) == 3
    assert summary["answers"][0]["is_correct"] is True
    assert summary["answers"][1]["is_correct"] is False

    with sqlite3.connect(db_path) as connection:
        row = connection.execute(
            "SELECT score, total, submitted_at FROM exam_attempts WHERE id = ?",
            (attempt_id,),
        ).fetchone()
        assert row is not None
        assert row[0] == 2
        assert row[1] == 3
        assert row[2] is not None


def test_v3_abandoned_attempt_remains_unscored(client) -> None:
    test_client, db_path = client
    quiz_id, question_ids = create_quiz(test_client, name="Abandoned Attempt Quiz")

    attempt_response = test_client.post(
        "/api/exams/attempts",
        data=json.dumps({"quiz_id": quiz_id}),
        content_type="application/json",
    )
    attempt_id = attempt_response.get_json()["attempt_id"]

    save_response = test_client.put(
        f"/api/exams/attempts/{attempt_id}/answers/{question_ids[0]}",
        data=json.dumps({"selected_option": "B"}),
        content_type="application/json",
    )
    assert save_response.status_code == 204

    with sqlite3.connect(db_path) as connection:
        row = connection.execute(
            "SELECT score, total, submitted_at FROM exam_attempts WHERE id = ?",
            (attempt_id,),
        ).fetchone()
        assert row is not None
        assert row[0] is None
        assert row[1] is None
        assert row[2] is None

        answer_count = connection.execute(
            "SELECT COUNT(*) FROM exam_answers WHERE attempt_id = ?",
            (attempt_id,),
        ).fetchone()[0]
        assert answer_count == 1


def test_v3_frontend_shell_includes_online_exam_modules(client) -> None:
    test_client, _ = client
    response = test_client.get("/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)

    assert 'data-nav-target="examList"' in html
    assert 'id="page-exam-list"' in html
    assert 'id="page-exam-taking"' in html
    assert 'id="page-exam-results"' in html
    assert 'id="exam-question-card"' in html
    assert 'id="exam-score-ring"' in html
    assert 'id="exam-answer-review-list"' in html
    assert 'disabled>Online Exam</button>' not in html.replace("\n", " ")

    for asset in (
        "/js/exam-list.js",
        "/js/exam-taking.js",
        "/js/exam-results.js",
    ):
        asset_response = test_client.get(asset)
        assert asset_response.status_code == 200

    exam_taking_js = test_client.get("/js/exam-taking.js").get_data(as_text=True)
    exam_results_js = test_client.get("/js/exam-results.js").get_data(as_text=True)
    assert "createExamAttempt" in exam_taking_js
    assert "submitExamAttempt" in exam_taking_js
    assert "renderAnswerReview" in exam_results_js
    assert "handleRetryQuiz" in exam_results_js


def test_v3_question_bank_regression_after_exam_operations(client) -> None:
    test_client, _ = client
    quiz_id, question_ids = create_quiz(test_client, name="Regression Exam Quiz")

    attempt_id = test_client.post(
        "/api/exams/attempts",
        data=json.dumps({"quiz_id": quiz_id}),
        content_type="application/json",
    ).get_json()["attempt_id"]

    for question_id in question_ids:
        test_client.put(
            f"/api/exams/attempts/{attempt_id}/answers/{question_id}",
            data=json.dumps({"selected_option": "B"}),
            content_type="application/json",
        )
    test_client.post(f"/api/exams/attempts/{attempt_id}/submit")

    list_response = test_client.get("/api/questions")
    assert list_response.status_code == 200
    assert len(list_response.get_json()["questions"]) == 3

    search_response = test_client.get("/api/questions?q=Question 2")
    assert len(search_response.get_json()["questions"]) == 1

    update_response = test_client.put(
        f"/api/questions/{question_ids[0]}",
        data=json.dumps({"question": "Updated after exam", "difficulty": "Hard"}),
        content_type="application/json",
    )
    assert update_response.status_code == 200
    assert update_response.get_json()["difficulty"] == "Hard"


def test_v3_quiz_builder_regression_after_exam_operations(client) -> None:
    test_client, _ = client
    quiz_id, question_ids = create_quiz(test_client, name="Builder Regression Quiz")

    attempt_id = test_client.post(
        "/api/exams/attempts",
        data=json.dumps({"quiz_id": quiz_id}),
        content_type="application/json",
    ).get_json()["attempt_id"]
    test_client.post(f"/api/exams/attempts/{attempt_id}/submit")

    list_response = test_client.get("/api/quizzes")
    assert list_response.status_code == 200
    quizzes = list_response.get_json()["quizzes"]
    assert len(quizzes) == 1
    assert quizzes[0]["name"] == "Builder Regression Quiz"
    assert quizzes[0]["questionCount"] == 3

    detail_response = test_client.get(f"/api/quizzes/{quiz_id}")
    assert detail_response.status_code == 200
    detail = detail_response.get_json()
    assert detail["questionIds"] == question_ids
    assert len(detail["questions"]) == 3

    update_response = test_client.put(
        f"/api/quizzes/{quiz_id}",
        data=json.dumps({"name": "Renamed After Exam"}),
        content_type="application/json",
    )
    assert update_response.status_code == 200
    assert update_response.get_json()["name"] == "Renamed After Exam"
