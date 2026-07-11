from __future__ import annotations


def test_quiz_preview_shell_is_present(client):
    response = client.get("/")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert 'id="quiz-preview-button"' in html
    assert 'id="quiz-preview-placeholder"' in html
    assert 'id="quiz-preview-list"' in html
    assert 'id="preview-question-count"' in html
    assert 'id="quiz-preview-close-button"' in html
