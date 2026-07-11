import pytest

from backend.app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app(db_path=tmp_path / "quiz_preview.db")
    app.config.update(TESTING=True)
    return app.test_client()


def test_preview_modal_markup_present(client):
    html = client.get("/").get_data(as_text=True)
    assert 'id="preview-overlay"' in html
    assert 'id="preview-title"' in html
    assert 'id="preview-body"' in html
    assert 'id="preview-close"' in html
    assert 'id="preview-close-btn"' in html


def test_preview_js_loaded_and_wired(client):
    html = client.get("/").get_data(as_text=True)
    assert "/js/quiz-preview.js" in html

    js = client.get("/js/quiz-preview.js").get_data(as_text=True)
    assert js.strip() != ""
    # Defines the hook the builder calls.
    assert "window.openQuizPreview" in js
    # Renders options and marks the correct answer.
    assert "is-correct" in js
    assert 'OPTION_LETTERS' in js


def test_builder_calls_preview_hook(client):
    js = client.get("/js/quiz-builder.js").get_data(as_text=True)
    assert "window.openQuizPreview" in js


def test_preview_reads_saved_quiz_shape(client):
    # A saved quiz's GET shape is the same as the builder draft the preview renders.
    ids = []
    for i in range(3):
        r = client.post(
            "/api/questions",
            json={"question": f"Q{i}", "a": "1", "b": "2", "c": "3", "d": "4",
                  "correct": "B", "difficulty": "Easy"},
        )
        ids.append(r.get_json()["id"])
    created = client.post("/api/quizzes", json={"name": "Prev", "questionIds": ids}).get_json()

    detail = client.get(f"/api/quizzes/{created['id']}").get_json()
    assert [q["id"] for q in detail["questions"]] == ids
    first = detail["questions"][0]
    for key in ("question", "a", "b", "c", "d", "correct"):
        assert key in first
