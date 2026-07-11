from flask import Blueprint, current_app, jsonify, request

exams_bp = Blueprint("exams", __name__, url_prefix="/api/exams")

VALID_OPTIONS = ("A", "B", "C", "D")


def _exam_repo():
    return current_app.config["EXAM_REPOSITORY"]


def _quiz_repo():
    return current_app.config["QUIZ_REPOSITORY"]


@exams_bp.post("/attempts")
def create_attempt():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict) or "quiz_id" not in payload:
        return jsonify({"error": "quiz_id is required"}), 400

    quiz_id = payload.get("quiz_id")
    if not isinstance(quiz_id, int) or isinstance(quiz_id, bool):
        return jsonify({"error": "quiz_id must be an integer"}), 400

    if _quiz_repo().get(quiz_id) is None:
        return jsonify({"error": "Quiz not found"}), 404

    attempt = _exam_repo().create_attempt(quiz_id)
    return jsonify({"attempt_id": attempt["id"]}), 201


@exams_bp.put("/attempts/<int:attempt_id>/answers/<int:question_id>")
def save_answer(attempt_id: int, question_id: int):
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "Request body must be JSON"}), 400

    selected = payload.get("selected_option")
    selected = selected.strip().upper() if isinstance(selected, str) else selected
    if selected not in VALID_OPTIONS:
        return jsonify({"error": "selected_option must be one of A, B, C, D"}), 400

    attempt = _exam_repo().get_attempt(attempt_id)
    if attempt is None:
        return jsonify({"error": "Attempt not found"}), 404

    # The question must belong to the attempt's quiz.
    quiz = _quiz_repo().get(attempt["quiz_id"])
    if quiz is None or question_id not in quiz["questionIds"]:
        return jsonify({"error": "Question not found in this exam"}), 404

    _exam_repo().save_answer(attempt_id, question_id, selected)
    return "", 204


@exams_bp.post("/attempts/<int:attempt_id>/submit")
def submit_attempt(attempt_id: int):
    exam_repo = _exam_repo()

    attempt = exam_repo.get_attempt(attempt_id)
    if attempt is None:
        return jsonify({"error": "Attempt not found"}), 404
    if attempt["submitted_at"] is not None:
        return jsonify({"error": "Attempt already submitted"}), 409

    quiz = _quiz_repo().get(attempt["quiz_id"])
    if quiz is None:
        return jsonify({"error": "Quiz not found"}), 404

    detail = exam_repo.get_attempt_with_answers(attempt_id)
    answers_map = {a["question_id"]: a["selected_option"] for a in detail["answers"]}

    review = []
    score = 0
    for question in quiz["questions"]:
        selected = answers_map.get(question["id"])
        correct = question["correct"]
        is_correct = selected == correct
        if is_correct:
            score += 1
        review.append(
            {
                "question_id": question["id"],
                "question_text": question["question"],
                "options": {
                    "A": question["a"],
                    "B": question["b"],
                    "C": question["c"],
                    "D": question["d"],
                },
                "selected_option": selected,
                "correct_option": correct,
                "is_correct": is_correct,
            }
        )

    total = len(quiz["questions"])
    percentage = round(score / total * 100) if total else 0

    exam_repo.submit_attempt(attempt_id, score, total)

    return jsonify(
        {"score": score, "total": total, "percentage": percentage, "answers": review}
    ), 200
