import pytest

from backend.app import create_app


@pytest.fixture
def app(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    db_path = data_dir / "quiz_bank.db"
    monkeypatch.setattr("backend.config.DATA_DIR", data_dir)
    monkeypatch.setattr("backend.config.DATABASE_PATH", db_path)
    monkeypatch.setattr("backend.db.DATA_DIR", data_dir)
    monkeypatch.setattr("backend.db.DATABASE_PATH", db_path)

    application = create_app()
    application.config.update({"TESTING": True})
    return application


@pytest.fixture
def client(app):
    return app.test_client()


def valid_question_payload(**overrides):
    payload = {
        "question": "What is 2 + 2?",
        "a": "3",
        "b": "4",
        "c": "5",
        "d": "6",
        "correct": "B",
    }
    payload.update(overrides)
    return payload


def test_list_questions_empty(client):
    response = client.get("/api/questions")
    assert response.status_code == 200
    assert response.get_json() == {"questions": []}


def test_create_get_update_delete_question_flow(client):
    create_response = client.post("/api/questions", json=valid_question_payload())
    assert create_response.status_code == 201
    created = create_response.get_json()["question"]
    question_id = created["id"]
    assert created["difficulty"] == "Medium"

    get_response = client.get(f"/api/questions/{question_id}")
    assert get_response.status_code == 200
    assert get_response.get_json()["question"]["id"] == question_id

    update_response = client.put(
        f"/api/questions/{question_id}",
        json=valid_question_payload(question="Updated question", difficulty="Hard"),
    )
    assert update_response.status_code == 200
    assert update_response.get_json()["question"]["question"] == "Updated question"
    assert update_response.get_json()["question"]["difficulty"] == "Hard"

    delete_response = client.delete(f"/api/questions/{question_id}")
    assert delete_response.status_code == 204

    missing_response = client.get(f"/api/questions/{question_id}")
    assert missing_response.status_code == 404


def test_search_questions(client):
    client.post("/api/questions", json=valid_question_payload(question="Python basics"))
    client.post("/api/questions", json=valid_question_payload(question="Java basics"))

    response = client.get("/api/questions?q=python")
    assert response.status_code == 200
    questions = response.get_json()["questions"]
    assert len(questions) == 1
    assert questions[0]["question"] == "Python basics"


def test_create_question_rejects_invalid_payload(client):
    response = client.post(
        "/api/questions",
        json=valid_question_payload(question="", correct="Z"),
    )
    assert response.status_code == 400
    body = response.get_json()
    assert "errors" in body
    assert "question" in body["errors"]
    assert "correct" in body["errors"]


def test_update_missing_question_returns_404(client):
    response = client.put("/api/questions/999", json=valid_question_payload())
    assert response.status_code == 404


def test_delete_missing_question_returns_404(client):
    response = client.delete("/api/questions/999")
    assert response.status_code == 404
