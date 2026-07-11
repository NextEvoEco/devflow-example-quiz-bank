def quiz_payload(name="Sample Quiz", question_ids=None):
    return {
        "name": name,
        "questionIds": question_ids or [],
    }


def test_quiz_list_page_markup(client):
    response = client.get("/")
    assert response.status_code == 200

    html = response.get_data(as_text=True)
    assert 'id="quizzes-page"' in html
    assert 'id="quiz-grid"' in html
    assert 'id="quizzes-empty"' in html
    assert 'id="delete-quiz-modal"' in html
    assert 'href="#quizzes"' in html
    assert 'href="#quiz-create"' in html


def test_quiz_list_assets_include_quiz_logic(client):
    js_response = client.get("/js/questions.js")
    api_response = client.get("/js/api.js")

    assert js_response.status_code == 200
    assert api_response.status_code == 200
    assert b"QuizListPage" in js_response.data
    assert b"DeleteQuizDialog" in js_response.data
    assert b"fetchQuizzes" in api_response.data
    assert b"deleteQuiz" in api_response.data


def test_quiz_list_api_supports_page(client):
    question_ids = []
    for index in range(3):
        response = client.post(
            "/api/questions",
            json={
                "question": f"Quiz list question {index + 1}",
                "a": "A",
                "b": "B",
                "c": "C",
                "d": "D",
                "correct": "A",
            },
        )
        question_ids.append(response.get_json()["question"]["id"])

    create_response = client.post(
        "/api/quizzes",
        json=quiz_payload(name="Frontend Quiz", question_ids=question_ids),
    )
    assert create_response.status_code == 201

    list_response = client.get("/api/quizzes")
    assert list_response.status_code == 200
    quizzes = list_response.get_json()["quizzes"]
    assert len(quizzes) == 1
    assert quizzes[0]["name"] == "Frontend Quiz"
    assert quizzes[0]["questionCount"] == 3
