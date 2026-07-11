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
                "question": f"Builder question {index + 1}",
                "a": "A",
                "b": "B",
                "c": "C",
                "d": "D",
                "correct": "A",
            },
        )
        assert response.status_code == 201
        question_ids.append(response.get_json()["question"]["id"])
    return question_ids


def test_quiz_builder_page_markup(client):
    response = client.get("/")
    assert response.status_code == 200

    html = response.get_data(as_text=True)
    assert 'id="quiz-builder-page"' in html
    assert 'id="quiz-name-input"' in html
    assert 'id="quiz-selected-list"' in html
    assert 'id="quiz-available-list"' in html
    assert 'id="quiz-save-btn"' in html
    assert 'id="quiz-preview-btn"' in html
    assert 'id="quiz-preview-page"' in html


def test_quiz_builder_assets_include_builder_logic(client):
    js_response = client.get("/js/questions.js")
    api_response = client.get("/js/api.js")

    assert js_response.status_code == 200
    assert api_response.status_code == 200
    assert b"QuizBuilderPage" in js_response.data
    assert b"openPreview" in js_response.data
    assert b"createQuiz" in api_response.data
    assert b"updateQuiz" in api_response.data
    assert b"getQuiz" in api_response.data


def test_quiz_builder_api_supports_create_and_edit_flow(client):
    question_ids = create_questions(client, 3)

    create_response = client.post(
        "/api/quizzes",
        json=quiz_payload(name="Builder Quiz", question_ids=question_ids),
    )
    assert create_response.status_code == 201
    quiz_id = create_response.get_json()["quiz"]["id"]

    get_response = client.get(f"/api/quizzes/{quiz_id}")
    assert get_response.status_code == 200
    quiz = get_response.get_json()["quiz"]
    assert quiz["name"] == "Builder Quiz"
    assert [question["id"] for question in quiz["questions"]] == question_ids

    reordered_ids = [question_ids[2], question_ids[0], question_ids[1]]
    update_response = client.put(
        f"/api/quizzes/{quiz_id}",
        json=quiz_payload(name="Updated Builder Quiz", question_ids=reordered_ids),
    )
    assert update_response.status_code == 200
    updated = update_response.get_json()["quiz"]
    assert updated["name"] == "Updated Builder Quiz"
    assert [question["id"] for question in updated["questions"]] == reordered_ids


def test_quiz_builder_api_blocks_save_with_too_few_questions(client):
    question_ids = create_questions(client, 2)

    response = client.post(
        "/api/quizzes",
        json=quiz_payload(name="Too Short", question_ids=question_ids),
    )
    assert response.status_code == 400
    assert "questionIds" in response.get_json()["errors"]
