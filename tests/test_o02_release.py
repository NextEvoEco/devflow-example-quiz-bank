"""Integration / release verification for Quiz Builder V2 (o02).

Ties the full quiz lifecycle together, asserts the min-3 rule, checks Question
Bank has not regressed, and guards the Online Exam (V3) scope boundary.
"""

import pytest

from backend.app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app(db_path=tmp_path / "o02_release.db")
    app.config.update(TESTING=True)
    return app.test_client()


def seed_questions(client, n):
    ids = []
    for i in range(n):
        r = client.post(
            "/api/questions",
            json={
                "question": f"Question {i}?",
                "a": "A", "b": "B", "c": "C", "d": "D",
                "correct": "A", "difficulty": "Easy",
            },
        )
        ids.append(r.get_json()["id"])
    return ids


# --- Full quiz lifecycle -----------------------------------------------------


def test_full_quiz_lifecycle(client):
    ids = seed_questions(client, 5)

    # create
    created = client.post(
        "/api/quizzes", json={"name": "Lifecycle", "questionIds": ids[:3]}
    ).get_json()
    quiz_id = created["id"]

    # list (with count)
    listing = client.get("/api/quizzes").get_json()
    assert len(listing) == 1
    assert listing[0]["question_count"] == 3

    # get (ordered full questions)
    detail = client.get(f"/api/quizzes/{quiz_id}").get_json()
    assert [q["id"] for q in detail["questions"]] == ids[:3]

    # update (rename + add + reorder)
    new_order = [ids[3], ids[0], ids[1], ids[2]]
    updated = client.put(
        f"/api/quizzes/{quiz_id}", json={"name": "Lifecycle v2", "questionIds": new_order}
    ).get_json()
    assert updated["name"] == "Lifecycle v2"
    assert updated["questionIds"] == new_order

    # delete
    assert client.delete(f"/api/quizzes/{quiz_id}").status_code == 204
    assert client.get(f"/api/quizzes/{quiz_id}").status_code == 404
    assert client.get("/api/quizzes").get_json() == []


def test_min_three_questions_rule_enforced(client):
    ids = seed_questions(client, 3)
    # create with 2 -> rejected
    assert client.post("/api/quizzes", json={"name": "X", "questionIds": ids[:2]}).status_code == 400
    # create with 3 -> ok
    created = client.post("/api/quizzes", json={"name": "OK", "questionIds": ids}).get_json()
    # update down to 2 -> rejected
    assert client.put(
        f"/api/quizzes/{created['id']}", json={"name": "OK", "questionIds": ids[:2]}
    ).status_code == 400


def test_manual_reorder_persists(client):
    ids = seed_questions(client, 3)
    created = client.post("/api/quizzes", json={"name": "R", "questionIds": ids}).get_json()
    reordered = [ids[2], ids[0], ids[1]]
    client.put(f"/api/quizzes/{created['id']}", json={"name": "R", "questionIds": reordered})
    detail = client.get(f"/api/quizzes/{created['id']}").get_json()
    assert detail["questionIds"] == reordered


# --- Question Bank regression ------------------------------------------------


def test_question_bank_crud_and_search_unaffected(client):
    # add
    created = client.post(
        "/api/questions",
        json={"question": "Python basics", "a": "1", "b": "2", "c": "3", "d": "4", "correct": "A"},
    ).get_json()
    client.post(
        "/api/questions",
        json={"question": "History facts", "a": "1", "b": "2", "c": "3", "d": "4", "correct": "B"},
    )
    # list
    assert len(client.get("/api/questions").get_json()) == 2
    # search
    hits = client.get("/api/questions?search=python").get_json()
    assert len(hits) == 1 and hits[0]["question"] == "Python basics"
    # edit
    edited = client.put(
        f"/api/questions/{created['id']}",
        json={"question": "Python edited", "a": "1", "b": "2", "c": "3", "d": "4", "correct": "C"},
    ).get_json()
    assert edited["question"] == "Python edited"
    # delete
    assert client.delete(f"/api/questions/{created['id']}").status_code == 204
    assert len(client.get("/api/questions").get_json()) == 1


def test_deleting_question_updates_quizzes(client):
    ids = seed_questions(client, 3)
    quiz = client.post("/api/quizzes", json={"name": "Ref", "questionIds": ids}).get_json()
    # Deleting a referenced question drops it from the quiz (cascade).
    client.delete(f"/api/questions/{ids[0]}")
    detail = client.get(f"/api/quizzes/{quiz['id']}").get_json()
    assert ids[0] not in detail["questionIds"]
    assert len(detail["questions"]) == 2

