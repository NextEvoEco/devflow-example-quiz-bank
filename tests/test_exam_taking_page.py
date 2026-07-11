from __future__ import annotations


def test_exam_taking_and_results_shell_are_present(client):
    response = client.get("/")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert 'id="exam-taking-view"' in html
    assert 'id="exam-progress-fill"' in html
    assert 'id="exam-question-jump"' in html
    assert 'id="exam-option-list"' in html
    assert 'id="exam-prev-button"' in html
    assert 'id="exam-next-button"' in html
    assert 'id="exam-results-view"' in html
    assert 'id="results-back-to-exams-button"' in html
