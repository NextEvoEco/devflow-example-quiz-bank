"""Question Bank HTTP routes."""

from __future__ import annotations

from flask import Blueprint, current_app, jsonify, request

from backend.models import NotFoundError, ValidationError
from backend.question_repository import QuestionRepository

questions_bp = Blueprint("questions", __name__)


def _repo() -> QuestionRepository:
    return QuestionRepository(current_app.config.get("DB_PATH"))


@questions_bp.get("/api/questions")
def list_questions():
    search = request.args.get("q") or request.args.get("search")
    items = _repo().list_questions(search=search)
    return jsonify([q.to_dict() for q in items])


@questions_bp.get("/api/questions/<int:question_id>")
def get_question(question_id: int):
    try:
        question = _repo().get_question(question_id)
    except NotFoundError as exc:
        return jsonify({"error": exc.message}), 404
    return jsonify(question.to_dict())


@questions_bp.post("/api/questions")
def create_question():
    try:
        question = _repo().create_question(request.get_json(silent=True))
    except ValidationError as exc:
        return jsonify({"error": exc.message, "field": exc.field}), 400
    return jsonify(question.to_dict()), 201


@questions_bp.put("/api/questions/<int:question_id>")
def update_question(question_id: int):
    try:
        question = _repo().update_question(
            question_id, request.get_json(silent=True)
        )
    except ValidationError as exc:
        return jsonify({"error": exc.message, "field": exc.field}), 400
    except NotFoundError as exc:
        return jsonify({"error": exc.message}), 404
    return jsonify(question.to_dict())


@questions_bp.delete("/api/questions/<int:question_id>")
def delete_question(question_id: int):
    try:
        _repo().delete_question(question_id)
    except NotFoundError as exc:
        return jsonify({"error": exc.message}), 404
    return "", 204
