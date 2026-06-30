from typing import Any

from flask import Blueprint, Response, current_app, jsonify, request

from backend.errors import ValidationError
from backend.exam_repository import ExamAttemptNotFoundError, ExamAttemptRepository
from backend.quiz_repository import QuizNotFoundError, QuizRepository

exams_bp = Blueprint("exams", __name__, url_prefix="/api/exams")

VALID_OPTIONS = frozenset({"A", "B", "C", "D"})


def _exam_repository() -> ExamAttemptRepository:
    return current_app.extensions["exam_repository"]


def _quiz_repository() -> QuizRepository:
    return current_app.extensions["quiz_repository"]


def _error_response(
    message: str,
    *,
    status: int,
    field: str | None = None,
) -> tuple[Response, int]:
    return jsonify({"error": message, "field": field}), status


def _normalize_selected_option(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValidationError("selected_option must be a string or null.", "selected_option")
    normalized = value.strip().upper()
    if normalized not in VALID_OPTIONS:
        raise ValidationError(
            "selected_option must be one of A, B, C, or D.",
            "selected_option",
        )
    return normalized


def _load_pending_attempt(attempt_id: int) -> tuple[Any, Any]:
    try:
        attempt_data = _exam_repository().get_attempt_with_answers(attempt_id)
    except ExamAttemptNotFoundError as error:
        raise error

    if attempt_data.attempt.submitted_at is not None:
        raise ValidationError("This exam attempt has already been submitted.")

    return attempt_data.attempt, attempt_data


def _build_submit_response(attempt_id: int) -> dict[str, Any]:
    attempt_data = _exam_repository().get_attempt_with_answers(attempt_id)
    attempt = attempt_data.attempt
    quiz = _quiz_repository().get(attempt.quiz_id)

    answers_by_question_id = {
        answer.question_id: answer.selected_option
        for answer in attempt_data.answers
    }

    answer_rows: list[dict[str, Any]] = []
    score = 0
    total = len(quiz.questions)

    for question in quiz.questions:
        selected_option = answers_by_question_id.get(question.id)
        is_correct = selected_option == question.correct
        if is_correct:
            score += 1

        answer_rows.append(
            {
                "question_id": question.id,
                "selected_option": selected_option,
                "correct_option": question.correct,
                "is_correct": is_correct,
                "question_text": question.question,
                "a": question.a,
                "b": question.b,
                "c": question.c,
                "d": question.d,
            }
        )

    percentage = round((score / total) * 100) if total else 0

    return {
        "score": score,
        "total": total,
        "percentage": percentage,
        "answers": answer_rows,
    }


@exams_bp.post("/attempts")
def create_attempt() -> tuple[Response, int]:
    payload = request.get_json(silent=True)
    if payload is None:
        return _error_response("Request body must be valid JSON.", status=400)

    quiz_id = payload.get("quiz_id")
    if isinstance(quiz_id, bool) or not isinstance(quiz_id, int):
        return _error_response("quiz_id must be an integer.", status=400, field="quiz_id")

    try:
        _quiz_repository().get(quiz_id)
    except QuizNotFoundError as error:
        return _error_response(str(error), status=404)

    attempt = _exam_repository().create_attempt(quiz_id)
    return jsonify({"attempt_id": attempt.id}), 201


@exams_bp.put("/attempts/<int:attempt_id>/answers/<int:question_id>")
def save_answer(attempt_id: int, question_id: int) -> tuple[Response, int]:
    payload = request.get_json(silent=True)
    if payload is None:
        return _error_response("Request body must be valid JSON.", status=400)

    try:
        selected_option = _normalize_selected_option(payload.get("selected_option"))
        attempt, _ = _load_pending_attempt(attempt_id)
    except ExamAttemptNotFoundError as error:
        return _error_response(str(error), status=404)
    except ValidationError as error:
        status = 409 if "already been submitted" in str(error) else 400
        return _error_response(str(error), status=status, field=error.field)

    try:
        quiz = _quiz_repository().get(attempt.quiz_id)
    except QuizNotFoundError as error:
        return _error_response(str(error), status=404)

    if question_id not in quiz.question_ids:
        return _error_response(
            f"Question {question_id} is not part of quiz {attempt.quiz_id}.",
            status=404,
        )

    _exam_repository().save_answer(attempt_id, question_id, selected_option)
    return "", 204


@exams_bp.post("/attempts/<int:attempt_id>/submit")
def submit_attempt(attempt_id: int) -> tuple[Response, int]:
    try:
        attempt_data = _exam_repository().get_attempt_with_answers(attempt_id)
    except ExamAttemptNotFoundError as error:
        return _error_response(str(error), status=404)

    if attempt_data.attempt.submitted_at is not None:
        return _error_response(
            "This exam attempt has already been submitted.",
            status=409,
        )

    summary = _build_submit_response(attempt_id)
    _exam_repository().submit_attempt(
        attempt_id,
        score=summary["score"],
        total=summary["total"],
    )
    return jsonify(summary), 200
