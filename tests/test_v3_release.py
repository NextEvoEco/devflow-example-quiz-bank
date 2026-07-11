"""O03 Online Exam V3 release verification checks."""

import sqlite3


def valid_question_payload(**overrides):
    payload = {
        "question": "O03 release question",
        "a": "One",
        "b": "Two",
        "c": "Three",
        "d": "Four",
        "correct": "B",
        "difficulty": "Easy",
    }
    payload.update(overrides)
    return payload


def quiz_payload(name="Release Exam Quiz", question_ids=None):
    return {
        "name": name,
        "questionIds": question_ids or [],
    }


def create_questions(client, count=3):
    correct_answers = ["A", "B", "C"]
    question_ids = []
    for index in range(count):
        response = client.post(
            "/api/questions",
            json=valid_question_payload(
                question=f"O03 question {index + 1}",
                correct=correct_answers[index % 3],
            ),
        )
        assert response.status_code == 201
        question_ids.append(response.get_json()["question"]["id"])
    return question_ids


def create_quiz(client, question_ids):
    response = client.post(
        "/api/quizzes",
        json=quiz_payload(question_ids=question_ids),
    )
    assert response.status_code == 201
    return response.get_json()["quiz"]["id"]


def test_v3_app_starts_and_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_v3_sqlite_schema_includes_exam_tables(db_paths):
    _, db_path = db_paths

    with sqlite3.connect(db_path) as connection:
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }

    assert "exam_attempts" in tables
    assert "exam_answers" in tables
    assert "quizzes" in tables
    assert "questions" in tables


def test_v3_exam_api_full_flow_and_scoring(client):
    question_ids = create_questions(client, 3)
    quiz_id = create_quiz(client, question_ids)

    attempt_response = client.post("/api/exams/attempts", json={"quiz_id": quiz_id})
    assert attempt_response.status_code == 201
    attempt_id = attempt_response.get_json()["attempt_id"]

    client.put(
        f"/api/exams/attempts/{attempt_id}/answers/{question_ids[0]}",
        json={"selected_option": "A"},
    )
    client.put(
        f"/api/exams/attempts/{attempt_id}/answers/{question_ids[1]}",
        json={"selected_option": "B"},
    )
    client.put(
        f"/api/exams/attempts/{attempt_id}/answers/{question_ids[2]}",
        json={"selected_option": "C"},
    )

    submit_response = client.post(f"/api/exams/attempts/{attempt_id}/submit")
    assert submit_response.status_code == 200
    body = submit_response.get_json()
    assert body["score"] == 3
    assert body["total"] == 3
    assert body["percentage"] == 100
    assert len(body["answers"]) == 3
    assert all("question_text" in answer for answer in body["answers"])


def test_v3_abandoned_attempt_remains_unscored(db_paths, client):
    question_ids = create_questions(client, 3)
    quiz_id = create_quiz(client, question_ids)

    attempt_response = client.post("/api/exams/attempts", json={"quiz_id": quiz_id})
    attempt_id = attempt_response.get_json()["attempt_id"]

    _, db_path = db_paths
    with sqlite3.connect(db_path) as connection:
        row = connection.execute(
            "SELECT score, submitted_at FROM exam_attempts WHERE id = ?",
            (attempt_id,),
        ).fetchone()

    assert row[0] is None
    assert row[1] is None


def test_v3_double_submit_returns_conflict(client):
    question_ids = create_questions(client, 3)
    quiz_id = create_quiz(client, question_ids)

    attempt_id = client.post(
        "/api/exams/attempts",
        json={"quiz_id": quiz_id},
    ).get_json()["attempt_id"]

    first_submit = client.post(f"/api/exams/attempts/{attempt_id}/submit")
    assert first_submit.status_code == 200

    second_submit = client.post(f"/api/exams/attempts/{attempt_id}/submit")
    assert second_submit.status_code == 409


def test_v3_question_bank_regression_baseline(client):
    create_response = client.post("/api/questions", json=valid_question_payload())
    assert create_response.status_code == 201
    question_id = create_response.get_json()["question"]["id"]

    search_response = client.get("/api/questions?q=release")
    assert search_response.status_code == 200
    assert len(search_response.get_json()["questions"]) == 1

    delete_response = client.delete(f"/api/questions/{question_id}")
    assert delete_response.status_code == 204


def test_v3_quiz_builder_regression_baseline(client):
    question_ids = create_questions(client, 3)

    create_response = client.post(
        "/api/quizzes",
        json=quiz_payload(question_ids=question_ids),
    )
    assert create_response.status_code == 201
    quiz_id = create_response.get_json()["quiz"]["id"]

    get_response = client.get(f"/api/quizzes/{quiz_id}")
    assert get_response.status_code == 200
    assert get_response.get_json()["quiz"]["questionCount"] == 3


def test_v3_frontend_online_exam_pages_are_available(client):
    response = client.get("/")
    assert response.status_code == 200

    html = response.get_data(as_text=True)
    assert 'data-nav-page="exams"' in html
    assert 'id="exams-page"' in html
    assert 'id="exam-taking-page"' in html
    assert 'id="exam-results-page"' in html
    assert "Available Exams" in html
    assert "Answer Review" in html


def test_v3_frontend_assets_include_online_exam_flow(client):
    js_response = client.get("/js/questions.js")
    api_response = client.get("/js/api.js")

    assert js_response.status_code == 200
    assert api_response.status_code == 200
    assert b"ExamListPage" in js_response.data
    assert b"ExamTakingPage" in js_response.data
    assert b"ExamResultsPage" in js_response.data
    assert b"createExamAttempt" in api_response.data
    assert b"submitExamAttempt" in api_response.data


def test_v3_exam_attempt_endpoints_are_available(client):
    question_ids = create_questions(client, 3)
    quiz_id = create_quiz(client, question_ids)

    create_response = client.post("/api/exams/attempts", json={"quiz_id": quiz_id})
    assert create_response.status_code == 201
    assert "attempt_id" in create_response.get_json()

    assert client.get("/api/exams").status_code == 404
