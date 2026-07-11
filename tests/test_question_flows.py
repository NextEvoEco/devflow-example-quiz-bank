def valid_question_payload(**overrides):
    payload = {
        "question": "What is 2 + 2?",
        "a": "3",
        "b": "4",
        "c": "5",
        "d": "6",
        "correct": "B",
    }
    payload.update(overrides)
    return payload


def test_question_editor_and_delete_modal_markup(client):
    response = client.get("/")
    assert response.status_code == 200

    html = response.get_data(as_text=True)
    assert 'id="question-editor-modal"' in html
    assert 'id="delete-question-modal"' in html
    assert 'id="question-editor-form"' in html
    assert 'id="confirm-delete-btn"' in html


def test_question_flow_assets_include_modal_logic(client):
    js_response = client.get("/js/questions.js")
    api_response = client.get("/js/api.js")

    assert js_response.status_code == 200
    assert api_response.status_code == 200
    assert b"QuestionEditorModal" in js_response.data
    assert b"DeleteQuestionDialog" in js_response.data
    assert b"createQuestion" in api_response.data
    assert b"deleteQuestion" in api_response.data


def test_question_add_edit_delete_flow(client):
    create_response = client.post("/api/questions", json=valid_question_payload())
    assert create_response.status_code == 201
    question_id = create_response.get_json()["question"]["id"]

    list_response = client.get("/api/questions")
    assert len(list_response.get_json()["questions"]) == 1

    update_response = client.put(
        f"/api/questions/{question_id}",
        json=valid_question_payload(question="Updated question", difficulty="Hard"),
    )
    assert update_response.status_code == 200
    assert update_response.get_json()["question"]["question"] == "Updated question"
    assert update_response.get_json()["question"]["difficulty"] == "Hard"

    delete_response = client.delete(f"/api/questions/{question_id}")
    assert delete_response.status_code == 204
    assert client.get("/api/questions").get_json()["questions"] == []


def test_question_invalid_payload_returns_field_errors(client):
    response = client.post(
        "/api/questions",
        json=valid_question_payload(question="", correct="Z"),
    )
    assert response.status_code == 400
    body = response.get_json()
    assert "errors" in body
    assert "question" in body["errors"]
    assert "correct" in body["errors"]
