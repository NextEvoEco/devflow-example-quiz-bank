import pytest

from backend.app import create_app


@pytest.fixture
def client(tmp_path):
    db_path = tmp_path / "flows_test.db"
    app = create_app(db_path=db_path)
    app.config.update(TESTING=True)
    return app.test_client()


def base_payload(**overrides):
    payload = {
        "question": "Original question?",
        "a": "1", "b": "2", "c": "3", "d": "4",
        "correct": "A", "difficulty": "Easy",
    }
    payload.update(overrides)
    return payload


# --- UI surface present ------------------------------------------------------


def test_editor_modal_markup_present(client):
    html = client.get("/").get_data(as_text=True)
    assert 'id="editor-overlay"' in html
    assert 'id="editor-form"' in html
    for field_id in ("f-question", "f-a", "f-b", "f-c", "f-d", "f-correct", "f-difficulty"):
        assert f'id="{field_id}"' in html
    assert 'id="editor-save"' in html


def test_delete_dialog_markup_present(client):
    html = client.get("/").get_data(as_text=True)
    assert 'id="delete-overlay"' in html
    assert "Delete Question" in html
    assert 'id="delete-confirm"' in html


def test_app_js_wires_add_edit_delete(client):
    js = client.get("/js/app.js").get_data(as_text=True)
    assert "openAdd" in js
    assert "openEdit" in js
    assert "openDelete" in js
    # Uses the real API verbs, not frontend-only checks.
    assert '"POST"' in js and '"PUT"' in js and '"DELETE"' in js
    assert "body.fields" in js  # surfaces backend validation errors


# --- Flow lifecycle through the API the UI drives ---------------------------


def test_add_then_appears_in_list(client):
    created = client.post("/api/questions", json=base_payload(question="Added Q")).get_json()
    listed = client.get("/api/questions").get_json()
    assert any(q["id"] == created["id"] and q["question"] == "Added Q" for q in listed)


def test_edit_reflected_in_list(client):
    created = client.post("/api/questions", json=base_payload()).get_json()
    client.put(
        f"/api/questions/{created['id']}",
        json=base_payload(question="Edited Q", difficulty="Hard"),
    )
    listed = client.get("/api/questions").get_json()
    row = next(q for q in listed if q["id"] == created["id"])
    assert row["question"] == "Edited Q"
    assert row["difficulty"] == "Hard"


def test_delete_removes_from_list(client):
    created = client.post("/api/questions", json=base_payload()).get_json()
    assert client.delete(f"/api/questions/{created['id']}").status_code == 204
    listed = client.get("/api/questions").get_json()
    assert all(q["id"] != created["id"] for q in listed)


def test_invalid_submission_blocked_with_field_errors(client):
    resp = client.post("/api/questions", json=base_payload(question="", correct="X"))
    assert resp.status_code == 400
    fields = resp.get_json()["fields"]
    assert "question" in fields and "correct" in fields
