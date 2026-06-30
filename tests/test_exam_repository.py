import sqlite3
from pathlib import Path

import pytest

from backend.database import SCHEMA_VERSION, get_connection, initialize_database
from backend.exam_repository import ExamAttemptNotFoundError, ExamAttemptRepository
from backend.question_repository import QuestionRepository


@pytest.fixture
def db_path(tmp_path: Path) -> Path:
    path = tmp_path / "quiz_bank.db"
    initialize_database(path)
    return path


@pytest.fixture
def repository(db_path: Path) -> ExamAttemptRepository:
    return ExamAttemptRepository(db_path)


@pytest.fixture
def quiz_id(db_path: Path) -> int:
    with get_connection(db_path) as connection:
        cursor = connection.execute(
            "INSERT INTO quizzes (name) VALUES (?)",
            ("Math Quiz",),
        )
        connection.commit()
        quiz_id = cursor.lastrowid
        assert quiz_id is not None
        return quiz_id


@pytest.fixture
def question_ids(db_path: Path) -> list[int]:
    question_repo = QuestionRepository(db_path)
    ids: list[int] = []
    for index, total in enumerate((2, 3), start=1):
        question = question_repo.create(
            {
                "question": f"What is {index} + {index}?",
                "a": str(total - 1),
                "b": str(total),
                "c": str(total + 1),
                "d": str(total + 2),
                "correct": "B",
            }
        )
        ids.append(question.id)
    return ids


def test_fresh_database_includes_exam_tables(db_path: Path) -> None:
    with sqlite3.connect(db_path) as connection:
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
        assert "exam_attempts" in tables
        assert "exam_answers" in tables

        versions = {
            row[0]
            for row in connection.execute("SELECT version FROM schema_migrations")
        }
        assert SCHEMA_VERSION in versions


def test_create_attempt_returns_pending_attempt(
    repository: ExamAttemptRepository,
    quiz_id: int,
) -> None:
    attempt = repository.create_attempt(quiz_id)

    assert attempt.id > 0
    assert attempt.quiz_id == quiz_id
    assert attempt.score is None
    assert attempt.total is None
    assert attempt.started_at
    assert attempt.submitted_at is None


def test_save_answer_inserts_and_replaces(
    repository: ExamAttemptRepository,
    quiz_id: int,
    question_ids: list[int],
) -> None:
    question_id = question_ids[0]
    attempt = repository.create_attempt(quiz_id)

    repository.save_answer(attempt.id, question_id=question_id, selected_option="A")
    result = repository.get_attempt_with_answers(attempt.id)
    assert len(result.answers) == 1
    assert result.answers[0].selected_option == "A"

    repository.save_answer(attempt.id, question_id=question_id, selected_option="B")
    result = repository.get_attempt_with_answers(attempt.id)
    assert len(result.answers) == 1
    assert result.answers[0].selected_option == "B"


def test_save_answer_allows_null_selected_option(
    repository: ExamAttemptRepository,
    quiz_id: int,
    question_ids: list[int],
) -> None:
    question_id = question_ids[0]
    attempt = repository.create_attempt(quiz_id)

    repository.save_answer(attempt.id, question_id=question_id, selected_option=None)
    result = repository.get_attempt_with_answers(attempt.id)
    assert len(result.answers) == 1
    assert result.answers[0].selected_option is None


def test_submit_attempt_sets_score_and_submitted_at(
    repository: ExamAttemptRepository,
    quiz_id: int,
    question_ids: list[int],
) -> None:
    question_id = question_ids[0]
    attempt = repository.create_attempt(quiz_id)
    repository.save_answer(attempt.id, question_id=question_id, selected_option="B")

    submitted = repository.submit_attempt(attempt.id, score=1, total=1)

    assert submitted.score == 1
    assert submitted.total == 1
    assert submitted.submitted_at is not None

    loaded = repository.get_attempt_with_answers(attempt.id)
    assert loaded.attempt.submitted_at == submitted.submitted_at
    assert loaded.attempt.score == 1
    assert loaded.attempt.total == 1
    assert len(loaded.answers) == 1


def test_get_attempt_with_answers_returns_all_answer_rows(
    repository: ExamAttemptRepository,
    quiz_id: int,
    question_ids: list[int],
) -> None:
    attempt = repository.create_attempt(quiz_id)
    repository.save_answer(attempt.id, question_id=question_ids[0], selected_option="A")
    repository.save_answer(attempt.id, question_id=question_ids[1], selected_option="C")

    result = repository.get_attempt_with_answers(attempt.id)

    assert result.attempt.id == attempt.id
    assert len(result.answers) == 2
    assert {answer.question_id for answer in result.answers} == set(question_ids)


def test_get_attempt_with_answers_raises_for_missing_attempt(
    repository: ExamAttemptRepository,
) -> None:
    with pytest.raises(ExamAttemptNotFoundError):
        repository.get_attempt_with_answers(999)


def test_submit_attempt_raises_for_missing_attempt(
    repository: ExamAttemptRepository,
) -> None:
    with pytest.raises(ExamAttemptNotFoundError):
        repository.submit_attempt(999, score=0, total=0)
