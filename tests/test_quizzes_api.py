import pytest


@pytest.fixture
def question_ids(client):
    ids = []
    for index in range(3):
        response = client.post(
            "/api/questions",
            json={
                "question": f"Quiz API question {index + 1}",
                "a": "A",
                "b": "B",
                "c": "C",
                "d": "D",
                "correct": "A",
            },
        )
        assert response.status_code == 201
        ids.append(response.get_json()["question"]["id"])
    return ids


def quiz_payload(name="Sample Quiz", question_ids=None, **overrides):
    payload = {
        "name": name,
        "questionIds": question_ids or [],
    }
    payload.update(overrides)
    return payload


def test_list_quizzes_empty(client):
    response = client.get("/api/quizzes")
    assert response.status_code == 200
    assert response.get_json() == {"quizzes": []}


def test_create_get_update_delete_quiz_flow(client, question_ids):
    create_response = client.post(
        "/api/quizzes",
        json=quiz_payload(question_ids=question_ids),
    )
    assert create_response.status_code == 201
    created = create_response.get_json()["quiz"]
    quiz_id = created["id"]
    assert created["name"] == "Sample Quiz"
    assert created["questionCount"] == 3
    assert len(created["questions"]) == 3
    assert [question["id"] for question in created["questions"]] == question_ids

    list_response = client.get("/api/quizzes")
    assert list_response.status_code == 200
    quizzes = list_response.get_json()["quizzes"]
    assert len(quizzes) == 1
    assert quizzes[0]["questionCount"] == 3

    get_response = client.get(f"/api/quizzes/{quiz_id}")
    assert get_response.status_code == 200
    assert get_response.get_json()["quiz"]["questions"][0]["question"] == "Quiz API question 1"

    extra_question = client.post(
        "/api/questions",
        json={
            "question": "Quiz API question 4",
            "a": "A",
            "b": "B",
            "c": "C",
            "d": "D",
            "correct": "B",
        },
    ).get_json()["question"]["id"]
    updated_ids = question_ids + [extra_question]

    update_response = client.put(
        f"/api/quizzes/{quiz_id}",
        json={"name": "Updated Quiz", "questionIds": updated_ids},
    )
    assert update_response.status_code == 200
    updated = update_response.get_json()["quiz"]
    assert updated["name"] == "Updated Quiz"
    assert updated["questionCount"] == 4

    delete_response = client.delete(f"/api/quizzes/{quiz_id}")
    assert delete_response.status_code == 204
    assert client.get("/api/quizzes").get_json()["quizzes"] == []


def test_create_quiz_requires_at_least_three_questions(client, question_ids):
    response = client.post(
        "/api/quizzes",
        json=quiz_payload(question_ids=question_ids[:2]),
    )
    assert response.status_code == 400
    assert "questionIds" in response.get_json()["errors"]


def test_create_quiz_rejects_missing_question_ids(client, question_ids):
    response = client.post(
        "/api/quizzes",
        json=quiz_payload(question_ids=question_ids + [9999]),
    )
    assert response.status_code == 400
    assert "questionIds" in response.get_json()["errors"]


def test_create_quiz_rejects_duplicate_question_ids(client, question_ids):
    response = client.post(
        "/api/quizzes",
        json=quiz_payload(question_ids=question_ids[:2] + [question_ids[0]]),
    )
    assert response.status_code == 400
    assert "questionIds" in response.get_json()["errors"]


def test_update_missing_quiz_returns_404(client, question_ids):
    response = client.put(
        "/api/quizzes/999",
        json=quiz_payload(question_ids=question_ids),
    )
    assert response.status_code == 404


def test_delete_missing_quiz_returns_404(client):
    response = client.delete("/api/quizzes/999")
    assert response.status_code == 404
