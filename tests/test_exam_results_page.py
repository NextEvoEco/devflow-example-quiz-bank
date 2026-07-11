from __future__ import annotations


def test_exam_results_shell_is_present(client):
    response = client.get("/")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert 'id="exam-results-view"' in html
    assert 'id="exam-results-quiz-label"' in html
    assert 'id="exam-score-ring-fill"' in html
    assert 'id="exam-score-percentage"' in html
    assert 'id="exam-correct-count"' in html
    assert 'id="exam-incorrect-count"' in html
    assert 'id="exam-review-list"' in html
    assert 'id="retry-exam-button"' in html
