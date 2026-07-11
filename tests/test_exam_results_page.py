import pytest

from backend.app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app(db_path=tmp_path / "exam_results_page.db")
    app.config.update(TESTING=True)
    return app.test_client()


def test_results_markup_present(client):
    html = client.get("/").get_data(as_text=True)
    assert 'id="page-examResults"' in html
    assert "Exam Complete!" in html
    assert 'id="results-quiz-name"' in html
    assert 'id="results-ring"' in html
    assert 'id="results-pct"' in html
    assert 'id="results-correct"' in html
    assert 'id="results-incorrect"' in html
    assert 'id="results-review"' in html
    assert 'id="results-back-btn"' in html
    assert 'id="results-retry-btn"' in html


def test_results_js_loaded_and_wired(client):
    html = client.get("/").get_data(as_text=True)
    assert "/js/exam-results.js" in html

    js = client.get("/js/exam-results.js").get_data(as_text=True)
    assert js.strip() != ""
    assert 'registerPage("examResults"' in js
    assert "window.examResult" in js         # reads the payload from state
    assert 'navigate("examTaking"' in js     # Retry Quiz restarts the same quiz
    assert 'navigate("examList"' in js       # Back to Exams
    # Must not re-fetch results from the API.
    assert "fetch(" not in js


def test_exam_taking_no_longer_owns_examresults(client):
    js = client.get("/js/exam-taking.js").get_data(as_text=True)
    assert 'registerPage("examResults"' not in js
    assert "exam-results-placeholder" not in js


def test_results_shows_correct_and_incorrect_distinction(client):
    # The results renderer must style correct vs incorrect differently.
    js = client.get("/js/exam-results.js").get_data(as_text=True)
    assert "is-correct" in js
    assert "is-incorrect" in js
    assert "Correct" in js and "Incorrect" in js


def test_submit_payload_has_everything_results_needs(client):
    # End-to-end: the submit response carries all fields the results page renders,
    # so no extra API call is needed.
    ids = []
    for correct in ["A", "B", "C"]:
        r = client.post(
            "/api/questions",
            json={"question": f"Q-{correct}", "a": "one", "b": "two", "c": "three", "d": "four",
                  "correct": correct, "difficulty": "Easy"},
        )
        ids.append(r.get_json()["id"])
    quiz_id = client.post("/api/quizzes", json={"name": "Res", "questionIds": ids}).get_json()["id"]
    attempt_id = client.post("/api/exams/attempts", json={"quiz_id": quiz_id}).get_json()["attempt_id"]
    client.put(f"/api/exams/attempts/{attempt_id}/answers/{ids[0]}", json={"selected_option": "A"})  # correct
    client.put(f"/api/exams/attempts/{attempt_id}/answers/{ids[1]}", json={"selected_option": "D"})  # wrong
    # ids[2] left unanswered

    summary = client.post(f"/api/exams/attempts/{attempt_id}/submit").get_json()
    assert summary["score"] == 1
    assert summary["total"] == 3
    for a in summary["answers"]:
        assert {"question_id", "question_text", "options", "selected_option", "correct_option", "is_correct"} <= set(a)
    # Unanswered question surfaces as selected_option None, is_correct False.
    unanswered = next(a for a in summary["answers"] if a["question_id"] == ids[2])
    assert unanswered["selected_option"] is None
    assert unanswered["is_correct"] is False
