def test_question_bank_page_markup(client):
    response = client.get("/")
    assert response.status_code == 200

    html = response.get_data(as_text=True)
    assert 'id="questions-page"' in html
    assert 'id="question-search"' in html
    assert 'id="question-table"' in html
    assert 'id="questions-empty"' in html
    assert "Add Question" in html
    assert 'id="question-editor-modal"' in html
    assert 'data-nav-page="quizzes"' in html
    assert "/js/questions.js" in html


def test_question_bank_static_assets(client):
    css_response = client.get("/css/styles.css")
    js_response = client.get("/js/questions.js")

    assert css_response.status_code == 200
    assert js_response.status_code == 200
    assert b"QuestionBankPage" in js_response.data


def test_question_bank_search_api_supports_list_page(client):
    client.post(
        "/api/questions",
        json={
            "question": "What is Python?",
            "a": "Snake",
            "b": "Language",
            "c": "Framework",
            "d": "Database",
            "correct": "B",
        },
    )
    client.post(
        "/api/questions",
        json={
            "question": "What is SQLite?",
            "a": "Language",
            "b": "Framework",
            "c": "Database",
            "d": "Browser",
            "correct": "C",
        },
    )

    all_response = client.get("/api/questions")
    search_response = client.get("/api/questions?q=python")

    assert len(all_response.get_json()["questions"]) == 2
    assert len(search_response.get_json()["questions"]) == 1
    assert search_response.get_json()["questions"][0]["question"] == "What is Python?"
