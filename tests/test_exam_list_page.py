from __future__ import annotations


def test_exam_list_page_shell_is_present(client):
    response = client.get("/")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert 'id="nav-exams"' in html
    assert 'data-page="examList"' in html
    assert 'id="exam-list-view"' in html
    assert 'id="exam-grid"' in html
    assert "Available Exams" in html
    assert 'id="exam-empty-state"' in html
    assert 'id="exam-empty-build-button"' in html
    assert 'id="exam-taking-view"' in html
