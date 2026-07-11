from __future__ import annotations


def test_quiz_builder_page_shell_is_present(client):
    response = client.get("/")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert 'id="quiz-builder-form"' in html
    assert 'id="quiz-name-input"' in html
    assert 'id="selected-questions-list"' in html
    assert 'id="available-questions-list"' in html
    assert "Save Quiz" in html
    assert "Preview" in html
