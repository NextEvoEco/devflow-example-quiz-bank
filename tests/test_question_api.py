"""Question Bank API integration tests."""

from __future__ import annotations


def _payload(**overrides):
    data = {
        "question": "What is 2+2?",
        "a": "3",
        "b": "4",
        "c": "5",
        "d": "6",
        "correct": "B",
        "difficulty": "Easy",
    }
    data.update(overrides)
    return data


def test_question_api_crud_and_search(client):
    create = client.post("/api/questions", json=_payload(question="Find Paris"))
    assert create.status_code == 201
    body = create.get_json()
    qid = body["id"]
    assert body["difficulty"] == "Easy"

    listed = client.get("/api/questions")
    assert listed.status_code == 200
    assert len(listed.get_json()) == 1

    searched = client.get("/api/questions?q=paris")
    assert len(searched.get_json()) == 1
    assert client.get("/api/questions?q=zzz").get_json() == []

    updated = client.put(
        f"/api/questions/{qid}",
        json=_payload(question="Find Paris?", difficulty="Hard"),
    )
    assert updated.status_code == 200
    assert updated.get_json()["difficulty"] == "Hard"

    deleted = client.delete(f"/api/questions/{qid}")
    assert deleted.status_code == 204
    assert client.get("/api/questions").get_json() == []


def test_question_api_validation_and_not_found(client):
    bad = client.post("/api/questions", json=_payload(question=""))
    assert bad.status_code == 400
    assert "error" in bad.get_json()

    missing = client.get("/api/questions/999999")
    assert missing.status_code == 404

    delete_missing = client.delete("/api/questions/999999")
    assert delete_missing.status_code == 404


def test_question_api_defaults_difficulty(client):
    data = _payload()
    del data["difficulty"]
    response = client.post("/api/questions", json=data)
    assert response.status_code == 201
    assert response.get_json()["difficulty"] == "Medium"
