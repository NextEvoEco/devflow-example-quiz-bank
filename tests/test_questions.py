from __future__ import annotations

import pytest

from backend.questions import (
    DEFAULT_DIFFICULTY,
    QuestionRepository,
    QuestionValidationError,
    validate_question_payload,
)


@pytest.fixture
def question_repository(app):
    return QuestionRepository(app.config["DATABASE_PATH"])


def make_payload(**overrides):
    payload = {
        "question": "What is 2 + 2?",
        "option_a": "3",
        "option_b": "4",
        "option_c": "5",
        "option_d": "6",
        "correct_answer": "B",
        "difficulty": "Easy",
    }
    payload.update(overrides)
    return payload


def test_validate_question_payload_applies_default_difficulty():
    payload = make_payload()
    payload.pop("difficulty")

    normalized = validate_question_payload(payload)

    assert normalized["difficulty"] == DEFAULT_DIFFICULTY


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("question", ""),
        ("option_a", " "),
        ("option_b", ""),
        ("option_c", ""),
        ("option_d", ""),
        ("correct_answer", "Z"),
    ],
)
def test_validate_question_payload_rejects_invalid_values(field, value):
    payload = make_payload(**{field: value})

    with pytest.raises(QuestionValidationError):
        validate_question_payload(payload)


def test_create_and_list_questions(question_repository):
    created = question_repository.create_question(make_payload(difficulty="hard"))
    listed = question_repository.list_questions()

    assert created.id is not None
    assert created.difficulty == "Hard"
    assert [question.id for question in listed] == [created.id]


def test_search_questions_matches_case_insensitive_substring(question_repository):
    first = question_repository.create_question(
        make_payload(question="What is the capital of Taiwan?")
    )
    second = question_repository.create_question(
        make_payload(question="Name the largest ocean", correct_answer="A")
    )

    results = question_repository.search_questions("capital")

    assert [question.id for question in results] == [first.id]
    assert second.id not in [question.id for question in results]


def test_update_question_replaces_stored_values(question_repository):
    created = question_repository.create_question(make_payload())

    updated = question_repository.update_question(
        created.id,
        make_payload(
            question="What is 3 + 3?",
            option_a="5",
            option_b="6",
            option_c="7",
            option_d="8",
            correct_answer="b",
        ),
    )

    assert updated.question == "What is 3 + 3?"
    assert updated.option_b == "6"
    assert updated.correct_answer == "B"
    assert updated.difficulty == "Easy"


def test_delete_question_removes_record(question_repository):
    created = question_repository.create_question(make_payload())

    deleted = question_repository.delete_question(created.id)

    assert deleted is True
    assert question_repository.get_question(created.id) is None


def test_update_question_raises_for_missing_record(question_repository):
    with pytest.raises(KeyError):
        question_repository.update_question(999, make_payload())
