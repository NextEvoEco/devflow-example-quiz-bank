from flask import Blueprint, jsonify, request

from backend.question_repository import QuestionNotFoundError, QuestionRepository
from backend.validation import ValidationError

questions_bp = Blueprint("questions", __name__, url_prefix="/api/questions")
repository = QuestionRepository()


@questions_bp.get("")
def list_questions():
    query = request.args.get("q", "")
    questions = repository.search(query) if query else repository.list_all()
    return jsonify({"questions": questions})


@questions_bp.get("/<int:question_id>")
def get_question(question_id: int):
    question = repository.get_by_id(question_id)
    if question is None:
        return jsonify({"error": f"Question {question_id} was not found."}), 404
    return jsonify({"question": question})


@questions_bp.post("")
def create_question():
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    try:
        question = repository.create(payload)
    except ValidationError as exc:
        return jsonify({"error": exc.message, "errors": exc.errors}), 400

    return jsonify({"question": question}), 201


@questions_bp.put("/<int:question_id>")
def update_question(question_id: int):
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    try:
        question = repository.update(question_id, payload)
    except ValidationError as exc:
        return jsonify({"error": exc.message, "errors": exc.errors}), 400
    except QuestionNotFoundError as exc:
        return jsonify({"error": str(exc)}), 404

    return jsonify({"question": question})


@questions_bp.delete("/<int:question_id>")
def delete_question(question_id: int):
    try:
        repository.delete(question_id)
    except QuestionNotFoundError as exc:
        return jsonify({"error": str(exc)}), 404

    return "", 204
