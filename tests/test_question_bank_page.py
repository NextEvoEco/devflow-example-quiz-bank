import json
from pathlib import Path

import pytest

from backend.app import create_app
from backend.database import initialize_database


@pytest.fixture
def client(tmp_path: Path):
    db_path = tmp_path / "quiz_bank.db"
    initialize_database(db_path)
    app = create_app(db_path)
    return app.test_client()


def sample_payload(**overrides) -> dict[str, str]:
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


def test_question_bank_page_includes_list_shell(client) -> None:
    response = client.get("/")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'id="question-table"' in html
    assert 'id="search-input"' in html
    assert 'id="empty-state"' in html
    assert 'id="editor-modal"' in html
    assert "Add Question" in html
    assert "No questions found" in html


def test_question_bank_page_assets_are_served(client) -> None:
    css_response = client.get("/css/app.css")
    js_response = client.get("/js/app.js")

    assert css_response.status_code == 200
    assert js_response.status_code == 200
    assert ".question-table" in css_response.get_data(as_text=True)
    assert "fetchQuestions" in js_response.get_data(as_text=True)


def test_api_list_and_search_support_question_bank_rendering(client) -> None:
    client.post(
        "/api/questions",
        data=json.dumps(sample_payload(question="Capital of France?")),
        content_type="application/json",
    )
    client.post(
        "/api/questions",
        data=json.dumps(sample_payload(question="Largest planet?", correct="C", difficulty="Hard")),
        content_type="application/json",
    )

    list_response = client.get("/api/questions")
    assert list_response.status_code == 200
    questions = list_response.get_json()["questions"]
    assert len(questions) == 2
    assert {question["difficulty"] for question in questions} == {"Medium", "Hard"}

    search_response = client.get("/api/questions?q=planet")
    assert search_response.status_code == 200
    search_results = search_response.get_json()["questions"]
    assert len(search_results) == 1
    assert "planet" in search_results[0]["question"].lower()

    empty_search_response = client.get("/api/questions?q=missing-term")
    assert empty_search_response.status_code == 200
    assert empty_search_response.get_json()["questions"] == []
