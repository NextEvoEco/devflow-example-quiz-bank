from flask import Blueprint, jsonify, request

from backend.quiz_repository import QuizNotFoundError, QuizRepository
from backend.quiz_validation import QuizValidationError

quizzes_bp = Blueprint("quizzes", __name__, url_prefix="/api/quizzes")
repository = QuizRepository()


@quizzes_bp.get("")
def list_quizzes():
    quizzes = repository.list_all()
    return jsonify({"quizzes": quizzes})


@quizzes_bp.get("/<int:quiz_id>")
def get_quiz(quiz_id: int):
    quiz = repository.get_by_id(quiz_id)
    if quiz is None:
        return jsonify({"error": f"Quiz {quiz_id} was not found."}), 404
    return jsonify({"quiz": quiz})


@quizzes_bp.post("")
def create_quiz():
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    try:
        quiz = repository.create(payload)
    except QuizValidationError as exc:
        return jsonify({"error": exc.message, "errors": exc.errors}), 400

    return jsonify({"quiz": quiz}), 201


@quizzes_bp.put("/<int:quiz_id>")
def update_quiz(quiz_id: int):
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    try:
        quiz = repository.update(quiz_id, payload)
    except QuizValidationError as exc:
        return jsonify({"error": exc.message, "errors": exc.errors}), 400
    except QuizNotFoundError as exc:
        return jsonify({"error": str(exc)}), 404

    return jsonify({"quiz": quiz})


@quizzes_bp.delete("/<int:quiz_id>")
def delete_quiz(quiz_id: int):
    try:
        repository.delete(quiz_id)
    except QuizNotFoundError as exc:
        return jsonify({"error": str(exc)}), 404

    return "", 204
