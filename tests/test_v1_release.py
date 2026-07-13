"""V1 release verification tests."""

from __future__ import annotations


def test_v1_health_and_spa(client):
    assert client.get("/api/health").get_json()["status"] == "ok"
    assert b"id=\"app\"" in client.get("/").data or b"Quiz Bank" in client.get("/").data


def test_v1_question_flow(client):
    created = client.post(
        "/api/questions",
        json={
            "question": "Release check?",
            "a": "No",
            "b": "Yes",
            "c": "Maybe",
            "d": "Later",
            "correct": "B",
        },
    )
    assert created.status_code == 201
    assert created.get_json()["difficulty"] == "Medium"
    qid = created.get_json()["id"]

    assert any(q["id"] == qid for q in client.get("/api/questions").get_json())
    assert len(client.get("/api/questions?q=release").get_json()) == 1

    updated = client.put(
        f"/api/questions/{qid}",
        json={
            "question": "Release check updated?",
            "a": "No",
            "b": "Yes",
            "c": "Maybe",
            "d": "Later",
            "correct": "B",
            "difficulty": "Hard",
        },
    )
    assert updated.status_code == 200
    assert updated.get_json()["difficulty"] == "Hard"

    assert client.delete(f"/api/questions/{qid}").status_code == 204
    assert client.get("/api/questions").get_json() == []
