from flask import Blueprint, current_app, jsonify, request

from ..validation import ValidationError

questions_bp = Blueprint("questions", __name__, url_prefix="/api/questions")


def _repo():
    return current_app.config["QUESTION_REPOSITORY"]


@questions_bp.get("")
def list_questions():
    search = request.args.get("search")
    return jsonify(_repo().list(search=search)), 200


@questions_bp.get("/<int:question_id>")
def get_question(question_id: int):
    question = _repo().get(question_id)
    if question is None:
        return jsonify({"error": "Question not found"}), 404
    return jsonify(question), 200


@questions_bp.post("")
def create_question():
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Request body must be JSON"}), 400
    try:
        created = _repo().create(payload)
    except ValidationError as exc:
        return jsonify({"error": "Validation failed", "fields": exc.errors}), 400
    return jsonify(created), 201


@questions_bp.put("/<int:question_id>")
def update_question(question_id: int):
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Request body must be JSON"}), 400
    try:
        updated = _repo().update(question_id, payload)
    except ValidationError as exc:
        return jsonify({"error": "Validation failed", "fields": exc.errors}), 400
    if updated is None:
        return jsonify({"error": "Question not found"}), 404
    return jsonify(updated), 200


@questions_bp.delete("/<int:question_id>")
def delete_question(question_id: int):
    if not _repo().delete(question_id):
        return jsonify({"error": "Question not found"}), 404
    return "", 204
