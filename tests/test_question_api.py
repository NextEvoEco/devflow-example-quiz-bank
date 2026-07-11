from __future__ import annotations


def make_payload(**overrides):
    payload = {
        "question": "What is 2 + 2?",
        "a": "3",
        "b": "4",
        "c": "5",
        "d": "6",
        "correct": "B",
        "difficulty": "Easy",
    }
    payload.update(overrides)
    return payload


def test_list_questions_returns_created_items(client):
    created = client.post("/api/questions", json=make_payload())

    response = client.get("/api/questions")

    assert created.status_code == 201
    assert response.status_code == 200
    payload = response.get_json()
    assert len(payload["items"]) == 1
    assert payload["items"][0]["question"] == "What is 2 + 2?"


def test_search_questions_filters_by_query(client):
    client.post("/api/questions", json=make_payload(question="Capital of Taiwan?"))
    client.post(
        "/api/questions",
        json=make_payload(question="Largest ocean?", correct="A"),
    )

    response = client.get("/api/questions?q=capital")

    assert response.status_code == 200
    payload = response.get_json()
    assert [item["question"] for item in payload["items"]] == ["Capital of Taiwan?"]


def test_create_question_returns_default_difficulty_when_omitted(client):
    payload = make_payload()
    payload.pop("difficulty")

    response = client.post("/api/questions", json=payload)

    assert response.status_code == 201
    assert response.get_json()["difficulty"] == "Medium"


def test_create_question_rejects_invalid_payload(client):
    response = client.post("/api/questions", json=make_payload(question=""))

    assert response.status_code == 400
    assert response.get_json()["error"] == "'question' must be a non-empty string"


def test_update_question_returns_updated_item(client):
    created = client.post("/api/questions", json=make_payload())
    question_id = created.get_json()["id"]

    response = client.put(
        f"/api/questions/{question_id}",
        json=make_payload(question="What is 3 + 3?", b="6"),
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["id"] == question_id
    assert payload["question"] == "What is 3 + 3?"
    assert payload["b"] == "6"


def test_update_question_returns_404_for_missing_record(client):
    response = client.put("/api/questions/999", json=make_payload())

    assert response.status_code == 404
    assert response.get_json()["error"] == "Question 999 does not exist"


def test_delete_question_removes_item(client):
    created = client.post("/api/questions", json=make_payload())
    question_id = created.get_json()["id"]

    delete_response = client.delete(f"/api/questions/{question_id}")
    list_response = client.get("/api/questions")

    assert delete_response.status_code == 200
    assert delete_response.get_json() == {"deleted": True, "id": question_id}
    assert list_response.get_json()["items"] == []


def test_delete_question_returns_404_for_missing_record(client):
    response = client.delete("/api/questions/999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Question 999 not found"


def test_create_question_requires_json_object(client):
    response = client.post(
        "/api/questions",
        data="not-json",
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Request body must be a JSON object"
