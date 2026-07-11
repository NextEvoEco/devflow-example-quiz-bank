import pytest

from backend.db import init_database
from backend.question_repository import QuestionNotFoundError, QuestionRepository
from backend.validation import DEFAULT_DIFFICULTY, ValidationError, validate_question_payload


@pytest.fixture
def db_paths(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    db_path = data_dir / "quiz_bank.db"
    monkeypatch.setattr("backend.config.DATA_DIR", data_dir)
    monkeypatch.setattr("backend.config.DATABASE_PATH", db_path)
    monkeypatch.setattr("backend.db.DATA_DIR", data_dir)
    monkeypatch.setattr("backend.db.DATABASE_PATH", db_path)
    init_database()
    return data_dir, db_path


@pytest.fixture
def repository(db_paths):
    return QuestionRepository()


def valid_question_payload(**overrides):
    payload = {
        "question": "What is 2 + 2?",
        "a": "3",
        "b": "4",
        "c": "5",
        "d": "6",
        "correct": "B",
    }
    payload.update(overrides)
    return payload


def test_validate_question_payload_defaults_difficulty():
    validated = validate_question_payload(valid_question_payload())
    assert validated["difficulty"] == DEFAULT_DIFFICULTY


def test_validate_question_payload_rejects_missing_option():
    with pytest.raises(ValidationError) as exc_info:
        validate_question_payload(valid_question_payload(a=""))

    assert "a" in exc_info.value.errors


def test_validate_question_payload_rejects_invalid_correct_answer():
    with pytest.raises(ValidationError) as exc_info:
        validate_question_payload(valid_question_payload(correct="E"))

    assert "correct" in exc_info.value.errors


def test_create_list_search_update_delete(repository):
    created = repository.create(valid_question_payload(question="Capital of France?"))
    assert created["id"] is not None
    assert created["difficulty"] == "Medium"

    listed = repository.list_all()
    assert len(listed) == 1
    assert listed[0]["question"] == "Capital of France?"

    matches = repository.search("france")
    assert len(matches) == 1

    updated = repository.update(
        created["id"],
        valid_question_payload(
            question="Capital of Germany?",
            correct="C",
            difficulty="Hard",
        ),
    )
    assert updated["question"] == "Capital of Germany?"
    assert updated["correct"] == "C"
    assert updated["difficulty"] == "Hard"

    repository.delete(created["id"])
    assert repository.get_by_id(created["id"]) is None


def test_delete_missing_question_raises(repository):
    with pytest.raises(QuestionNotFoundError):
        repository.delete(999)
