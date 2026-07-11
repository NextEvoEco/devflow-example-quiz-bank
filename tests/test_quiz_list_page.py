from __future__ import annotations


def test_quiz_list_page_shell_is_present(client):
    response = client.get("/")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert 'id="nav-quizzes"' in html
    assert 'id="quiz-list-view"' in html
    assert 'id="quiz-grid"' in html
    assert "Create Quiz" in html
    assert 'id="quiz-empty-state"' in html
