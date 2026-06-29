from flask import Blueprint, Response, current_app, jsonify, request

from backend.errors import ValidationError
from backend.quiz_repository import QuizNotFoundError, QuizRepository

quizzes_bp = Blueprint("quizzes", __name__, url_prefix="/api/quizzes")


def _repository() -> QuizRepository:
    return current_app.extensions["quiz_repository"]


def _error_response(
    message: str,
    *,
    status: int,
    field: str | None = None,
) -> tuple[Response, int]:
    return jsonify({"error": message, "field": field}), status


@quizzes_bp.get("")
def list_quizzes() -> tuple[Response, int]:
    quizzes = _repository().list_all()
    return jsonify({"quizzes": [quiz.to_dict() for quiz in quizzes]}), 200


@quizzes_bp.get("/<int:quiz_id>")
def get_quiz(quiz_id: int) -> tuple[Response, int]:
    try:
        quiz = _repository().get(quiz_id)
    except QuizNotFoundError as error:
        return _error_response(str(error), status=404)
    return jsonify(quiz.to_dict()), 200


@quizzes_bp.post("")
def create_quiz() -> tuple[Response, int]:
    payload = request.get_json(silent=True)
    if payload is None:
        return _error_response("Request body must be valid JSON.", status=400)

    try:
        quiz = _repository().create(payload)
    except ValidationError as error:
        return _error_response(str(error), status=400, field=error.field)
    return jsonify(quiz.to_dict()), 201


@quizzes_bp.put("/<int:quiz_id>")
def update_quiz(quiz_id: int) -> tuple[Response, int]:
    payload = request.get_json(silent=True)
    if payload is None:
        return _error_response("Request body must be valid JSON.", status=400)

    try:
        quiz = _repository().update(quiz_id, payload)
    except QuizNotFoundError as error:
        return _error_response(str(error), status=404)
    except ValidationError as error:
        return _error_response(str(error), status=400, field=error.field)
    return jsonify(quiz.to_dict()), 200


@quizzes_bp.delete("/<int:quiz_id>")
def delete_quiz(quiz_id: int) -> tuple[Response, int]:
    try:
        _repository().delete(quiz_id)
    except QuizNotFoundError as error:
        return _error_response(str(error), status=404)
    return "", 204
