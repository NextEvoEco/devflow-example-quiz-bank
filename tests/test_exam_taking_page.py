import pytest

from backend.app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app(db_path=tmp_path / "exam_taking_page.db")
    app.config.update(TESTING=True)
    return app.test_client()


def test_exam_taking_markup_present(client):
    html = client.get("/").get_data(as_text=True)
    assert 'id="page-examTaking"' in html
    assert 'id="exam-question-text"' in html
    assert 'id="exam-options"' in html
    assert 'id="exam-progress-fill"' in html
    assert 'id="exam-progress-label"' in html
    assert 'id="exam-prev-btn"' in html
    assert 'id="exam-next-btn"' in html
    assert 'id="exam-exit-btn"' in html
    assert 'id="exam-nav-numbers"' in html
    # Results view target for Submit (placeholder until t05).
    assert 'id="page-examResults"' in html


def test_exam_taking_js_loaded_and_wired(client):
    html = client.get("/").get_data(as_text=True)
    assert "/js/exam-taking.js" in html

    js = client.get("/js/exam-taking.js").get_data(as_text=True)
    assert js.strip() != ""
    assert 'registerPage("examTaking"' in js
    assert "/api/exams" in js                       # exam API base
    assert "/attempts" in js                        # create attempt
    assert "/answers/" in js                        # save answer
    assert "/submit" in js                          # submit
    assert "window.examResult" in js                # hands payload to results view


def test_exam_list_no_longer_owns_examtaking(client):
    js = client.get("/js/exam-list.js").get_data(as_text=True)
    assert 'registerPage("examTaking"' not in js


def test_exam_taking_does_not_hardcode_correct_marker(client):
    # The taking view must not render a correct-answer marker. Only the results
    # placeholder / submit response deals with scoring.
    js = client.get("/js/exam-taking.js").get_data(as_text=True)
    assert "is-correct" not in js
    assert "correct_option" not in js


def test_qb_and_quiz_frontend_untouched(client):
    # Sanity: V1/V2 page modules still present and referenced.
    html = client.get("/").get_data(as_text=True)
    assert "/js/app.js" in html
    assert "/js/quiz-builder.js" in html
    assert 'id="page-questions"' in html
    assert 'id="page-quizCreate"' in html


def test_full_exam_flow_through_api(client):
    """Exercise the exact API sequence the taking view drives."""
    ids = []
    for correct in ["A", "B", "C"]:
        r = client.post(
            "/api/questions",
            json={"question": f"Q-{correct}", "a": "1", "b": "2", "c": "3", "d": "4",
                  "correct": correct, "difficulty": "Easy"},
        )
        ids.append(r.get_json()["id"])
    quiz_id = client.post("/api/quizzes", json={"name": "Flow", "questionIds": ids}).get_json()["id"]

    # start
    attempt_id = client.post("/api/exams/attempts", json={"quiz_id": quiz_id}).get_json()["attempt_id"]
    # answer 2 correct, 1 wrong
    assert client.put(f"/api/exams/attempts/{attempt_id}/answers/{ids[0]}", json={"selected_option": "A"}).status_code == 204
    assert client.put(f"/api/exams/attempts/{attempt_id}/answers/{ids[1]}", json={"selected_option": "B"}).status_code == 204
    assert client.put(f"/api/exams/attempts/{attempt_id}/answers/{ids[2]}", json={"selected_option": "A"}).status_code == 204
    # change an answer (navigation back + reselect)
    assert client.put(f"/api/exams/attempts/{attempt_id}/answers/{ids[2]}", json={"selected_option": "C"}).status_code == 204
    # submit
    summary = client.post(f"/api/exams/attempts/{attempt_id}/submit").get_json()
    assert summary["score"] == 3
    assert summary["total"] == 3
    assert summary["percentage"] == 100
