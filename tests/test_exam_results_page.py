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


def test_exam_results_page_includes_shell_and_actions(client) -> None:
    response = client.get("/")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'id="page-exam-results"' in html
    assert 'id="exam-score-ring"' in html
    assert 'id="exam-answer-review-list"' in html
    assert 'id="exam-back-to-list-btn"' in html
    assert 'id="exam-retry-btn"' in html
    assert "Exam Complete!" in html
    assert "Answer Review" in html


def test_exam_results_assets_are_served(client) -> None:
    results_response = client.get("/js/exam-results.js")

    assert results_response.status_code == 200
    results_js = results_response.get_data(as_text=True)
    assert "renderScoreSummary" in results_js
    assert "renderAnswerReview" in results_js
    assert "handleRetryQuiz" in results_js
    assert "handleBackToExams" in results_js
    assert "clearExamResultsSession" in results_js
    assert "submitResult" in results_js
