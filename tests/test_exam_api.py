import pytest

from backend.app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app(db_path=tmp_path / "exam_api.db")
    app.config.update(TESTING=True)
    return app.test_client()


@pytest.fixture
def quiz(client):
    """Seed 3 questions (correct A/B/C) and a quiz over them. Returns (quiz_id, [question_ids])."""
    ids = []
    for i, correct in enumerate(["A", "B", "C"]):
        r = client.post(
            "/api/questions",
            json={
                "question": f"Question {i}?",
                "a": "opt A", "b": "opt B", "c": "opt C", "d": "opt D",
                "correct": correct, "difficulty": "Easy",
            },
        )
        ids.append(r.get_json()["id"])
    quiz_id = client.post("/api/quizzes", json={"name": "Exam Quiz", "questionIds": ids}).get_json()["id"]
    return quiz_id, ids


def start_attempt(client, quiz_id):
    return client.post("/api/exams/attempts", json={"quiz_id": quiz_id}).get_json()["attempt_id"]


# --- create attempt ----------------------------------------------------------


def test_create_attempt_returns_201_and_id(client, quiz):
    quiz_id, _ = quiz
    resp = client.post("/api/exams/attempts", json={"quiz_id": quiz_id})
    assert resp.status_code == 201
    body = resp.get_json()
    assert isinstance(body["attempt_id"], int)
    # No correct answers leaked at creation.
    assert "correct" not in resp.get_data(as_text=True)


def test_create_attempt_invalid_quiz_returns_404(client):
    assert client.post("/api/exams/attempts", json={"quiz_id": 9999}).status_code == 404


def test_create_attempt_missing_quiz_id_returns_400(client):
    assert client.post("/api/exams/attempts", json={}).status_code == 400


# --- save answer -------------------------------------------------------------


def test_save_answer_returns_204(client, quiz):
    quiz_id, ids = quiz
    attempt_id = start_attempt(client, quiz_id)
    resp = client.put(
        f"/api/exams/attempts/{attempt_id}/answers/{ids[0]}",
        json={"selected_option": "A"},
    )
    assert resp.status_code == 204


def test_save_answer_invalid_attempt_returns_404(client, quiz):
    _, ids = quiz
    resp = client.put(
        f"/api/exams/attempts/9999/answers/{ids[0]}", json={"selected_option": "A"}
    )
    assert resp.status_code == 404


def test_save_answer_invalid_option_returns_400(client, quiz):
    quiz_id, ids = quiz
    attempt_id = start_attempt(client, quiz_id)
    resp = client.put(
        f"/api/exams/attempts/{attempt_id}/answers/{ids[0]}",
        json={"selected_option": "Z"},
    )
    assert resp.status_code == 400


def test_save_answer_question_not_in_quiz_returns_404(client, quiz):
    quiz_id, _ = quiz
    attempt_id = start_attempt(client, quiz_id)
    resp = client.put(
        f"/api/exams/attempts/{attempt_id}/answers/9999",
        json={"selected_option": "A"},
    )
    assert resp.status_code == 404


def test_save_answer_can_be_updated(client, quiz):
    quiz_id, ids = quiz
    attempt_id = start_attempt(client, quiz_id)
    client.put(f"/api/exams/attempts/{attempt_id}/answers/{ids[0]}", json={"selected_option": "A"})
    client.put(f"/api/exams/attempts/{attempt_id}/answers/{ids[0]}", json={"selected_option": "D"})
    # Submit and confirm the latest answer was scored.
    summary = client.post(f"/api/exams/attempts/{attempt_id}/submit").get_json()
    first = next(a for a in summary["answers"] if a["question_id"] == ids[0])
    assert first["selected_option"] == "D"


# --- submit ------------------------------------------------------------------


def test_submit_scores_correctly(client, quiz):
    quiz_id, ids = quiz  # correct answers: A, B, C
    attempt_id = start_attempt(client, quiz_id)
    client.put(f"/api/exams/attempts/{attempt_id}/answers/{ids[0]}", json={"selected_option": "A"})  # correct
    client.put(f"/api/exams/attempts/{attempt_id}/answers/{ids[1]}", json={"selected_option": "B"})  # correct
    client.put(f"/api/exams/attempts/{attempt_id}/answers/{ids[2]}", json={"selected_option": "A"})  # wrong

    resp = client.post(f"/api/exams/attempts/{attempt_id}/submit")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["score"] == 2
    assert body["total"] == 3
    assert body["percentage"] == 67  # round(2/3*100)
    assert len(body["answers"]) == 3

    review = {a["question_id"]: a for a in body["answers"]}
    assert review[ids[0]]["is_correct"] is True
    assert review[ids[2]]["is_correct"] is False
    assert review[ids[2]]["correct_option"] == "C"
    assert "question_text" in review[ids[0]]
    assert review[ids[0]]["options"]["A"] == "opt A"


def test_submit_counts_unanswered_as_wrong(client, quiz):
    quiz_id, ids = quiz
    attempt_id = start_attempt(client, quiz_id)
    client.put(f"/api/exams/attempts/{attempt_id}/answers/{ids[0]}", json={"selected_option": "A"})
    # ids[1], ids[2] left unanswered
    body = client.post(f"/api/exams/attempts/{attempt_id}/submit").get_json()
    assert body["score"] == 1
    review = {a["question_id"]: a for a in body["answers"]}
    assert review[ids[1]]["selected_option"] is None
    assert review[ids[1]]["is_correct"] is False


def test_submit_already_submitted_returns_409(client, quiz):
    quiz_id, _ = quiz
    attempt_id = start_attempt(client, quiz_id)
    assert client.post(f"/api/exams/attempts/{attempt_id}/submit").status_code == 200
    assert client.post(f"/api/exams/attempts/{attempt_id}/submit").status_code == 409


def test_submit_invalid_attempt_returns_404(client):
    assert client.post("/api/exams/attempts/9999/submit").status_code == 404


# --- V1/V2 regression --------------------------------------------------------


def test_question_and_quiz_apis_unaffected(client, quiz):
    quiz_id, _ = quiz
    assert client.get("/api/questions").status_code == 200
    assert len(client.get("/api/questions").get_json()) == 3
    assert client.get(f"/api/quizzes/{quiz_id}").status_code == 200
