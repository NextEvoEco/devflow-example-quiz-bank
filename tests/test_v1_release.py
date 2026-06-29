import json
import sqlite3
from pathlib import Path

import pytest

from backend.app import create_app
from backend.database import initialize_database


@pytest.fixture
def client(tmp_path: Path):
    db_path = tmp_path / "quiz_bank.db"
    initialize_database(db_path)
    app = create_app(db_path)
    return app.test_client(), db_path


def sample_payload(**overrides) -> dict[str, str]:
    payload = {
        "question": "What is 2 + 2?",
        "a": "3",
        "b": "4",
        "c": "5",
        "d": "6",
        "correct": "B",
        "difficulty": "Medium",
    }
    payload.update(overrides)
    return payload


def test_v1_starts_with_health_check_and_question_bank_page(client) -> None:
    test_client, _ = client

    health_response = test_client.get("/api/health")
    assert health_response.status_code == 200
    assert health_response.get_json() == {"status": "ok"}

    page_response = test_client.get("/")
    assert page_response.status_code == 200
    html = page_response.get_data(as_text=True)
    assert "Question Bank" in html
    assert 'id="question-table"' in html
    assert 'id="editor-modal"' in html


def test_v1_starts_with_empty_question_bank(client) -> None:
    test_client, _ = client

    response = test_client.get("/api/questions")
    assert response.status_code == 200
    assert response.get_json() == {"questions": []}


def test_v1_sqlite_persists_questions_across_requests(client) -> None:
    test_client, db_path = client

    create_response = test_client.post(
        "/api/questions",
        data=json.dumps(sample_payload(question="Persisted question")),
        content_type="application/json",
    )
    assert create_response.status_code == 201
    created = create_response.get_json()

    list_response = test_client.get("/api/questions")
    assert len(list_response.get_json()["questions"]) == 1

    with sqlite3.connect(db_path) as connection:
        row = connection.execute(
            "SELECT question FROM questions WHERE id = ?",
            (created["id"],),
        ).fetchone()
        assert row is not None
        assert row[0] == "Persisted question"


def test_v1_question_bank_crud_and_search_baseline(client) -> None:
    test_client, _ = client

    first = test_client.post(
        "/api/questions",
        data=json.dumps(sample_payload(question="Alpha topic")),
        content_type="application/json",
    ).get_json()
    second = test_client.post(
        "/api/questions",
        data=json.dumps(sample_payload(question="Beta topic", difficulty="Hard")),
        content_type="application/json",
    ).get_json()

    search_response = test_client.get("/api/questions?q=beta")
    assert len(search_response.get_json()["questions"]) == 1
    assert search_response.get_json()["questions"][0]["id"] == second["id"]

    update_response = test_client.put(
        f"/api/questions/{first['id']}",
        data=json.dumps({"question": "Alpha topic updated", "difficulty": "Easy"}),
        content_type="application/json",
    )
    assert update_response.status_code == 200
    assert update_response.get_json()["difficulty"] == "Easy"

    delete_response = test_client.delete(f"/api/questions/{second['id']}")
    assert delete_response.status_code == 204
    assert len(test_client.get("/api/questions").get_json()["questions"]) == 1


def test_v1_validation_rules_are_enforced(client) -> None:
    test_client, _ = client

    empty_question = test_client.post(
        "/api/questions",
        data=json.dumps(sample_payload(question="")),
        content_type="application/json",
    )
    assert empty_question.status_code == 400
    assert empty_question.get_json()["field"] == "question"

    default_difficulty = test_client.post(
        "/api/questions",
        data=json.dumps(sample_payload()),
        content_type="application/json",
    )
    assert default_difficulty.status_code == 201
    assert default_difficulty.get_json()["difficulty"] == "Medium"


@pytest.mark.parametrize(
    "path",
    [
        "/api/exams",
        "/quizList",
        "/examList",
    ],
)
def test_v1_out_of_scope_routes_are_not_available(client, path: str) -> None:
    test_client, _ = client
    response = test_client.get(path)
    assert response.status_code == 404


def test_v1_out_of_scope_navigation_remains_disabled(client) -> None:
    test_client, _ = client
    html = test_client.get("/").get_data(as_text=True)

    assert 'disabled>Quiz Builder</button>' in html.replace("\n", " ") or "Quiz Builder</button>" in html
    assert "Online Exam" in html
    assert 'nav-item is-disabled' in html
