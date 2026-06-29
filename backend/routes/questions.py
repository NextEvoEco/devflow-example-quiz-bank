from flask import Blueprint, Response, current_app, jsonify, request

from backend.errors import ValidationError
from backend.question_repository import QuestionNotFoundError, QuestionRepository

questions_bp = Blueprint("questions", __name__, url_prefix="/api/questions")


def _repository() -> QuestionRepository:
    return current_app.extensions["question_repository"]


def _question_response(question: object, status: int = 200) -> tuple[Response, int]:
    return jsonify(question.to_dict()), status  # type: ignore[attr-defined]


def _error_response(
    message: str,
    *,
    status: int,
    field: str | None = None,
) -> tuple[Response, int]:
    return jsonify({"error": message, "field": field}), status


@questions_bp.get("")
def list_questions() -> tuple[Response, int]:
    query = request.args.get("q", "")
    repository = _repository()
    questions = repository.search(query) if query.strip() else repository.list_all()
    return jsonify({"questions": [question.to_dict() for question in questions]}), 200


@questions_bp.get("/<int:question_id>")
def get_question(question_id: int) -> tuple[Response, int]:
    try:
        question = _repository().get(question_id)
    except QuestionNotFoundError as error:
        return _error_response(str(error), status=404)
    return _question_response(question)


@questions_bp.post("")
def create_question() -> tuple[Response, int]:
    payload = request.get_json(silent=True)
    if payload is None:
        return _error_response("Request body must be valid JSON.", status=400)

    try:
        question = _repository().create(payload)
    except ValidationError as error:
        return _error_response(str(error), status=400, field=error.field)
    return _question_response(question, status=201)


@questions_bp.put("/<int:question_id>")
def update_question(question_id: int) -> tuple[Response, int]:
    payload = request.get_json(silent=True)
    if payload is None:
        return _error_response("Request body must be valid JSON.", status=400)

    try:
        question = _repository().update(question_id, payload)
    except QuestionNotFoundError as error:
        return _error_response(str(error), status=404)
    except ValidationError as error:
        return _error_response(str(error), status=400, field=error.field)
    return _question_response(question)


@questions_bp.delete("/<int:question_id>")
def delete_question(question_id: int) -> tuple[Response, int]:
    try:
        _repository().delete(question_id)
    except QuestionNotFoundError as error:
        return _error_response(str(error), status=404)
    return "", 204
