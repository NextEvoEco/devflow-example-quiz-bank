import pytest

from backend.exam_repository import (
    ExamAttemptAlreadySubmittedError,
    ExamAttemptNotFoundError,
    ExamAttemptRepository,
)
from backend.question_repository import QuestionRepository
from backend.quiz_repository import QuizNotFoundError, QuizRepository


def _create_sample_quiz(question_count: int = 3) -> int:
    question_repository = QuestionRepository()
    question_ids = []
    for index in range(question_count):
        created = question_repository.create(
            {
                "question": f"Exam repository question {index + 1}",
                "a": "Option A",
                "b": "Option B",
                "c": "Option C",
                "d": "Option D",
                "correct": "A",
                "difficulty": "Easy",
            }
        )
        question_ids.append(created["id"])

    quiz = QuizRepository().create(
        {
            "name": "Exam Repository Quiz",
            "questionIds": question_ids,
        }
    )
    return quiz["id"]


def test_create_attempt_returns_pending_attempt(db_paths):
    quiz_id = _create_sample_quiz()
    repository = ExamAttemptRepository()

    attempt = repository.create_attempt(quiz_id)

    assert attempt.id is not None
    assert attempt.quiz_id == quiz_id
    assert attempt.score is None
    assert attempt.total is None
    assert attempt.started_at
    assert attempt.submitted_at is None


def test_create_attempt_rejects_missing_quiz(db_paths):
    repository = ExamAttemptRepository()

    with pytest.raises(QuizNotFoundError):
        repository.create_attempt(9999)


def test_save_answer_inserts_and_replaces_answer(db_paths):
    quiz_id = _create_sample_quiz()
    repository = ExamAttemptRepository()
    attempt = repository.create_attempt(quiz_id)
    quiz = QuizRepository().get_by_id(quiz_id)
    question_id = quiz["questions"][0]["id"]

    repository.save_answer(attempt.id, question_id, "A")
    result = repository.get_attempt_with_answers(attempt.id)
    assert len(result["answers"]) == 1
    assert result["answers"][0].selected_option == "A"

    repository.save_answer(attempt.id, question_id, "B")
    result = repository.get_attempt_with_answers(attempt.id)
    assert len(result["answers"]) == 1
    assert result["answers"][0].selected_option == "B"


def test_save_answer_allows_null_selected_option(db_paths):
    quiz_id = _create_sample_quiz()
    repository = ExamAttemptRepository()
    attempt = repository.create_attempt(quiz_id)
    question_id = QuizRepository().get_by_id(quiz_id)["questions"][0]["id"]

    repository.save_answer(attempt.id, question_id, None)
    result = repository.get_attempt_with_answers(attempt.id)

    assert result["answers"][0].selected_option is None


def test_submit_attempt_sets_score_and_submitted_at(db_paths):
    quiz_id = _create_sample_quiz()
    repository = ExamAttemptRepository()
    attempt = repository.create_attempt(quiz_id)
    quiz = QuizRepository().get_by_id(quiz_id)

    for question in quiz["questions"]:
        repository.save_answer(attempt.id, question["id"], question["correct"])

    submitted = repository.submit_attempt(attempt.id, score=3, total=3)

    assert submitted.score == 3
    assert submitted.total == 3
    assert submitted.submitted_at is not None


def test_submit_attempt_rejects_already_submitted_attempt(db_paths):
    quiz_id = _create_sample_quiz()
    repository = ExamAttemptRepository()
    attempt = repository.create_attempt(quiz_id)

    repository.submit_attempt(attempt.id, score=0, total=3)

    with pytest.raises(ExamAttemptAlreadySubmittedError):
        repository.submit_attempt(attempt.id, score=1, total=3)


def test_save_answer_rejects_submitted_attempt(db_paths):
    quiz_id = _create_sample_quiz()
    repository = ExamAttemptRepository()
    attempt = repository.create_attempt(quiz_id)
    question_id = QuizRepository().get_by_id(quiz_id)["questions"][0]["id"]

    repository.submit_attempt(attempt.id, score=0, total=3)

    with pytest.raises(ExamAttemptAlreadySubmittedError):
        repository.save_answer(attempt.id, question_id, "A")


def test_get_attempt_with_answers_returns_none_for_missing_attempt(db_paths):
    repository = ExamAttemptRepository()

    assert repository.get_attempt_with_answers(9999) is None


def test_submit_attempt_raises_for_missing_attempt(db_paths):
    repository = ExamAttemptRepository()

    with pytest.raises(ExamAttemptNotFoundError):
        repository.submit_attempt(9999, score=0, total=3)
