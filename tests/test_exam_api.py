from __future__ import annotations


def make_question_payload(index: int, correct: str = "A"):
    return {
        "question": f"Question {index}?",
        "a": f"A{index}",
        "b": f"B{index}",
        "c": f"C{index}",
        "d": f"D{index}",
        "correct": correct,
        "difficulty": "Easy",
    }


def seed_quiz(client) -> tuple[int, list[int]]:
    question_ids = []
    for index, correct in enumerate(["A", "B", "C"], start=1):
        response = client.post("/api/questions", json=make_question_payload(index, correct))
        question_ids.append(response.get_json()["id"])

    quiz_response = client.post(
        "/api/quizzes",
        json={"name": "Exam Ready Quiz", "questionIds": question_ids},
    )
    return quiz_response.get_json()["id"], question_ids


def test_create_attempt_returns_attempt_id(client):
    quiz_id, _ = seed_quiz(client)

    response = client.post("/api/exams/attempts", json={"quiz_id": quiz_id})

    assert response.status_code == 201
    assert isinstance(response.get_json()["attempt_id"], int)


def test_create_attempt_returns_404_for_missing_quiz(client):
    response = client.post("/api/exams/attempts", json={"quiz_id": 999})

    assert response.status_code == 404
    assert response.get_json()["error"] == "Quiz 999 not found"


def test_save_answer_returns_204(client):
    quiz_id, question_ids = seed_quiz(client)
    attempt_response = client.post("/api/exams/attempts", json={"quiz_id": quiz_id})
    attempt_id = attempt_response.get_json()["attempt_id"]

    response = client.put(
        f"/api/exams/attempts/{attempt_id}/answers/{question_ids[0]}",
        json={"selected_option": "A"},
    )

    assert response.status_code == 204
    assert response.data == b""


def test_save_answer_returns_404_for_missing_attempt(client):
    _, question_ids = seed_quiz(client)

    response = client.put(
        f"/api/exams/attempts/999/answers/{question_ids[0]}",
        json={"selected_option": "A"},
    )

    assert response.status_code == 404
    assert response.get_json()["error"] == "Attempt 999 not found"


def test_submit_attempt_returns_score_summary_and_answer_review(client):
    quiz_id, question_ids = seed_quiz(client)
    attempt_id = client.post("/api/exams/attempts", json={"quiz_id": quiz_id}).get_json()[
        "attempt_id"
    ]
    client.put(
        f"/api/exams/attempts/{attempt_id}/answers/{question_ids[0]}",
        json={"selected_option": "A"},
    )
    client.put(
        f"/api/exams/attempts/{attempt_id}/answers/{question_ids[1]}",
        json={"selected_option": "C"},
    )

    response = client.post(f"/api/exams/attempts/{attempt_id}/submit")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["attempt_id"] == attempt_id
    assert payload["quiz_id"] == quiz_id
    assert payload["score"] == 1
    assert payload["total"] == 3
    assert payload["percentage"] == 33
    assert payload["submitted_at"] is not None
    assert payload["answers"][0]["question_id"] == question_ids[0]
    assert payload["answers"][0]["selected_option"] == "A"
    assert payload["answers"][0]["correct_option"] == "A"
    assert payload["answers"][0]["is_correct"] is True
    assert payload["answers"][0]["question_text"] == "Question 1?"
    assert payload["answers"][0]["options"]["A"] == "A1"
    assert payload["answers"][1]["selected_option"] == "C"
    assert payload["answers"][1]["correct_option"] == "B"
    assert payload["answers"][1]["is_correct"] is False
    assert payload["answers"][2]["selected_option"] is None
    assert payload["answers"][2]["correct_option"] == "C"


def test_submit_attempt_returns_404_for_missing_attempt(client):
    response = client.post("/api/exams/attempts/999/submit")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Attempt 999 not found"


def test_submit_attempt_returns_409_when_already_submitted(client):
    quiz_id, question_ids = seed_quiz(client)
    attempt_id = client.post("/api/exams/attempts", json={"quiz_id": quiz_id}).get_json()[
        "attempt_id"
    ]
    client.put(
        f"/api/exams/attempts/{attempt_id}/answers/{question_ids[0]}",
        json={"selected_option": "A"},
    )

    first_submit = client.post(f"/api/exams/attempts/{attempt_id}/submit")
    second_submit = client.post(f"/api/exams/attempts/{attempt_id}/submit")

    assert first_submit.status_code == 200
    assert second_submit.status_code == 409
    assert second_submit.get_json()["error"] == (
        f"Attempt {attempt_id} has already been submitted"
    )
