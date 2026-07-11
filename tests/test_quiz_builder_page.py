import pytest

from backend.app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app(db_path=tmp_path / "quiz_builder_page.db")
    app.config.update(TESTING=True)
    return app.test_client()


def test_builder_markup_present(client):
    html = client.get("/").get_data(as_text=True)
    assert 'id="page-quizCreate"' in html
    assert 'id="quiz-name"' in html
    assert 'id="selected-list"' in html
    assert 'id="available-list"' in html
    assert 'id="available-search"' in html
    assert 'id="quiz-save-btn"' in html
    assert 'id="quiz-cancel-btn"' in html
    assert 'id="quiz-preview-btn"' in html
    assert 'id="quiz-form-error"' in html


def test_builder_js_loaded_and_wired(client):
    html = client.get("/").get_data(as_text=True)
    assert "/js/quiz-builder.js" in html

    js = client.get("/js/quiz-builder.js").get_data(as_text=True)
    assert js.strip() != ""
    assert 'registerPage("quizCreate"' in js
    assert "/api/quizzes" in js
    assert "/api/questions" in js
    assert '"POST"' in js and '"PUT"' in js
    assert "MIN_QUESTIONS" in js  # client-side min-3 guard


def test_quiz_list_no_longer_owns_quizcreate(client):
    # Ownership moved to quiz-builder.js; quiz-list.js must not register it.
    js = client.get("/js/quiz-list.js").get_data(as_text=True)
    assert 'registerPage("quizCreate"' not in js


def test_builder_backed_by_apis_end_to_end(client):
    # Seed questions the builder browses, then simulate the save it performs.
    ids = []
    for i in range(4):
        r = client.post(
            "/api/questions",
            json={"question": f"Q{i}", "a": "1", "b": "2", "c": "3", "d": "4", "correct": "A"},
        )
        ids.append(r.get_json()["id"])

    # Builder loads the bank
    assert len(client.get("/api/questions").get_json()) == 4

    # Save (create) with a chosen order
    order = [ids[2], ids[0], ids[3]]
    created = client.post("/api/quizzes", json={"name": "Built", "questionIds": order}).get_json()
    assert created["questionIds"] == order

    # Edit-mode prefill source preserves order
    detail = client.get(f"/api/quizzes/{created['id']}").get_json()
    assert [q["id"] for q in detail["questions"]] == order

    # Save (update) with new order
    updated = client.put(
        f"/api/quizzes/{created['id']}",
        json={"name": "Built v2", "questionIds": ids[:3]},
    ).get_json()
    assert updated["name"] == "Built v2"
    assert updated["questionIds"] == ids[:3]

    # Fewer than 3 rejected by the API (mirrors the client guard)
    assert client.post("/api/quizzes", json={"name": "Tiny", "questionIds": ids[:2]}).status_code == 400
