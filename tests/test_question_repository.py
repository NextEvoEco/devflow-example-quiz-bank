import pytest

from backend.database import init_db
from backend.question_repository import QuestionRepository
from backend.validation import DEFAULT_DIFFICULTY, ValidationError


def make_payload(**overrides):
    payload = {
        "question": "What is 2 + 2?",
        "a": "3",
        "b": "4",
        "c": "5",
        "d": "6",
        "correct": "B",
        "difficulty": "Easy",
    }
    payload.update(overrides)
    return payload


@pytest.fixture
def repo(tmp_path):
    db_path = tmp_path / "test_quiz_bank.db"
    init_db(db_path)
    return QuestionRepository(db_path=db_path)


# --- CRUD + search -----------------------------------------------------------


def test_create_and_get(repo):
    created = repo.create(make_payload())
    assert created["id"] is not None
    assert created["question"] == "What is 2 + 2?"
    assert created["correct"] == "B"

    fetched = repo.get(created["id"])
    assert fetched == created


def test_list_returns_all_ordered(repo):
    repo.create(make_payload(question="First question"))
    repo.create(make_payload(question="Second question"))

    items = repo.list()
    assert len(items) == 2
    assert [q["question"] for q in items] == ["First question", "Second question"]


def test_update_changes_fields(repo):
    created = repo.create(make_payload())
    updated = repo.update(created["id"], make_payload(question="Updated text", correct="C"))

    assert updated["id"] == created["id"]
    assert updated["question"] == "Updated text"
    assert updated["correct"] == "C"


def test_update_missing_returns_none(repo):
    assert repo.update(9999, make_payload()) is None


def test_delete_removes_question(repo):
    created = repo.create(make_payload())
    assert repo.delete(created["id"]) is True
    assert repo.get(created["id"]) is None


def test_delete_missing_returns_false(repo):
    assert repo.delete(9999) is False


def test_search_is_case_insensitive_substring(repo):
    repo.create(make_payload(question="Python basics"))
    repo.create(make_payload(question="JavaScript basics"))
    repo.create(make_payload(question="Unrelated topic"))

    results = repo.list(search="basics")
    assert len(results) == 2

    results = repo.list(search="PYTHON")
    assert len(results) == 1
    assert results[0]["question"] == "Python basics"


# --- validation --------------------------------------------------------------


@pytest.mark.parametrize("field", ["question", "a", "b", "c", "d"])
def test_missing_required_text_field_is_rejected(repo, field):
    with pytest.raises(ValidationError) as exc:
        repo.create(make_payload(**{field: ""}))
    assert field in exc.value.errors


def test_missing_correct_is_rejected(repo):
    with pytest.raises(ValidationError) as exc:
        repo.create(make_payload(correct=""))
    assert "correct" in exc.value.errors


def test_invalid_correct_value_is_rejected(repo):
    with pytest.raises(ValidationError) as exc:
        repo.create(make_payload(correct="E"))
    assert "correct" in exc.value.errors


def test_invalid_difficulty_is_rejected(repo):
    with pytest.raises(ValidationError) as exc:
        repo.create(make_payload(difficulty="Impossible"))
    assert "difficulty" in exc.value.errors


def test_omitted_difficulty_gets_default(repo):
    payload = make_payload()
    del payload["difficulty"]
    created = repo.create(payload)
    assert created["difficulty"] == DEFAULT_DIFFICULTY


def test_empty_difficulty_gets_default(repo):
    created = repo.create(make_payload(difficulty="   "))
    assert created["difficulty"] == DEFAULT_DIFFICULTY


def test_difficulty_is_normalized(repo):
    created = repo.create(make_payload(difficulty="hard"))
    assert created["difficulty"] == "Hard"


def test_correct_is_normalized_to_uppercase(repo):
    created = repo.create(make_payload(correct="c"))
    assert created["correct"] == "C"


def test_text_fields_are_trimmed(repo):
    created = repo.create(make_payload(question="  spaced  "))
    assert created["question"] == "spaced"
