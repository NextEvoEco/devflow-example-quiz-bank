import pytest

from backend.app import create_app


@pytest.fixture
def client(tmp_path):
    db_path = tmp_path / "page_test.db"
    app = create_app(db_path=db_path)
    app.config.update(TESTING=True)
    return app.test_client()


def test_index_page_served(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.mimetype == "text/html"


def test_index_contains_question_bank_shell(client):
    html = client.get("/").get_data(as_text=True)
    # Sidebar nav
    assert "Question Bank" in html
    # Page header
    assert 'id="question-count"' in html
    assert "Add Question" in html
    # Search box
    assert 'id="search-input"' in html
    # Question table + body
    assert 'id="question-table"' in html
    assert 'id="question-tbody"' in html
    # Empty state
    assert 'id="empty-state"' in html


def test_static_assets_served(client):
    css = client.get("/css/style.css")
    assert css.status_code == 200
    assert "difficulty-badge" in css.get_data(as_text=True)

    js = client.get("/js/app.js")
    assert js.status_code == 200
    body = js.get_data(as_text=True)
    # List page must be API-driven, not hardcoded data.
    assert "/api/questions" in body
    assert "search" in body


def test_page_reads_from_api_end_to_end(client):
    # Seed through the API, then confirm the list endpoint the page consumes returns it.
    client.post(
        "/api/questions",
        json={
            "question": "Seeded question",
            "a": "1", "b": "2", "c": "3", "d": "4",
            "correct": "A", "difficulty": "Hard",
        },
    )
    items = client.get("/api/questions").get_json()
    assert len(items) == 1
    assert items[0]["question"] == "Seeded question"

    # Search filtering the page relies on.
    assert client.get("/api/questions?search=seeded").get_json()[0]["question"] == "Seeded question"
    assert client.get("/api/questions?search=nomatch").get_json() == []
