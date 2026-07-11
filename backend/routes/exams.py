from flask import Blueprint, jsonify, request

from backend.exam_repository import (
    ExamAttemptAlreadySubmittedError,
    ExamAttemptNotFoundError,
    ExamAttemptRepository,
)
from backend.quiz_repository import QuizNotFoundError

exams_bp = Blueprint("exams", __name__, url_prefix="/api/exams")
repository = ExamAttemptRepository()

VALID_OPTIONS = {"A", "B", "C", "D"}


def _build_submit_response(attempt_id: int) -> dict:
    result = repository.get_attempt_with_answers(attempt_id)
    if result is None:
        raise ExamAttemptNotFoundError(attempt_id)

    attempt = result["attempt"]
    quiz = repository.quiz_repository.get_by_id(attempt.quiz_id)
    answers_by_question = {
        answer.question_id: answer.selected_option for answer in result["answers"]
    }

    score = 0
    questions = quiz["questions"]
    total = len(questions)
    answer_details = []

    for question in questions:
        selected_option = answers_by_question.get(question["id"])
        correct_option = question["correct"]
        is_correct = (
            selected_option is not None and selected_option == correct_option
        )
        if is_correct:
            score += 1

        answer_details.append(
            {
                "question_id": question["id"],
                "selected_option": selected_option,
                "correct_option": correct_option,
                "is_correct": is_correct,
                "question_text": question["question"],
                "a": question["a"],
                "b": question["b"],
                "c": question["c"],
                "d": question["d"],
            }
        )

    percentage = round((score / total) * 100) if total else 0
    repository.submit_attempt(attempt_id, score, total)

    return {
        "score": score,
        "total": total,
        "percentage": percentage,
        "answers": answer_details,
    }


@exams_bp.post("/attempts")
def create_attempt():
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    if "quiz_id" not in payload:
        return jsonify({"error": "quiz_id is required."}), 400

    try:
        quiz_id = int(payload["quiz_id"])
    except (TypeError, ValueError):
        return jsonify({"error": "quiz_id must be an integer."}), 400

    try:
        attempt = repository.create_attempt(quiz_id)
    except QuizNotFoundError as exc:
        return jsonify({"error": str(exc)}), 404

    return jsonify({"attempt_id": attempt.id}), 201


@exams_bp.put("/attempts/<int:attempt_id>/answers/<int:question_id>")
def save_answer(attempt_id: int, question_id: int):
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    if "selected_option" not in payload:
        return jsonify({"error": "selected_option is required."}), 400

    selected_option = payload["selected_option"]
    if selected_option is not None and selected_option not in VALID_OPTIONS:
        return jsonify({"error": "selected_option must be A, B, C, D, or null."}), 400

    result = repository.get_attempt_with_answers(attempt_id)
    if result is None:
        return jsonify({"error": f"Exam attempt {attempt_id} was not found."}), 404

    attempt = result["attempt"]
    quiz = repository.quiz_repository.get_by_id(attempt.quiz_id)
    question_ids = {question["id"] for question in quiz["questions"]}
    if question_id not in question_ids:
        return jsonify({"error": f"Question {question_id} is not part of this exam."}), 404

    try:
        repository.save_answer(attempt_id, question_id, selected_option)
    except ExamAttemptAlreadySubmittedError as exc:
        return jsonify({"error": str(exc)}), 409

    return "", 204


@exams_bp.post("/attempts/<int:attempt_id>/submit")
def submit_attempt(attempt_id: int):
    result = repository.get_attempt_with_answers(attempt_id)
    if result is None:
        return jsonify({"error": f"Exam attempt {attempt_id} was not found."}), 404

    if result["attempt"].submitted_at is not None:
        return jsonify({"error": f"Exam attempt {attempt_id} was already submitted."}), 409

    try:
        summary = _build_submit_response(attempt_id)
    except ExamAttemptAlreadySubmittedError as exc:
        return jsonify({"error": str(exc)}), 409

    return jsonify(summary)
