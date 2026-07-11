import pytest

from backend.app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app(db_path=tmp_path / "exam_list_page.db")
    app.config.update(TESTING=True)
    return app.test_client()


def test_online_exam_nav_is_active(client):
    html = client.get("/").get_data(as_text=True)
    assert 'data-page="examList"' in html
    # No V3 placeholder disabled label should remain.
    assert 'title="Available in V3"' not in html


def test_available_exams_page_markup_present(client):
    html = client.get("/").get_data(as_text=True)
    assert 'id="page-examList"' in html
    assert 'id="exam-grid"' in html
    assert 'id="exam-empty-state"' in html
    assert "Available Exams" in html
    assert 'id="page-examTaking"' in html  # navigation target for Start Exam


def test_exam_list_js_loaded_and_wired(client):
    html = client.get("/").get_data(as_text=True)
    assert "/js/exam-list.js" in html

    js = client.get("/js/exam-list.js").get_data(as_text=True)
    assert js.strip() != ""
    assert "/api/quizzes" in js
    assert "registerPage" in js
    assert "Start Exam" in js
    assert "currentExamQuizId" in js  # carries quiz id into t04
    # Must not call the exam API in this task.
    assert "/api/exams" not in js


def test_question_bank_and_quiz_nav_unaffected(client):
    html = client.get("/").get_data(as_text=True)
    assert 'data-page="questions"' in html
    assert 'data-page="quizList"' in html
    assert 'id="page-questions"' in html
    assert 'id="page-quizList"' in html


def test_exam_list_reads_from_quiz_api(client):
    ids = []
    for i in range(3):
        r = client.post(
            "/api/questions",
            json={"question": f"Q{i}", "a": "1", "b": "2", "c": "3", "d": "4", "correct": "A"},
        )
        ids.append(r.get_json()["id"])
    client.post("/api/quizzes", json={"name": "Exam Quiz", "questionIds": ids})

    quizzes = client.get("/api/quizzes").get_json()
    assert len(quizzes) == 1
    assert quizzes[0]["name"] == "Exam Quiz"
    assert quizzes[0]["question_count"] == 3
