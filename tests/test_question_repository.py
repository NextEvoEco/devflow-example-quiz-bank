"""Tests for question validation and persistence."""

from __future__ import annotations

import pytest

from backend.database import initialize_database
from backend.models import ValidationError, normalize_question_payload
from backend.question_repository import QuestionRepository


def _valid_payload(**overrides):
    data = {
        "question": "What is 2+2?",
        "a": "3",
        "b": "4",
        "c": "5",
        "d": "6",
        "correct": "B",
        "difficulty": "Easy",
    }
    data.update(overrides)
    return data


def test_normalize_defaults_difficulty():
    payload = normalize_question_payload(_valid_payload(difficulty=None))
    # omit key entirely
    data = _valid_payload()
    del data["difficulty"]
    payload = normalize_question_payload(data)
    assert payload["difficulty"] == "Medium"


def test_normalize_rejects_missing_fields():
    with pytest.raises(ValidationError):
        normalize_question_payload(_valid_payload(question=""))
    with pytest.raises(ValidationError):
        normalize_question_payload(_valid_payload(a=""))
    with pytest.raises(ValidationError):
        normalize_question_payload(_valid_payload(correct="E"))


def test_repository_crud_and_search(tmp_path):
    db_path = tmp_path / "q.db"
    initialize_database(db_path)
    repo = QuestionRepository(db_path)

    created = repo.create_question(_valid_payload(question="Capital of France?"))
    assert created.id > 0
    assert created.difficulty == "Easy"

    listed = repo.list_questions()
    assert len(listed) == 1

    found = repo.list_questions(search="france")
    assert len(found) == 1
    assert repo.list_questions(search="xyz") == []

    updated = repo.update_question(
        created.id,
        _valid_payload(question="Capital of France is?", difficulty="Hard"),
    )
    assert updated.question.startswith("Capital of France is")
    assert updated.difficulty == "Hard"

    repo.delete_question(created.id)
    assert repo.list_questions() == []


def test_create_defaults_difficulty_in_storage(tmp_path):
    db_path = tmp_path / "q.db"
    initialize_database(db_path)
    repo = QuestionRepository(db_path)
    data = _valid_payload()
    del data["difficulty"]
    created = repo.create_question(data)
    assert created.difficulty == "Medium"
