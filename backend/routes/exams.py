from __future__ import annotations

from pathlib import Path

from flask import Blueprint, current_app, jsonify, request

from ..exam_repository import ExamAttemptRepository
from ..questions import ALLOWED_CORRECT_ANSWERS, Question
from ..quizzes import QuizDetail, QuizRepository


class ExamApiError(ValueError):
    """Raised when an Online Exam API request cannot be fulfilled."""

    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.status_code = status_code


exams_bp = Blueprint("exams", __name__)


def _database_path() -> Path:
    return Path(current_app.config["DATABASE_PATH"])


def _exam_repository() -> ExamAttemptRepository:
    return ExamAttemptRepository(_database_path())


def _quiz_repository() -> QuizRepository:
    return QuizRepository(_database_path())


def _load_attempt_or_404(attempt_id: int):
    attempt = _exam_repository().get_attempt_with_answers(attempt_id)
    if attempt is None:
        raise ExamApiError(f"Attempt {attempt_id} not found", 404)
    return attempt


def _load_quiz_or_404(quiz_id: int) -> QuizDetail:
    quiz = _quiz_repository().get_quiz(quiz_id)
    if quiz is None:
        raise ExamApiError(f"Quiz {quiz_id} not found", 404)
    return quiz


def _parse_json_object() -> dict:
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        raise ExamApiError("Request body must be a JSON object")
    return payload


def _parse_selected_option(payload: dict) -> str | None:
    if "selected_option" in payload:
        selected_option = payload["selected_option"]
    elif "selectedOption" in payload:
        selected_option = payload["selectedOption"]
    else:
        raise ExamApiError("'selected_option' is required")

    if selected_option is None:
        return None
    if not isinstance(selected_option, str) or not selected_option.strip():
        raise ExamApiError("'selected_option' must be one of A, B, C, D, or null")

    normalized = selected_option.strip().upper()
    if normalized not in ALLOWED_CORRECT_ANSWERS:
        raise ExamApiError("'selected_option' must be one of A, B, C, D, or null")
    return normalized


def _serialize_answer_review(question: Question, selected_option: str | None) -> dict[str, object]:
    is_correct = selected_option == question.correct_answer
    return {
        "question_id": question.id,
        "question_text": question.question,
        "selected_option": selected_option,
        "correct_option": question.correct_answer,
        "is_correct": is_correct,
        "options": {
            "A": question.option_a,
            "B": question.option_b,
            "C": question.option_c,
            "D": question.option_d,
        },
    }


@exams_bp.post("/api/exams/attempts")
def create_attempt():
    payload = _parse_json_object()
    quiz_id = payload.get("quiz_id", payload.get("quizId"))
    if not isinstance(quiz_id, int):
        raise ExamApiError("'quiz_id' must be an integer")

    _load_quiz_or_404(quiz_id)
    attempt = _exam_repository().create_attempt(quiz_id)
    return jsonify({"attempt_id": attempt.id}), 201


@exams_bp.put("/api/exams/attempts/<int:attempt_id>/answers/<int:question_id>")
def save_answer(attempt_id: int, question_id: int):
    payload = _parse_json_object()
    selected_option = _parse_selected_option(payload)

    attempt = _load_attempt_or_404(attempt_id)
    if attempt.submitted_at is not None:
        raise ExamApiError(f"Attempt {attempt_id} has already been submitted", 409)

    quiz = _load_quiz_or_404(attempt.quiz_id)
    valid_question_ids = {question.id for question in quiz.questions}
    if question_id not in valid_question_ids:
        raise ExamApiError(
            f"Question {question_id} is not part of quiz {attempt.quiz_id}",
            404,
        )

    _exam_repository().save_answer(attempt_id, question_id, selected_option)
    return ("", 204)


@exams_bp.post("/api/exams/attempts/<int:attempt_id>/submit")
def submit_attempt(attempt_id: int):
    attempt = _load_attempt_or_404(attempt_id)
    if attempt.submitted_at is not None:
        raise ExamApiError(f"Attempt {attempt_id} has already been submitted", 409)

    quiz = _load_quiz_or_404(attempt.quiz_id)
    answer_map = {
        answer.question_id: answer.selected_option
        for answer in attempt.answers
    }
    answer_reviews = [
        _serialize_answer_review(question, answer_map.get(question.id))
        for question in quiz.questions
    ]
    score = sum(1 for answer in answer_reviews if answer["is_correct"])
    total = len(answer_reviews)

    submitted = _exam_repository().submit_attempt(attempt_id, score=score, total=total)
    percentage = 0 if total == 0 else round((score / total) * 100)

    return jsonify(
        {
            "attempt_id": submitted.id,
            "quiz_id": submitted.quiz_id,
            "score": submitted.score,
            "total": submitted.total,
            "percentage": percentage,
            "submitted_at": submitted.submitted_at,
            "answers": answer_reviews,
        }
    )


@exams_bp.errorhandler(ExamApiError)
def handle_exam_api_error(error: ExamApiError):
    return jsonify({"error": str(error)}), error.status_code
