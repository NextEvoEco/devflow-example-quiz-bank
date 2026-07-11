from __future__ import annotations


def make_question_payload(index: int):
    return {
        "question": f"Question {index}?",
        "a": f"A{index}",
        "b": f"B{index}",
        "c": f"C{index}",
        "d": f"D{index}",
        "correct": "A",
        "difficulty": "Easy",
    }


def seed_question_ids(client, count: int = 3) -> list[int]:
    question_ids = []
    for index in range(1, count + 1):
        response = client.post("/api/questions", json=make_question_payload(index))
        question_ids.append(response.get_json()["id"])
    return question_ids


def test_create_quiz_returns_201(client):
    question_ids = seed_question_ids(client, 3)

    response = client.post(
        "/api/quizzes",
        json={"name": "Starter Quiz", "questionIds": question_ids},
    )

    assert response.status_code == 201
    payload = response.get_json()
    assert payload["name"] == "Starter Quiz"
    assert payload["questionIds"] == question_ids
    assert len(payload["questions"]) == 3


def test_create_quiz_rejects_fewer_than_three_questions(client):
    question_ids = seed_question_ids(client, 2)

    response = client.post(
        "/api/quizzes",
        json={"name": "Too Small", "questionIds": question_ids},
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "A quiz must contain at least 3 questions"


def test_create_quiz_rejects_missing_question_ids(client):
    question_ids = seed_question_ids(client, 3)
    question_ids[-1] = 999

    response = client.post(
        "/api/quizzes",
        json={"name": "Broken Quiz", "questionIds": question_ids},
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Question IDs do not exist: 999"


def test_create_quiz_rejects_duplicate_question_ids(client):
    question_ids = seed_question_ids(client, 3)

    response = client.post(
        "/api/quizzes",
        json={"name": "Duplicate Quiz", "questionIds": [question_ids[0], question_ids[0], question_ids[1]]},
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "A quiz cannot contain duplicate question IDs"


def test_list_quizzes_returns_quiz_summaries(client):
    question_ids = seed_question_ids(client, 3)
    client.post("/api/quizzes", json={"name": "Starter Quiz", "questionIds": question_ids})

    response = client.get("/api/quizzes")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["items"][0]["name"] == "Starter Quiz"
    assert payload["items"][0]["questionCount"] == 3


def test_get_quiz_returns_ordered_question_details(client):
    question_ids = seed_question_ids(client, 3)
    ordered_ids = [question_ids[2], question_ids[0], question_ids[1]]
    created = client.post(
        "/api/quizzes",
        json={"name": "Ordered Quiz", "questionIds": ordered_ids},
    )
    quiz_id = created.get_json()["id"]

    response = client.get(f"/api/quizzes/{quiz_id}")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["questionIds"] == ordered_ids
    assert [question["id"] for question in payload["questions"]] == ordered_ids


def test_update_quiz_replaces_name_and_question_order(client):
    original_ids = seed_question_ids(client, 4)
    created = client.post(
        "/api/quizzes",
        json={"name": "Starter Quiz", "questionIds": original_ids[:3]},
    )
    quiz_id = created.get_json()["id"]

    response = client.put(
        f"/api/quizzes/{quiz_id}",
        json={"name": "Updated Quiz", "questionIds": [original_ids[3], original_ids[1], original_ids[0]]},
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["name"] == "Updated Quiz"
    assert payload["questionIds"] == [original_ids[3], original_ids[1], original_ids[0]]


def test_delete_quiz_removes_quiz_and_references(client):
    question_ids = seed_question_ids(client, 3)
    created = client.post(
        "/api/quizzes",
        json={"name": "Delete Me", "questionIds": question_ids},
    )
    quiz_id = created.get_json()["id"]

    delete_response = client.delete(f"/api/quizzes/{quiz_id}")
    get_response = client.get(f"/api/quizzes/{quiz_id}")

    assert delete_response.status_code == 200
    assert delete_response.get_json() == {"deleted": True, "id": quiz_id}
    assert get_response.status_code == 404
    assert get_response.get_json()["error"] == f"Quiz {quiz_id} not found"
