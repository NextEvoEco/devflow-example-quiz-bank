from __future__ import annotations


def test_question_bank_page_contains_editor_and_delete_dialog_shell(client):
    response = client.get("/")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert 'id="question-form"' in html
    assert 'id="editor-overlay"' in html
    assert 'id="delete-overlay"' in html
    assert "Save Question" in html
    assert "Delete Question" in html
