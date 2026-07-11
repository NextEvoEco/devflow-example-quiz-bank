def quiz_payload(name="Sample Quiz", question_ids=None):
    return {
        "name": name,
        "questionIds": question_ids or [],
    }


def create_questions(client, count=3):
    question_ids = []
    correct_answers = ["A", "B", "C"]
    for index in range(count):
        response = client.post(
            "/api/questions",
            json={
                "question": f"Exam results question {index + 1}",
                "a": f"A{index}",
                "b": f"B{index}",
                "c": f"C{index}",
                "d": f"D{index}",
                "correct": correct_answers[index % 3],
            },
        )
        assert response.status_code == 201
        question_ids.append(response.get_json()["question"]["id"])
    return question_ids


def test_exam_results_page_markup(client):
    response = client.get("/")
    assert response.status_code == 200

    html = response.get_data(as_text=True)
    assert 'id="exam-results-page"' in html
    assert 'id="exam-results-quiz-name"' in html
    assert 'id="exam-results-score-summary"' in html
    assert 'id="exam-results-correct-count"' in html
    assert 'id="exam-results-incorrect-count"' in html
    assert 'id="exam-results-review-list"' in html
    assert 'id="exam-results-retry-btn"' in html
    assert 'id="exam-results-back-btn"' in html
    assert "Exam Complete!" in html
    assert "Answer Review" in html


def test_exam_results_assets_include_results_logic(client):
    js_response = client.get("/js/questions.js")

    assert js_response.status_code == 200
    assert b"ExamResultsPage" in js_response.data
    assert b"renderScoreRing" in js_response.data
    assert b"renderAnswerReviewItem" in js_response.data
    assert b"exam-results-retry-btn" in js_response.data
    assert b"examResultsPayload" in js_response.data


def test_exam_results_submit_payload_supports_page(client):
    question_ids = create_questions(client, 3)

    quiz_response = client.post(
        "/api/quizzes",
        json=quiz_payload(name="Results Quiz", question_ids=question_ids),
    )
    assert quiz_response.status_code == 201
    quiz_id = quiz_response.get_json()["quiz"]["id"]

    attempt_response = client.post("/api/exams/attempts", json={"quiz_id": quiz_id})
    attempt_id = attempt_response.get_json()["attempt_id"]

    client.put(
        f"/api/exams/attempts/{attempt_id}/answers/{question_ids[0]}",
        json={"selected_option": "A"},
    )
    client.put(
        f"/api/exams/attempts/{attempt_id}/answers/{question_ids[1]}",
        json={"selected_option": "A"},
    )

    submit_response = client.post(f"/api/exams/attempts/{attempt_id}/submit")
    assert submit_response.status_code == 200
    body = submit_response.get_json()

    assert body["score"] == 1
    assert body["total"] == 3
    assert "percentage" in body
    assert len(body["answers"]) == 3

    correct_answer = next(item for item in body["answers"] if item["is_correct"])
    incorrect_answer = next(item for item in body["answers"] if not item["is_correct"])

    assert correct_answer["question_text"]
    assert correct_answer["selected_option"]
    assert correct_answer["correct_option"]
    assert incorrect_answer["selected_option"] is not None
    assert incorrect_answer["correct_option"]
