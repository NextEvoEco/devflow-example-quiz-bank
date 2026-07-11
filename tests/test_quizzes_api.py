import pytest

from backend.app import create_app


@pytest.fixture
def app(tmp_path):
    application = create_app(db_path=tmp_path / "quiz_api.db")
    application.config.update(TESTING=True)
    return application


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def question_ids(client):
    """Seed 5 questions and return their ids."""
    ids = []
    for i in range(5):
        resp = client.post(
            "/api/questions",
            json={
                "question": f"Question {i}?",
                "a": "1", "b": "2", "c": "3", "d": "4",
                "correct": "A", "difficulty": "Easy",
            },
        )
        ids.append(resp.get_json()["id"])
    return ids


def quiz_payload(name, ids):
    return {"name": name, "questionIds": ids}


# --- create ------------------------------------------------------------------


def test_create_returns_201_with_ordered_questions(client, question_ids):
    resp = client.post("/api/quizzes", json=quiz_payload("Quiz A", question_ids[:3]))
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["id"] is not None
    assert body["name"] == "Quiz A"
    assert body["questionIds"] == question_ids[:3]
    assert [q["id"] for q in body["questions"]] == question_ids[:3]


def test_create_preserves_custom_order(client, question_ids):
    ordered = [question_ids[2], question_ids[0], question_ids[4]]
    body = client.post("/api/quizzes", json=quiz_payload("Ordered", ordered)).get_json()
    assert body["questionIds"] == ordered


def test_create_with_fewer_than_three_returns_400(client, question_ids):
    resp = client.post("/api/quizzes", json=quiz_payload("Too small", question_ids[:2]))
    assert resp.status_code == 400
    assert "questionIds" in resp.get_json()["fields"]


def test_create_with_nonexistent_question_returns_400(client, question_ids):
    resp = client.post("/api/quizzes", json=quiz_payload("Bad ref", question_ids[:2] + [999999]))
    assert resp.status_code == 400
    assert "questionIds" in resp.get_json()["fields"]


def test_create_with_duplicate_ids_returns_400(client, question_ids):
    dupe = [question_ids[0], question_ids[0], question_ids[1]]
    resp = client.post("/api/quizzes", json=quiz_payload("Dupes", dupe))
    assert resp.status_code == 400
    assert "questionIds" in resp.get_json()["fields"]


def test_create_without_name_returns_400(client, question_ids):
    resp = client.post("/api/quizzes", json={"name": "  ", "questionIds": question_ids[:3]})
    assert resp.status_code == 400
    assert "name" in resp.get_json()["fields"]


def test_create_non_json_returns_400(client):
    resp = client.post("/api/quizzes", data="x", content_type="text/plain")
    assert resp.status_code == 400


# --- list / get --------------------------------------------------------------


def test_list_returns_quizzes_with_counts(client, question_ids):
    client.post("/api/quizzes", json=quiz_payload("Q1", question_ids[:3]))
    client.post("/api/quizzes", json=quiz_payload("Q2", question_ids[:4]))

    items = client.get("/api/quizzes").get_json()
    assert len(items) == 2
    by_name = {q["name"]: q for q in items}
    assert by_name["Q1"]["question_count"] == 3
    assert by_name["Q2"]["question_count"] == 4


def test_get_returns_full_question_objects(client, question_ids):
    created = client.post("/api/quizzes", json=quiz_payload("Detail", question_ids[:3])).get_json()
    body = client.get(f"/api/quizzes/{created['id']}").get_json()
    assert body["name"] == "Detail"
    assert len(body["questions"]) == 3
    first = body["questions"][0]
    for key in ("id", "question", "a", "b", "c", "d", "correct", "difficulty"):
        assert key in first


def test_get_missing_returns_404(client):
    assert client.get("/api/quizzes/9999").status_code == 404


# --- update ------------------------------------------------------------------


def test_update_changes_name_and_questions(client, question_ids):
    created = client.post("/api/quizzes", json=quiz_payload("Old", question_ids[:3])).get_json()
    new_ids = question_ids[1:5]
    resp = client.put(f"/api/quizzes/{created['id']}", json=quiz_payload("New", new_ids))
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["name"] == "New"
    assert body["questionIds"] == new_ids


def test_update_with_fewer_than_three_returns_400(client, question_ids):
    created = client.post("/api/quizzes", json=quiz_payload("Q", question_ids[:3])).get_json()
    resp = client.put(f"/api/quizzes/{created['id']}", json=quiz_payload("Q", question_ids[:1]))
    assert resp.status_code == 400


def test_update_missing_returns_404(client, question_ids):
    resp = client.put("/api/quizzes/9999", json=quiz_payload("X", question_ids[:3]))
    assert resp.status_code == 404


# --- delete ------------------------------------------------------------------


def test_delete_removes_quiz_and_references(client, question_ids):
    created = client.post("/api/quizzes", json=quiz_payload("Bye", question_ids[:3])).get_json()
    assert client.delete(f"/api/quizzes/{created['id']}").status_code == 204
    assert client.get(f"/api/quizzes/{created['id']}").status_code == 404


def test_delete_missing_returns_404(client):
    assert client.delete("/api/quizzes/9999").status_code == 404


def test_deleting_referenced_question_removes_join_row(client, question_ids):
    """Deleting a question used by a quiz must not break the quiz endpoint."""
    created = client.post("/api/quizzes", json=quiz_payload("Ref", question_ids[:3])).get_json()
    # Delete one referenced question via the (unmodified) Question Bank API.
    assert client.delete(f"/api/questions/{question_ids[0]}").status_code == 204
    body = client.get(f"/api/quizzes/{created['id']}").get_json()
    assert question_ids[0] not in body["questionIds"]
    assert len(body["questions"]) == 2


# --- Question Bank must remain unaffected ------------------------------------


def test_question_bank_still_works(client):
    resp = client.post(
        "/api/questions",
        json={"question": "Still here?", "a": "1", "b": "2", "c": "3", "d": "4", "correct": "A"},
    )
    assert resp.status_code == 201
    assert len(client.get("/api/questions").get_json()) == 1
