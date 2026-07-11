def quiz_payload(name="Sample Quiz", question_ids=None):
    return {
        "name": name,
        "questionIds": question_ids or [],
    }


def test_exam_list_page_markup(client):
    response = client.get("/")
    assert response.status_code == 200

    html = response.get_data(as_text=True)
    assert 'data-nav-page="exams"' in html
    assert 'href="#exams"' in html
    assert 'id="exams-page"' in html
    assert 'id="exam-grid"' in html
    assert 'id="exams-empty"' in html
    assert 'id="exam-taking-page"' in html
    assert "Available Exams" in html
    assert 'disabled>Online Exam</button>' not in html


def test_exam_list_assets_include_exam_logic(client):
    js_response = client.get("/js/questions.js")
    api_response = client.get("/js/api.js")

    assert js_response.status_code == 200
    assert api_response.status_code == 200
    assert b"ExamListPage" in js_response.data
    assert b"ExamTakingPage" in js_response.data
    assert b"renderExamCard" in js_response.data
    assert b"#exam-taking-" in js_response.data
    assert b"currentExamQuizId" in js_response.data
    assert b"fetchQuizzes" in api_response.data


def test_exam_list_api_supports_page(client):
    question_ids = []
    for index in range(3):
        response = client.post(
            "/api/questions",
            json={
                "question": f"Exam list question {index + 1}",
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
        json=quiz_payload(name="Frontend Exam Quiz", question_ids=question_ids),
    )
    assert create_response.status_code == 201

    list_response = client.get("/api/quizzes")
    assert list_response.status_code == 200
    quizzes = list_response.get_json()["quizzes"]
    assert len(quizzes) == 1
    assert quizzes[0]["name"] == "Frontend Exam Quiz"
    assert quizzes[0]["questionCount"] == 3
