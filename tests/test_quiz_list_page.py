import pytest

from backend.app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app(db_path=tmp_path / "quiz_list_page.db")
    app.config.update(TESTING=True)
    return app.test_client()


def test_quiz_builder_nav_is_active(client):
    html = client.get("/").get_data(as_text=True)
    # Quiz Builder nav item is enabled and wired to the quizList page.
    assert 'data-page="quizList"' in html


def test_quiz_list_page_markup_present(client):
    html = client.get("/").get_data(as_text=True)
    assert 'id="page-quizList"' in html
    assert 'id="quiz-grid"' in html
    assert 'id="quiz-count"' in html
    assert 'id="new-quiz-btn"' in html
    assert 'id="quiz-empty-state"' in html
    assert 'id="page-quizCreate"' in html  # navigation target for New/Edit


def test_quiz_delete_dialog_present(client):
    html = client.get("/").get_data(as_text=True)
    assert 'id="quiz-delete-overlay"' in html
    assert "Delete Quiz" in html
    assert 'id="quiz-delete-confirm"' in html


def test_quiz_list_js_loaded_and_wired(client):
    html = client.get("/").get_data(as_text=True)
    assert '/js/quiz-list.js' in html

    js = client.get("/js/quiz-list.js").get_data(as_text=True)
    assert js.strip() != ""
    assert "/api/quizzes" in js
    assert "loadQuizzes" in js
    assert "registerPage" in js  # integrates with the nav controller


def test_app_js_has_navigation_controller(client):
    js = client.get("/js/app.js").get_data(as_text=True)
    assert "function navigate" in js
    assert "registerPage" in js


def test_question_bank_page_unaffected(client):
    html = client.get("/").get_data(as_text=True)
    # QB page + nav entry must remain intact.
    assert 'id="page-questions"' in html
    assert 'data-page="questions"' in html
    assert 'id="question-table"' in html


def test_quiz_list_reads_from_api(client):
    # Seed questions + a quiz, then confirm the endpoint the page consumes.
    ids = []
    for i in range(3):
        r = client.post(
            "/api/questions",
            json={"question": f"Q{i}", "a": "1", "b": "2", "c": "3", "d": "4", "correct": "A"},
        )
        ids.append(r.get_json()["id"])
    client.post("/api/quizzes", json={"name": "Sample Quiz", "questionIds": ids})

    quizzes = client.get("/api/quizzes").get_json()
    assert len(quizzes) == 1
    assert quizzes[0]["name"] == "Sample Quiz"
    assert quizzes[0]["question_count"] == 3
