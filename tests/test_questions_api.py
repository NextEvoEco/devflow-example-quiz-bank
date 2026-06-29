import json
from pathlib import Path

import pytest

from backend.app import create_app
from backend.database import initialize_database


@pytest.fixture
def client(tmp_path: Path):
    db_path = tmp_path / "quiz_bank.db"
    initialize_database(db_path)
    app = create_app(db_path)
    return app.test_client()


def sample_payload(**overrides) -> dict[str, str]:
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


def test_list_questions_returns_empty_collection(client) -> None:
    response = client.get("/api/questions")

    assert response.status_code == 200
    assert response.get_json() == {"questions": []}


def test_create_list_search_update_and_delete_flow(client) -> None:
    create_response = client.post(
        "/api/questions",
        data=json.dumps(sample_payload(question="Capital of France?")),
        content_type="application/json",
    )
    assert create_response.status_code == 201
    created = create_response.get_json()
    assert created["difficulty"] == "Medium"

    second_response = client.post(
        "/api/questions",
        data=json.dumps(sample_payload(question="Largest planet?", correct="C", difficulty="Hard")),
        content_type="application/json",
    )
    assert second_response.status_code == 201
    second = second_response.get_json()

    list_response = client.get("/api/questions")
    assert list_response.status_code == 200
    assert len(list_response.get_json()["questions"]) == 2

    search_response = client.get("/api/questions?q=planet")
    assert search_response.status_code == 200
    search_results = search_response.get_json()["questions"]
    assert len(search_results) == 1
    assert search_results[0]["id"] == second["id"]

    get_response = client.get(f"/api/questions/{created['id']}")
    assert get_response.status_code == 200
    assert get_response.get_json()["question"] == "Capital of France?"

    update_response = client.put(
        f"/api/questions/{created['id']}",
        data=json.dumps({"question": "Capital of France in Europe?", "difficulty": "Easy"}),
        content_type="application/json",
    )
    assert update_response.status_code == 200
    updated = update_response.get_json()
    assert updated["question"] == "Capital of France in Europe?"
    assert updated["difficulty"] == "Easy"

    delete_response = client.delete(f"/api/questions/{created['id']}")
    assert delete_response.status_code == 204

    missing_response = client.get(f"/api/questions/{created['id']}")
    assert missing_response.status_code == 404
    assert "error" in missing_response.get_json()


def test_create_with_invalid_payload_returns_validation_error(client) -> None:
    response = client.post(
        "/api/questions",
        data=json.dumps(sample_payload(question="")),
        content_type="application/json",
    )

    assert response.status_code == 400
    payload = response.get_json()
    assert payload["field"] == "question"
    assert "error" in payload


def test_create_with_invalid_json_returns_error(client) -> None:
    response = client.post(
        "/api/questions",
        data="not-json",
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Request body must be valid JSON."


def test_update_missing_question_returns_not_found(client) -> None:
    response = client.put(
        "/api/questions/999",
        data=json.dumps({"question": "Missing"}),
        content_type="application/json",
    )

    assert response.status_code == 404
    assert "error" in response.get_json()


def test_delete_missing_question_returns_not_found(client) -> None:
    response = client.delete("/api/questions/999")

    assert response.status_code == 404
    assert "error" in response.get_json()
