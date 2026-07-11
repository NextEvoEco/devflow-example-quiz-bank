from backend.app import create_app
from backend.config import DATABASE_PATH


def test_app_serves_minimal_shell_page():
    app = create_app()
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Quiz Bank" in response.data


def test_database_is_initialized_on_first_start():
    create_app()

    assert DATABASE_PATH.exists()
