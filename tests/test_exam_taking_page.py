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
                "question": f"Exam taking question {index + 1}",
                "a": f"A{index}",
                "b": f"B{index}",
                "c": f"C{index}",
                "d": f"D{index}",
                "correct": ["A", "B", "C"][index % 3],
            },
        )
        assert response.status_code == 201
        question_ids.append(response.get_json()["question"]["id"])
    return question_ids


def test_exam_taking_page_markup(client):
    response = client.get("/")
    assert response.status_code == 200

    html = response.get_data(as_text=True)
    assert 'id="exam-taking-page"' in html
    assert 'id="exam-options"' in html
    assert 'id="exam-progress-bar"' in html
    assert 'id="exam-question-jump"' in html
    assert 'id="exam-prev-btn"' in html
    assert 'id="exam-next-btn"' in html
    assert 'id="exam-exit-btn"' in html
    assert 'id="exam-results-page"' in html


def test_exam_taking_assets_include_exam_logic(client):
    js_response = client.get("/js/questions.js")
    api_response = client.get("/js/api.js")

    assert js_response.status_code == 200
    assert api_response.status_code == 200
    assert b"ExamTakingPage" in js_response.data
    assert b"ExamResultsPage" in js_response.data
    assert b"renderExamOption" in js_response.data
    assert b"examResultsPayload" in js_response.data
    assert b"createExamAttempt" in api_response.data
    assert b"saveExamAnswer" in api_response.data
    assert b"submitExamAttempt" in api_response.data


def test_exam_taking_api_supports_exam_flow(client):
    question_ids = create_questions(client, 3)

    quiz_response = client.post(
        "/api/quizzes",
        json=quiz_payload(name="Exam Taking Quiz", question_ids=question_ids),
    )
    assert quiz_response.status_code == 201
    quiz_id = quiz_response.get_json()["quiz"]["id"]

    attempt_response = client.post("/api/exams/attempts", json={"quiz_id": quiz_id})
    assert attempt_response.status_code == 201
    attempt_id = attempt_response.get_json()["attempt_id"]

    save_response = client.put(
        f"/api/exams/attempts/{attempt_id}/answers/{question_ids[0]}",
        json={"selected_option": "A"},
    )
    assert save_response.status_code == 204

    submit_response = client.post(f"/api/exams/attempts/{attempt_id}/submit")
    assert submit_response.status_code == 200
    body = submit_response.get_json()
    assert body["score"] == 1
    assert body["total"] == 3
    assert len(body["answers"]) == 3
