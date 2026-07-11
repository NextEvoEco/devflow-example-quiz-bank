def quiz_payload(name="Sample Quiz", question_ids=None):
    return {
        "name": name,
        "questionIds": question_ids or [],
    }


def create_questions(client, count=3):
    question_ids = []
    for index in range(count):
        response = client.post(
            "/api/questions",
            json={
                "question": f"Preview question {index + 1}",
                "a": f"A{index}",
                "b": f"B{index}",
                "c": f"C{index}",
                "d": f"D{index}",
                "correct": "B",
            },
        )
        assert response.status_code == 201
        question_ids.append(response.get_json()["question"]["id"])
    return question_ids


def test_quiz_preview_page_markup(client):
    response = client.get("/")
    assert response.status_code == 200

    html = response.get_data(as_text=True)
    assert 'id="quiz-preview-page"' in html
    assert 'id="quiz-preview-content"' in html
    assert 'id="quiz-preview-back-link"' in html


def test_quiz_preview_assets_include_preview_logic(client):
    js_response = client.get("/js/questions.js")

    assert js_response.status_code == 200
    assert b"QuizPreviewPage" in js_response.data
    assert b"renderPreviewQuestion" in js_response.data
    assert b"QUIZ_PREVIEW_DRAFT_KEY" in js_response.data


def test_quiz_preview_api_returns_ordered_questions_with_options(client):
    question_ids = create_questions(client, 3)

    create_response = client.post(
        "/api/quizzes",
        json=quiz_payload(name="Preview Quiz", question_ids=question_ids),
    )
    assert create_response.status_code == 201
    quiz_id = create_response.get_json()["quiz"]["id"]

    get_response = client.get(f"/api/quizzes/{quiz_id}")
    assert get_response.status_code == 200
    quiz = get_response.get_json()["quiz"]
    assert quiz["name"] == "Preview Quiz"
    assert len(quiz["questions"]) == 3
    assert [question["id"] for question in quiz["questions"]] == question_ids

    first_question = quiz["questions"][0]
    assert first_question["question"] == "Preview question 1"
    assert first_question["a"] == "A0"
    assert first_question["b"] == "B0"
    assert first_question["correct"] == "B"
