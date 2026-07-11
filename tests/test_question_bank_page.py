from __future__ import annotations


def test_question_bank_page_contains_list_shell(client):
    response = client.get("/")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Question Bank" in html
    assert 'id="search-input"' in html
    assert 'id="question-table-body"' in html
    assert "Add Question" in html
    assert "Actions" in html
