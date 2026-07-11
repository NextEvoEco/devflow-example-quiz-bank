import pytest

from backend.app import create_app


def make_payload(**overrides):
    payload = {
        "question": "What is the capital of France?",
        "a": "Berlin",
        "b": "Paris",
        "c": "Madrid",
        "d": "Rome",
        "correct": "B",
        "difficulty": "Easy",
    }
    payload.update(overrides)
    return payload


@pytest.fixture
def client(tmp_path):
    db_path = tmp_path / "api_test.db"
    app = create_app(db_path=db_path)
    app.config.update(TESTING=True)
    return app.test_client()


def _create(client, **overrides):
    return client.post("/api/questions", json=make_payload(**overrides))


# --- success paths -----------------------------------------------------------


def test_create_returns_201_with_body(client):
    resp = _create(client)
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["id"] is not None
    assert body["question"] == "What is the capital of France?"
    assert body["correct"] == "B"


def test_list_returns_created_questions(client):
    _create(client, question="First")
    _create(client, question="Second")

    resp = client.get("/api/questions")
    assert resp.status_code == 200
    items = resp.get_json()
    assert [q["question"] for q in items] == ["First", "Second"]


def test_search_filters_results(client):
    _create(client, question="Python basics")
    _create(client, question="History facts")

    resp = client.get("/api/questions?search=python")
    assert resp.status_code == 200
    items = resp.get_json()
    assert len(items) == 1
    assert items[0]["question"] == "Python basics"


def test_get_single_question(client):
    created = _create(client).get_json()
    resp = client.get(f"/api/questions/{created['id']}")
    assert resp.status_code == 200
    assert resp.get_json()["id"] == created["id"]


def test_update_changes_question(client):
    created = _create(client).get_json()
    resp = client.put(
        f"/api/questions/{created['id']}",
        json=make_payload(question="Updated", correct="C"),
    )
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["question"] == "Updated"
    assert body["correct"] == "C"


def test_delete_removes_question(client):
    created = _create(client).get_json()
    resp = client.delete(f"/api/questions/{created['id']}")
    assert resp.status_code == 204

    assert client.get(f"/api/questions/{created['id']}").status_code == 404


# --- failure paths -----------------------------------------------------------


def test_create_invalid_payload_returns_400_with_fields(client):
    resp = _create(client, question="", correct="Z")
    assert resp.status_code == 400
    body = resp.get_json()
    assert "fields" in body
    assert "question" in body["fields"]
    assert "correct" in body["fields"]


def test_create_non_json_returns_400(client):
    resp = client.post("/api/questions", data="not json", content_type="text/plain")
    assert resp.status_code == 400


def test_get_missing_question_returns_404(client):
    assert client.get("/api/questions/9999").status_code == 404


def test_update_missing_question_returns_404(client):
    resp = client.put("/api/questions/9999", json=make_payload())
    assert resp.status_code == 404


def test_delete_missing_question_returns_404(client):
    assert client.delete("/api/questions/9999").status_code == 404
