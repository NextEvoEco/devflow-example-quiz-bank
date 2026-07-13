"""Exam repository unit tests."""

from __future__ import annotations

import pytest

from backend.database import initialize_database
from backend.exam_repository import ExamAttemptRepository
from backend.models import ValidationError
from backend.question_repository import QuestionRepository
from backend.quiz_repository import QuizRepository


def _seed(db_path):
    initialize_database(db_path)
    qrepo = QuestionRepository(db_path)
    ids = []
    for i in range(3):
        q = qrepo.create_question(
            {
                "question": f"Q{i}",
                "a": "A",
                "b": "B",
                "c": "C",
                "d": "D",
                "correct": "B",
                "difficulty": "Easy",
            }
        )
        ids.append(q.id)
    quiz = QuizRepository(db_path).create_quiz(
        {"name": "Exam Quiz", "question_ids": ids}
    )
    return quiz["id"], ids


def test_exam_repository_flow(tmp_path):
    db_path = tmp_path / "exam.db"
    quiz_id, ids = _seed(db_path)
    repo = ExamAttemptRepository(db_path)

    attempt = repo.create_attempt(quiz_id)
    assert attempt.submitted_at is None

    repo.save_answer(attempt.id, ids[0], "B")
    repo.save_answer(attempt.id, ids[0], "A")  # replace
    attempt2, answers = repo.get_attempt_with_answers(attempt.id)
    assert attempt2.id == attempt.id
    assert len(answers) == 1
    assert answers[0].selected_option == "A"

    result = repo.score_attempt(attempt.id)
    assert result["total"] == 3
    assert result["score"] == 0

    with pytest.raises(ValidationError):
        repo.score_attempt(attempt.id)
