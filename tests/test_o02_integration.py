"""o02 integration-style tests."""

from __future__ import annotations


def _q(client, text: str) -> int:
    return client.post(
        "/api/questions",
        json={
            "question": text,
            "a": "1",
            "b": "2",
            "c": "3",
            "d": "4",
            "correct": "B",
            "difficulty": "Medium",
        },
    ).get_json()["id"]


def test_quiz_builder_end_to_end(client):
    ids = [_q(client, f"Item {i}") for i in range(4)]
    created = client.post(
        "/api/quizzes",
        json={"name": "Sample Quiz", "question_ids": ids[:3]},
    )
    assert created.status_code == 201
    quiz_id = created.get_json()["id"]

    # reorder and expand
    updated = client.put(
        f"/api/quizzes/{quiz_id}",
        json={"name": "Sample Quiz", "question_ids": [ids[2], ids[0], ids[1], ids[3]]},
    )
    assert [q["id"] for q in updated.get_json()["questions"]] == [
        ids[2],
        ids[0],
        ids[1],
        ids[3],
    ]

    # deleting a question cascades out of quiz_questions
    assert client.delete(f"/api/questions/{ids[2]}").status_code == 204
    detail = client.get(f"/api/quizzes/{quiz_id}").get_json()
    assert ids[2] not in detail["question_ids"]
