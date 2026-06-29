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
        "difficulty": "Medium",
    }
    payload.update(overrides)
    return payload


def test_question_bank_page_includes_editor_and_delete_modals(client) -> None:
    response = client.get("/")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'id="editor-modal"' in html
    assert 'id="delete-modal"' in html
    assert "Save Question" in html
    assert "Delete Question" in html


def test_question_bank_js_exposes_crud_flow_helpers(client) -> None:
    response = client.get("/js/app.js")

    assert response.status_code == 200
    js = response.get_data(as_text=True)
    assert "createQuestion" in js
    assert "updateQuestion" in js
    assert "deleteQuestion" in js
    assert "openEditorModal" in js
    assert "handleConfirmDelete" in js


def test_full_question_bank_add_edit_delete_flow(client) -> None:
    create_response = client.post(
        "/api/questions",
        data=json.dumps(sample_payload(question="First question")),
        content_type="application/json",
    )
    assert create_response.status_code == 201
    created = create_response.get_json()

    list_response = client.get("/api/questions")
    assert len(list_response.get_json()["questions"]) == 1

    update_response = client.put(
        f"/api/questions/{created['id']}",
        data=json.dumps(
            {
                "question": "Updated question",
                "a": "1",
                "b": "2",
                "c": "3",
                "d": "4",
                "correct": "C",
                "difficulty": "Hard",
            }
        ),
        content_type="application/json",
    )
    assert update_response.status_code == 200
    updated = update_response.get_json()
    assert updated["question"] == "Updated question"
    assert updated["difficulty"] == "Hard"

    delete_response = client.delete(f"/api/questions/{created['id']}")
    assert delete_response.status_code == 204

    final_list = client.get("/api/questions")
    assert final_list.get_json()["questions"] == []


def test_invalid_create_is_blocked_with_validation_feedback(client) -> None:
    response = client.post(
        "/api/questions",
        data=json.dumps(sample_payload(question="")),
        content_type="application/json",
    )

    assert response.status_code == 400
    payload = response.get_json()
    assert payload["field"] == "question"
    assert payload["error"]

    list_response = client.get("/api/questions")
    assert list_response.get_json()["questions"] == []
