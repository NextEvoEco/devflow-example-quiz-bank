import json
from pathlib import Path

import pytest

from backend.app import create_app
from backend.database import initialize_database
from tests.test_quizzes_api import create_questions, sample_quiz_payload


@pytest.fixture
def client(tmp_path: Path):
    db_path = tmp_path / "quiz_bank.db"
    initialize_database(db_path)
    app = create_app(db_path)
    return app.test_client()


def test_quiz_preview_assets_are_served(client) -> None:
    preview_response = client.get("/js/quiz-preview.js")
    builder_response = client.get("/js/quiz-builder.js")
    html_response = client.get("/")

    assert preview_response.status_code == 200
    assert builder_response.status_code == 200
    assert html_response.status_code == 200

    preview_js = preview_response.get_data(as_text=True)
    assert "renderQuizPreviewContent" in preview_js
    assert "preview-option" in preview_js
    assert "Correct answer" in preview_js
    assert "question.a" in preview_js
    assert "question.correct" in preview_js

    html = html_response.get_data(as_text=True)
    assert 'src="/js/quiz-preview.js"' in html
    assert 'id="quiz-preview-modal"' in html


def test_quiz_detail_api_includes_fields_needed_for_preview(client) -> None:
    question_ids = create_questions(client, 3)
    create_response = client.post(
        "/api/quizzes",
        data=json.dumps(sample_quiz_payload(question_ids, name="Preview Quiz")),
        content_type="application/json",
    )
    quiz_id = create_response.get_json()["id"]

    detail_response = client.get(f"/api/quizzes/{quiz_id}")
    assert detail_response.status_code == 200
    detail = detail_response.get_json()

    assert detail["name"] == "Preview Quiz"
    assert len(detail["questions"]) == 3
    first = detail["questions"][0]
    for field in ("question", "a", "b", "c", "d", "correct", "difficulty"):
        assert field in first

    assert detail["questionIds"] == [question["id"] for question in detail["questions"]]


def test_builder_preview_uses_in_memory_order_from_api_payload(client) -> None:
    question_ids = create_questions(client, 4)
    ordered_ids = [question_ids[2], question_ids[0], question_ids[3]]
    payload = sample_quiz_payload(ordered_ids, name="Ordered Preview Quiz")

    create_response = client.post(
        "/api/quizzes",
        data=json.dumps(payload),
        content_type="application/json",
    )
    quiz_id = create_response.get_json()["id"]
    detail = client.get(f"/api/quizzes/{quiz_id}").get_json()

    assert detail["questionIds"] == ordered_ids
    assert [question["id"] for question in detail["questions"]] == ordered_ids
