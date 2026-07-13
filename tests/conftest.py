"""Shared pytest fixtures."""

from __future__ import annotations

import pytest

from backend.app import create_app


@pytest.fixture()
def app(tmp_path):
    db_path = tmp_path / "test.db"
    application = create_app(db_path=db_path)
    application.config.update(TESTING=True)
    yield application


@pytest.fixture()
def client(app):
    return app.test_client()
