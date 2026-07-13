"""Quiz Builder HTTP routes."""

from __future__ import annotations

from flask import Blueprint, current_app, jsonify, request

from backend.models import NotFoundError, ValidationError
from backend.quiz_repository import QuizRepository

quizzes_bp = Blueprint("quizzes", __name__)


def _repo() -> QuizRepository:
    return QuizRepository(current_app.config.get("DB_PATH"))


@quizzes_bp.get("/api/quizzes")
def list_quizzes():
    return jsonify(_repo().list_quizzes())


@quizzes_bp.post("/api/quizzes")
def create_quiz():
    try:
        quiz = _repo().create_quiz(request.get_json(silent=True))
    except ValidationError as exc:
        return jsonify({"error": exc.message, "field": exc.field}), 400
    return jsonify(quiz), 201


@quizzes_bp.get("/api/quizzes/<int:quiz_id>")
def get_quiz(quiz_id: int):
    try:
        quiz = _repo().get_quiz(quiz_id)
    except NotFoundError as exc:
        return jsonify({"error": exc.message}), 404
    return jsonify(quiz)


@quizzes_bp.put("/api/quizzes/<int:quiz_id>")
def update_quiz(quiz_id: int):
    try:
        quiz = _repo().update_quiz(quiz_id, request.get_json(silent=True))
    except ValidationError as exc:
        return jsonify({"error": exc.message, "field": exc.field}), 400
    except NotFoundError as exc:
        return jsonify({"error": exc.message}), 404
    return jsonify(quiz)


@quizzes_bp.delete("/api/quizzes/<int:quiz_id>")
def delete_quiz(quiz_id: int):
    try:
        _repo().delete_quiz(quiz_id)
    except NotFoundError as exc:
        return jsonify({"error": exc.message}), 404
    return "", 204
