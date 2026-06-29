import pytest

from backend.database import initialize_database
from backend.errors import ValidationError
from backend.question_repository import QuestionNotFoundError, QuestionRepository
from backend.validation import DEFAULT_DIFFICULTY, validate_question_payload


@pytest.fixture
def repository(tmp_path) -> QuestionRepository:
    db_path = tmp_path / "quiz_bank.db"
    initialize_database(db_path)
    return QuestionRepository(db_path)


def sample_payload(**overrides) -> dict[str, str]:
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


def test_create_question_persists_record(repository: QuestionRepository) -> None:
    created = repository.create(sample_payload())

    assert created.id > 0
    assert created.question == "What is 2 + 2?"
    assert created.correct == "B"
    assert created.difficulty == DEFAULT_DIFFICULTY

    loaded = repository.get(created.id)
    assert loaded.to_dict() == created.to_dict()


def test_create_question_defaults_difficulty_when_omitted(
    repository: QuestionRepository,
) -> None:
    created = repository.create(sample_payload())

    assert created.difficulty == "Medium"


def test_create_question_defaults_difficulty_when_blank(
    repository: QuestionRepository,
) -> None:
    created = repository.create(sample_payload(difficulty="   "))

    assert created.difficulty == "Medium"


def test_list_update_delete_and_search(repository: QuestionRepository) -> None:
    first = repository.create(sample_payload(question="Capital of France?"))
    second = repository.create(
        sample_payload(question="Largest planet?", correct="C", difficulty="Hard")
    )

    assert len(repository.list_all()) == 2

    updated = repository.update(
        first.id,
        {"question": "Capital of France in Europe?", "difficulty": "Easy"},
    )
    assert updated.question == "Capital of France in Europe?"
    assert updated.difficulty == "Easy"

    matches = repository.search("planet")
    assert len(matches) == 1
    assert matches[0].id == second.id

    repository.delete(first.id)
    assert len(repository.list_all()) == 1

    with pytest.raises(QuestionNotFoundError):
        repository.get(first.id)


@pytest.mark.parametrize(
    ("payload", "field"),
    [
        (sample_payload(question=""), "question"),
        (sample_payload(a=""), "a"),
        (sample_payload(correct="E"), "correct"),
        (sample_payload(difficulty="Impossible"), "difficulty"),
    ],
)
def test_invalid_payload_is_rejected(
    repository: QuestionRepository,
    payload: dict[str, str],
    field: str,
) -> None:
    with pytest.raises(ValidationError) as exc_info:
        repository.create(payload)

    assert exc_info.value.field == field


def test_validate_question_payload_rejects_missing_required_fields() -> None:
    with pytest.raises(ValidationError) as exc_info:
        validate_question_payload({"question": "Only text"})

    assert exc_info.value.field == "a"


def test_search_with_empty_query_returns_all(repository: QuestionRepository) -> None:
    repository.create(sample_payload(question="Alpha"))
    repository.create(sample_payload(question="Beta"))

    assert len(repository.search("")) == 2
    assert len(repository.search("   ")) == 2
