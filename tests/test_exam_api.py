import pytest


@pytest.fixture
def quiz_with_questions(client):
    question_ids = []
    correct_answers = ["A", "B", "C"]
    for index, correct in enumerate(correct_answers):
        response = client.post(
            "/api/questions",
            json={
                "question": f"Exam API question {index + 1}",
                "a": f"Option A {index + 1}",
                "b": f"Option B {index + 1}",
                "c": f"Option C {index + 1}",
                "d": f"Option D {index + 1}",
                "correct": correct,
            },
        )
        assert response.status_code == 201
        question_ids.append(response.get_json()["question"]["id"])

    quiz_response = client.post(
        "/api/quizzes",
        json={"name": "Exam API Quiz", "questionIds": question_ids},
    )
    assert quiz_response.status_code == 201
    quiz = quiz_response.get_json()["quiz"]
    return {
        "quiz_id": quiz["id"],
        "question_ids": question_ids,
        "correct_answers": correct_answers,
        "questions": quiz["questions"],
    }


def test_create_attempt_returns_attempt_id(client, quiz_with_questions):
    response = client.post(
        "/api/exams/attempts",
        json={"quiz_id": quiz_with_questions["quiz_id"]},
    )

    assert response.status_code == 201
    assert "attempt_id" in response.get_json()


def test_create_attempt_rejects_missing_quiz(client):
    response = client.post("/api/exams/attempts", json={"quiz_id": 9999})

    assert response.status_code == 404


def test_save_answer_returns_204(client, quiz_with_questions):
    attempt_id = client.post(
        "/api/exams/attempts",
        json={"quiz_id": quiz_with_questions["quiz_id"]},
    ).get_json()["attempt_id"]
    question_id = quiz_with_questions["question_ids"][0]

    response = client.put(
        f"/api/exams/attempts/{attempt_id}/answers/{question_id}",
        json={"selected_option": "A"},
    )

    assert response.status_code == 204
    assert response.data == b""


def test_save_answer_rejects_invalid_attempt(client, quiz_with_questions):
    question_id = quiz_with_questions["question_ids"][0]

    response = client.put(
        f"/api/exams/attempts/9999/answers/{question_id}",
        json={"selected_option": "A"},
    )

    assert response.status_code == 404


def test_save_answer_rejects_invalid_question(client, quiz_with_questions):
    attempt_id = client.post(
        "/api/exams/attempts",
        json={"quiz_id": quiz_with_questions["quiz_id"]},
    ).get_json()["attempt_id"]

    response = client.put(
        f"/api/exams/attempts/{attempt_id}/answers/9999",
        json={"selected_option": "A"},
    )

    assert response.status_code == 404


def test_submit_attempt_returns_score_summary(client, quiz_with_questions):
    attempt_id = client.post(
        "/api/exams/attempts",
        json={"quiz_id": quiz_with_questions["quiz_id"]},
    ).get_json()["attempt_id"]

    for question_id, correct in zip(
        quiz_with_questions["question_ids"],
        quiz_with_questions["correct_answers"],
    ):
        save_response = client.put(
            f"/api/exams/attempts/{attempt_id}/answers/{question_id}",
            json={"selected_option": correct},
        )
        assert save_response.status_code == 204

    response = client.post(f"/api/exams/attempts/{attempt_id}/submit")
    body = response.get_json()

    assert response.status_code == 200
    assert body["score"] == 3
    assert body["total"] == 3
    assert body["percentage"] == 100
    assert len(body["answers"]) == 3
    assert body["answers"][0]["question_text"] == "Exam API question 1"
    assert body["answers"][0]["a"] == "Option A 1"
    assert body["answers"][0]["is_correct"] is True


def test_submit_counts_unanswered_questions_as_incorrect(client, quiz_with_questions):
    attempt_id = client.post(
        "/api/exams/attempts",
        json={"quiz_id": quiz_with_questions["quiz_id"]},
    ).get_json()["attempt_id"]

    first_question_id = quiz_with_questions["question_ids"][0]
    client.put(
        f"/api/exams/attempts/{attempt_id}/answers/{first_question_id}",
        json={"selected_option": "A"},
    )

    response = client.post(f"/api/exams/attempts/{attempt_id}/submit")
    body = response.get_json()

    assert response.status_code == 200
    assert body["score"] == 1
    assert body["total"] == 3
    assert body["percentage"] == 33
    assert body["answers"][1]["selected_option"] is None
    assert body["answers"][1]["is_correct"] is False


def test_submit_already_submitted_attempt_returns_409(client, quiz_with_questions):
    attempt_id = client.post(
        "/api/exams/attempts",
        json={"quiz_id": quiz_with_questions["quiz_id"]},
    ).get_json()["attempt_id"]

    first_submit = client.post(f"/api/exams/attempts/{attempt_id}/submit")
    assert first_submit.status_code == 200

    second_submit = client.post(f"/api/exams/attempts/{attempt_id}/submit")
    assert second_submit.status_code == 409


def test_save_answer_on_submitted_attempt_returns_409(client, quiz_with_questions):
    attempt_id = client.post(
        "/api/exams/attempts",
        json={"quiz_id": quiz_with_questions["quiz_id"]},
    ).get_json()["attempt_id"]
    question_id = quiz_with_questions["question_ids"][0]

    submit_response = client.post(f"/api/exams/attempts/{attempt_id}/submit")
    assert submit_response.status_code == 200

    response = client.put(
        f"/api/exams/attempts/{attempt_id}/answers/{question_id}",
        json={"selected_option": "A"},
    )
    assert response.status_code == 409


def test_submit_missing_attempt_returns_404(client):
    response = client.post("/api/exams/attempts/9999/submit")

    assert response.status_code == 404
