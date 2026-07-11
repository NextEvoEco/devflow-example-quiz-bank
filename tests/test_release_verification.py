"""V1 release verification checks for the Question Bank baseline."""

import sqlite3

from backend.question_repository import QuestionRepository


def valid_question_payload(**overrides):
    payload = {
        "question": "Release verification question",
        "a": "One",
        "b": "Two",
        "c": "Three",
        "d": "Four",
        "correct": "B",
        "difficulty": "Easy",
    }
    payload.update(overrides)
    return payload


def test_v1_app_starts_and_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_v1_sqlite_schema_is_initialized(db_paths):
    data_dir, db_path = db_paths

    with sqlite3.connect(db_path) as connection:
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }

    assert "schema_migrations" in tables
    assert "questions" in tables


def test_v1_question_bank_crud_and_search_baseline(client):
    create_response = client.post("/api/questions", json=valid_question_payload())
    assert create_response.status_code == 201
    question_id = create_response.get_json()["question"]["id"]

    list_response = client.get("/api/questions")
    assert list_response.status_code == 200
    assert len(list_response.get_json()["questions"]) == 1

    search_response = client.get("/api/questions?q=verification")
    assert search_response.status_code == 200
    assert len(search_response.get_json()["questions"]) == 1

    update_response = client.put(
        f"/api/questions/{question_id}",
        json=valid_question_payload(question="Updated release question", difficulty="Hard"),
    )
    assert update_response.status_code == 200
    updated = update_response.get_json()["question"]
    assert updated["question"] == "Updated release question"
    assert updated["difficulty"] == "Hard"

    delete_response = client.delete(f"/api/questions/{question_id}")
    assert delete_response.status_code == 204
    assert client.get("/api/questions").get_json()["questions"] == []


def test_v1_validation_rejects_invalid_question(client):
    response = client.post(
        "/api/questions",
        json=valid_question_payload(question="", correct="Z"),
    )
    assert response.status_code == 400
    body = response.get_json()
    assert body["errors"]["question"]
    assert body["errors"]["correct"]


def test_v1_default_difficulty_is_applied(client):
    payload = valid_question_payload()
    del payload["difficulty"]

    response = client.post("/api/questions", json=payload)
    assert response.status_code == 201
    assert response.get_json()["question"]["difficulty"] == "Medium"


def test_v1_sqlite_persistence_through_repository(db_paths):
    repository = QuestionRepository()
    created = repository.create(valid_question_payload(question="Persisted question"))

    reloaded = QuestionRepository().get_by_id(created["id"])
    assert reloaded is not None
    assert reloaded["question"] == "Persisted question"


def test_v1_frontend_question_bank_page_is_available(client):
    response = client.get("/")
    assert response.status_code == 200

    html = response.get_data(as_text=True)
    assert 'id="questions-page"' in html
    assert 'id="question-editor-modal"' in html
    assert 'id="delete-question-modal"' in html


def test_v1_out_of_scope_api_routes_are_not_implemented(client):
    assert client.get("/api/exams").status_code == 404


def test_v1_online_exam_navigation_remains_disabled(client):
    response = client.get("/")
    html = response.get_data(as_text=True)

    assert "Quiz Builder" in html
    assert "Online Exam" in html
    assert 'data-nav-page="exams"' in html


def test_v1_fresh_database_starts_without_seed_questions(client):
    response = client.get("/api/questions")
    assert response.status_code == 200
    assert response.get_json()["questions"] == []
