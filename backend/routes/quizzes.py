from flask import Blueprint, current_app, jsonify, request

from ..validation import ValidationError

quizzes_bp = Blueprint("quizzes", __name__, url_prefix="/api/quizzes")


def _repo():
    return current_app.config["QUIZ_REPOSITORY"]


@quizzes_bp.get("")
def list_quizzes():
    return jsonify(_repo().list()), 200


@quizzes_bp.get("/<int:quiz_id>")
def get_quiz(quiz_id: int):
    quiz = _repo().get(quiz_id)
    if quiz is None:
        return jsonify({"error": "Quiz not found"}), 404
    return jsonify(quiz), 200


@quizzes_bp.post("")
def create_quiz():
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Request body must be JSON"}), 400
    try:
        created = _repo().create(payload)
    except ValidationError as exc:
        return jsonify({"error": "Validation failed", "fields": exc.errors}), 400
    return jsonify(created), 201


@quizzes_bp.put("/<int:quiz_id>")
def update_quiz(quiz_id: int):
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Request body must be JSON"}), 400
    try:
        updated = _repo().update(quiz_id, payload)
    except ValidationError as exc:
        return jsonify({"error": "Validation failed", "fields": exc.errors}), 400
    if updated is None:
        return jsonify({"error": "Quiz not found"}), 404
    return jsonify(updated), 200


@quizzes_bp.delete("/<int:quiz_id>")
def delete_quiz(quiz_id: int):
    if not _repo().delete(quiz_id):
        return jsonify({"error": "Quiz not found"}), 404
    return "", 204
