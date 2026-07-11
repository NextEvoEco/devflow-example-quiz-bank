"""Integration / release verification for Online Exam V3 (o03).

Ties the full exam flow together (create → answer → submit → score), checks the
abandonment and double-submit rules against the database, confirms the exam API
never leaks correct answers before submit, and guards V1/V2 against regression.
"""

import pytest

from backend.app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app(db_path=tmp_path / "v3_release.db")
    app.config.update(TESTING=True)
    return app.test_client()


def seed_quiz(client, correct_answers):
    """Seed questions with the given correct letters and a quiz over them."""
    ids = []
    for i, correct in enumerate(correct_answers):
        r = client.post(
            "/api/questions",
            json={
                "question": f"Question {i}?",
                "a": "opt A", "b": "opt B", "c": "opt C", "d": "opt D",
                "correct": correct, "difficulty": "Easy",
            },
        )
        ids.append(r.get_json()["id"])
    quiz_id = client.post("/api/quizzes", json={"name": "Release Exam", "questionIds": ids}).get_json()["id"]
    return quiz_id, ids


# --- Full exam flow ----------------------------------------------------------


def test_full_exam_flow_scores_correctly(client):
    quiz_id, ids = seed_quiz(client, ["A", "B", "C"])
    attempt_id = client.post("/api/exams/attempts", json={"quiz_id": quiz_id}).get_json()["attempt_id"]

    client.put(f"/api/exams/attempts/{attempt_id}/answers/{ids[0]}", json={"selected_option": "A"})  # correct
    client.put(f"/api/exams/attempts/{attempt_id}/answers/{ids[1]}", json={"selected_option": "B"})  # correct
    client.put(f"/api/exams/attempts/{attempt_id}/answers/{ids[2]}", json={"selected_option": "D"})  # wrong

    summary = client.post(f"/api/exams/attempts/{attempt_id}/submit").get_json()
    assert summary["score"] == 2
    assert summary["total"] == 3
    assert summary["percentage"] == 67
    # Review payload has everything the results page needs.
    assert len(summary["answers"]) == 3
    for a in summary["answers"]:
        assert {"question_id", "question_text", "options", "selected_option", "correct_option", "is_correct"} <= set(a)


def test_unanswered_questions_count_as_incorrect(client):
    quiz_id, ids = seed_quiz(client, ["A", "B", "C"])
    attempt_id = client.post("/api/exams/attempts", json={"quiz_id": quiz_id}).get_json()["attempt_id"]
    client.put(f"/api/exams/attempts/{attempt_id}/answers/{ids[0]}", json={"selected_option": "A"})  # only one answered
    summary = client.post(f"/api/exams/attempts/{attempt_id}/submit").get_json()
    assert summary["score"] == 1
    unanswered = [a for a in summary["answers"] if a["selected_option"] is None]
    assert len(unanswered) == 2
    assert all(a["is_correct"] is False for a in unanswered)


# --- Persistence rules -------------------------------------------------------


def test_abandoned_attempt_stays_unscored(client):
    quiz_id, ids = seed_quiz(client, ["A", "B", "C"])
    attempt_id = client.post("/api/exams/attempts", json={"quiz_id": quiz_id}).get_json()["attempt_id"]
    client.put(f"/api/exams/attempts/{attempt_id}/answers/{ids[0]}", json={"selected_option": "A"})
    # No submit call — the attempt must remain pending in the database.
    repo = client.application.config["EXAM_REPOSITORY"]
    attempt = repo.get_attempt(attempt_id)
    assert attempt["submitted_at"] is None
    assert attempt["score"] is None
    assert attempt["total"] is None


def test_double_submit_returns_409(client):
    quiz_id, _ = seed_quiz(client, ["A", "B", "C"])
    attempt_id = client.post("/api/exams/attempts", json={"quiz_id": quiz_id}).get_json()["attempt_id"]
    assert client.post(f"/api/exams/attempts/{attempt_id}/submit").status_code == 200
    assert client.post(f"/api/exams/attempts/{attempt_id}/submit").status_code == 409


def test_exam_api_does_not_leak_correct_before_submit(client):
    quiz_id, ids = seed_quiz(client, ["A", "B", "C"])
    create_resp = client.post("/api/exams/attempts", json={"quiz_id": quiz_id})
    assert "correct" not in create_resp.get_data(as_text=True)
    attempt_id = create_resp.get_json()["attempt_id"]
    save_resp = client.put(
        f"/api/exams/attempts/{attempt_id}/answers/{ids[0]}", json={"selected_option": "A"}
    )
    assert save_resp.status_code == 204
    assert save_resp.get_data(as_text=True) == ""


# --- Available Exams source --------------------------------------------------


def test_available_exams_lists_quizzes(client):
    seed_quiz(client, ["A", "B", "C"])
    quizzes = client.get("/api/quizzes").get_json()
    assert len(quizzes) == 1
    assert quizzes[0]["question_count"] == 3


# --- V1 / V2 regression ------------------------------------------------------


def test_question_bank_unaffected(client):
    created = client.post(
        "/api/questions",
        json={"question": "Regression?", "a": "1", "b": "2", "c": "3", "d": "4", "correct": "A"},
    ).get_json()
    assert client.get("/api/questions?search=regression").get_json()[0]["id"] == created["id"]
    assert client.put(
        f"/api/questions/{created['id']}",
        json={"question": "Regression edited", "a": "1", "b": "2", "c": "3", "d": "4", "correct": "B"},
    ).status_code == 200
    assert client.delete(f"/api/questions/{created['id']}").status_code == 204


def test_quiz_builder_unaffected(client):
    _, ids = seed_quiz(client, ["A", "B", "C"])
    # min-3 rule still enforced
    assert client.post("/api/quizzes", json={"name": "X", "questionIds": ids[:2]}).status_code == 400


# --- All views present -------------------------------------------------------


def test_all_app_views_present(client):
    html = client.get("/").get_data(as_text=True)
    for page_id in (
        "page-questions", "page-quizList", "page-quizCreate",
        "page-examList", "page-examTaking", "page-examResults",
    ):
        assert f'id="{page_id}"' in html
