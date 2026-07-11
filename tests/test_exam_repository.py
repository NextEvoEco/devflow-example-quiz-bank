from __future__ import annotations

import sqlite3
from pathlib import Path

from backend.db import initialize_database
from backend.exam_repository import ExamAttemptRepository


def seed_question_and_quiz(database_path: Path) -> tuple[int, int]:
    with sqlite3.connect(database_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        question_cursor = connection.execute(
            """
            INSERT INTO questions (
                question, option_a, option_b, option_c, option_d, correct_answer, difficulty
            ) VALUES (
                'What is 2 + 2?', '3', '4', '5', '6', 'B', 'Easy'
            )
            """
        )
        question_id = question_cursor.lastrowid
        quiz_cursor = connection.execute(
            "INSERT INTO quizzes (name) VALUES ('Math Quiz')"
        )
        quiz_id = quiz_cursor.lastrowid
        connection.execute(
            """
            INSERT INTO quiz_questions (quiz_id, question_id, position)
            VALUES (?, ?, 1)
            """,
            (quiz_id, question_id),
        )
        connection.commit()
    return question_id, quiz_id


def test_exam_attempt_tables_are_created(tmp_path: Path):
    database_path = tmp_path / "exam-schema.db"

    initialize_database(database_path)

    with sqlite3.connect(database_path) as connection:
        tables = connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"
        ).fetchall()

    assert ("exam_answers",) in tables
    assert ("exam_attempts",) in tables


def test_create_attempt_returns_pending_attempt(tmp_path: Path):
    database_path = tmp_path / "exam-attempt.db"
    initialize_database(database_path)
    _, quiz_id = seed_question_and_quiz(database_path)
    repository = ExamAttemptRepository(database_path)

    attempt = repository.create_attempt(quiz_id)

    assert attempt.quiz_id == quiz_id
    assert attempt.score is None
    assert attempt.total is None
    assert attempt.submitted_at is None
    assert attempt.answers == []


def test_save_answer_inserts_or_replaces_answer(tmp_path: Path):
    database_path = tmp_path / "exam-answer.db"
    initialize_database(database_path)
    question_id, quiz_id = seed_question_and_quiz(database_path)
    repository = ExamAttemptRepository(database_path)
    attempt = repository.create_attempt(quiz_id)

    first = repository.save_answer(attempt.id, question_id, "A")
    replaced = repository.save_answer(attempt.id, question_id, "B")

    assert first.question_id == question_id
    assert replaced.question_id == question_id
    assert replaced.selected_option == "B"

    loaded = repository.get_attempt_with_answers(attempt.id)
    assert loaded is not None
    assert len(loaded.answers) == 1
    assert loaded.answers[0].selected_option == "B"


def test_submit_attempt_sets_score_total_and_submitted_at(tmp_path: Path):
    database_path = tmp_path / "exam-submit.db"
    initialize_database(database_path)
    question_id, quiz_id = seed_question_and_quiz(database_path)
    repository = ExamAttemptRepository(database_path)
    attempt = repository.create_attempt(quiz_id)
    repository.save_answer(attempt.id, question_id, None)

    submitted = repository.submit_attempt(attempt.id, score=1, total=1)

    assert submitted.score == 1
    assert submitted.total == 1
    assert submitted.submitted_at is not None
    assert submitted.answers[0].selected_option is None


def test_get_attempt_with_answers_returns_attempt_and_answer_rows(tmp_path: Path):
    database_path = tmp_path / "exam-load.db"
    initialize_database(database_path)
    question_id, quiz_id = seed_question_and_quiz(database_path)
    repository = ExamAttemptRepository(database_path)
    attempt = repository.create_attempt(quiz_id)
    repository.save_answer(attempt.id, question_id, "C")

    loaded = repository.get_attempt_with_answers(attempt.id)

    assert loaded is not None
    assert loaded.id == attempt.id
    assert loaded.quiz_id == quiz_id
    assert len(loaded.answers) == 1
    assert loaded.answers[0].question_id == question_id
    assert loaded.answers[0].selected_option == "C"
