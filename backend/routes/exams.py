"""Online Exam HTTP routes."""

from __future__ import annotations

from flask import Blueprint, current_app, jsonify, request

from backend.exam_repository import ExamAttemptRepository
from backend.models import NotFoundError, ValidationError

exams_bp = Blueprint("exams", __name__)


def _repo() -> ExamAttemptRepository:
    return ExamAttemptRepository(current_app.config.get("DB_PATH"))


@exams_bp.post("/api/exams/attempts")
def create_attempt():
    data = request.get_json(silent=True) or {}
    quiz_id = data.get("quiz_id")
    if quiz_id is None:
        return jsonify({"error": "quiz_id is required", "field": "quiz_id"}), 400
    try:
        attempt = _repo().create_attempt(int(quiz_id))
    except (TypeError, ValueError):
        return jsonify({"error": "quiz_id must be an integer", "field": "quiz_id"}), 400
    except NotFoundError as exc:
        return jsonify({"error": exc.message}), 404
    return jsonify({"attempt_id": attempt.id, "quiz_id": attempt.quiz_id}), 201


@exams_bp.put("/api/exams/attempts/<int:attempt_id>/answers/<int:question_id>")
def save_answer(attempt_id: int, question_id: int):
    data = request.get_json(silent=True) or {}
    selected = data.get("selected_option")
    try:
        _repo().save_answer(attempt_id, question_id, selected)
    except NotFoundError as exc:
        return jsonify({"error": exc.message}), 404
    except ValidationError as exc:
        return jsonify({"error": exc.message, "field": exc.field}), 400
    return "", 204


@exams_bp.post("/api/exams/attempts/<int:attempt_id>/submit")
def submit_attempt(attempt_id: int):
    try:
        result = _repo().score_attempt(attempt_id)
    except NotFoundError as exc:
        return jsonify({"error": exc.message}), 404
    except ValidationError as exc:
        status = 409 if "already submitted" in exc.message.lower() else 400
        return jsonify({"error": exc.message}), status
    return jsonify(result)
