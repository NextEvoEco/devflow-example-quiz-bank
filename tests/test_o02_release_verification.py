"""O02 Quiz Builder release verification checks."""

import sqlite3


def valid_question_payload(**overrides):
    payload = {
        "question": "O02 release question",
        "a": "One",
        "b": "Two",
        "c": "Three",
        "d": "Four",
        "correct": "B",
        "difficulty": "Easy",
    }
    payload.update(overrides)
    return payload


def quiz_payload(name="Release Quiz", question_ids=None):
    return {
        "name": name,
        "questionIds": question_ids or [],
    }


def create_questions(client, count=3):
    question_ids = []
    for index in range(count):
        response = client.post(
            "/api/questions",
            json=valid_question_payload(question=f"O02 question {index + 1}"),
        )
        assert response.status_code == 201
        question_ids.append(response.get_json()["question"]["id"])
    return question_ids


def test_o2_app_starts_and_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_o2_sqlite_schema_includes_quiz_tables(db_paths):
    _, db_path = db_paths

    with sqlite3.connect(db_path) as connection:
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }

    assert "quizzes" in tables
    assert "quiz_questions" in tables
    assert "questions" in tables


def test_o2_quiz_api_full_flow_and_min_validation(client):
    question_ids = create_questions(client, 3)

    too_few_response = client.post(
        "/api/quizzes",
        json=quiz_payload(name="Too Short", question_ids=question_ids[:2]),
    )
    assert too_few_response.status_code == 400
    assert "questionIds" in too_few_response.get_json()["errors"]

    create_response = client.post(
        "/api/quizzes",
        json=quiz_payload(question_ids=question_ids),
    )
    assert create_response.status_code == 201
    quiz_id = create_response.get_json()["quiz"]["id"]

    list_response = client.get("/api/quizzes")
    assert list_response.status_code == 200
    assert len(list_response.get_json()["quizzes"]) == 1

    get_response = client.get(f"/api/quizzes/{quiz_id}")
    assert get_response.status_code == 200
    quiz = get_response.get_json()["quiz"]
    assert quiz["questionCount"] == 3
    assert [question["id"] for question in quiz["questions"]] == question_ids

    reordered_ids = [question_ids[2], question_ids[0], question_ids[1]]
    update_response = client.put(
        f"/api/quizzes/{quiz_id}",
        json=quiz_payload(name="Updated Release Quiz", question_ids=reordered_ids),
    )
    assert update_response.status_code == 200
    updated = update_response.get_json()["quiz"]
    assert updated["name"] == "Updated Release Quiz"
    assert [question["id"] for question in updated["questions"]] == reordered_ids

    delete_response = client.delete(f"/api/quizzes/{quiz_id}")
    assert delete_response.status_code == 204
    assert client.get("/api/quizzes").get_json()["quizzes"] == []


def test_o2_question_bank_regression_baseline(client):
    create_response = client.post("/api/questions", json=valid_question_payload())
    assert create_response.status_code == 201
    question_id = create_response.get_json()["question"]["id"]

    search_response = client.get("/api/questions?q=release")
    assert search_response.status_code == 200
    assert len(search_response.get_json()["questions"]) == 1

    update_response = client.put(
        f"/api/questions/{question_id}",
        json=valid_question_payload(question="Updated O02 question"),
    )
    assert update_response.status_code == 200

    delete_response = client.delete(f"/api/questions/{question_id}")
    assert delete_response.status_code == 204


def test_o2_frontend_quiz_builder_pages_are_available(client):
    response = client.get("/")
    assert response.status_code == 200

    html = response.get_data(as_text=True)
    assert 'id="quizzes-page"' in html
    assert 'id="quiz-builder-page"' in html
    assert 'id="quiz-preview-page"' in html
    assert 'data-nav-page="quizzes"' in html


def test_o2_frontend_assets_include_quiz_builder_flow(client):
    js_response = client.get("/js/questions.js")
    api_response = client.get("/js/api.js")

    assert js_response.status_code == 200
    assert api_response.status_code == 200
    assert b"QuizListPage" in js_response.data
    assert b"QuizBuilderPage" in js_response.data
    assert b"QuizPreviewPage" in js_response.data
    assert b"createQuiz" in api_response.data
    assert b"getQuiz" in api_response.data


def test_o2_exams_api_remains_out_of_scope(client):
    assert client.get("/api/exams").status_code == 404


def test_o2_online_exam_navigation_remains_disabled(client):
    response = client.get("/")
    html = response.get_data(as_text=True)

    assert "Online Exam" in html
    assert 'data-nav-page="exams"' in html
    assert 'href="#exams"' in html


def test_o2_quiz_builder_navigation_is_enabled(client):
    response = client.get("/")
    html = response.get_data(as_text=True)

    assert 'data-nav-page="quizzes"' in html
    assert 'href="#quizzes"' in html


def test_o2_online_exam_navigation_is_enabled(client):
    response = client.get("/")
    html = response.get_data(as_text=True)

    assert 'data-nav-page="exams"' in html
    assert 'href="#exams"' in html
    assert 'id="exams-page"' in html
