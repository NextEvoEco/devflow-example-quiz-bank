from __future__ import annotations

from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from .config import DATABASE_PATH, FRONTEND_DIR
from .db import initialize_database
from .questions import Question, QuestionRepository, QuestionValidationError
from .quizzes import QuizDetail, QuizRepository, QuizSummary, QuizValidationError
from .routes.exams import exams_bp


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(
        __name__,
        static_folder=str(FRONTEND_DIR),
        static_url_path="",
    )

    app.config.update(
        DATABASE_PATH=str(DATABASE_PATH),
        TESTING=False,
    )

    if test_config:
        app.config.update(test_config)

    initialize_database(Path(app.config["DATABASE_PATH"]))
    app.register_blueprint(exams_bp)
    question_repository = QuestionRepository(Path(app.config["DATABASE_PATH"]))
    quiz_repository = QuizRepository(Path(app.config["DATABASE_PATH"]))

    def serialize_question(question: Question) -> dict[str, str | int]:
        return {
            "id": question.id,
            "question": question.question,
            "a": question.option_a,
            "b": question.option_b,
            "c": question.option_c,
            "d": question.option_d,
            "correct": question.correct_answer,
            "difficulty": question.difficulty,
        }

    def serialize_quiz_summary(quiz: QuizSummary) -> dict[str, str | int]:
        return {
            "id": quiz.id,
            "name": quiz.name,
            "questionCount": quiz.question_count,
        }

    def serialize_quiz_detail(quiz: QuizDetail) -> dict[str, object]:
        return {
            "id": quiz.id,
            "name": quiz.name,
            "questionIds": quiz.question_ids,
            "questions": [serialize_question(question) for question in quiz.questions],
        }

    def parse_question_payload() -> dict:
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            raise QuestionValidationError("Request body must be a JSON object")

        field_map = {
            "question": "question",
            "a": "option_a",
            "b": "option_b",
            "c": "option_c",
            "d": "option_d",
            "correct": "correct_answer",
            "difficulty": "difficulty",
        }
        normalized_payload = {}
        for source_field, target_field in field_map.items():
            if source_field in payload:
                normalized_payload[target_field] = payload[source_field]
        return normalized_payload

    def parse_quiz_payload() -> dict:
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            raise QuizValidationError("Request body must be a JSON object")

        normalized_payload = {}
        if "name" in payload:
            normalized_payload["name"] = payload["name"]
        if "questionIds" in payload:
            normalized_payload["question_ids"] = payload["questionIds"]
        return normalized_payload

    @app.get("/health")
    def healthcheck():
        return jsonify(
            {
                "status": "ok",
                "database_path": app.config["DATABASE_PATH"],
            }
        )

    @app.get("/")
    def index():
        return send_from_directory(app.static_folder, "index.html")

    @app.get("/api/questions")
    def list_questions():
        search_term = request.args.get("q", "")
        questions = question_repository.search_questions(search_term)
        return jsonify({"items": [serialize_question(question) for question in questions]})

    @app.post("/api/questions")
    def create_question():
        payload = parse_question_payload()
        question = question_repository.create_question(payload)
        return jsonify(serialize_question(question)), 201

    @app.put("/api/questions/<int:question_id>")
    def update_question(question_id: int):
        payload = parse_question_payload()
        question = question_repository.update_question(question_id, payload)
        return jsonify(serialize_question(question))

    @app.delete("/api/questions/<int:question_id>")
    def delete_question(question_id: int):
        deleted = question_repository.delete_question(question_id)
        if not deleted:
            return jsonify({"error": f"Question {question_id} not found"}), 404
        return jsonify({"deleted": True, "id": question_id})

    @app.get("/api/quizzes")
    def list_quizzes():
        quizzes = quiz_repository.list_quizzes()
        return jsonify({"items": [serialize_quiz_summary(quiz) for quiz in quizzes]})

    @app.post("/api/quizzes")
    def create_quiz():
        payload = parse_quiz_payload()
        quiz = quiz_repository.create_quiz(payload)
        return jsonify(serialize_quiz_detail(quiz)), 201

    @app.get("/api/quizzes/<int:quiz_id>")
    def get_quiz(quiz_id: int):
        quiz = quiz_repository.get_quiz(quiz_id)
        if quiz is None:
            return jsonify({"error": f"Quiz {quiz_id} not found"}), 404
        return jsonify(serialize_quiz_detail(quiz))

    @app.put("/api/quizzes/<int:quiz_id>")
    def update_quiz(quiz_id: int):
        payload = parse_quiz_payload()
        quiz = quiz_repository.update_quiz(quiz_id, payload)
        return jsonify(serialize_quiz_detail(quiz))

    @app.delete("/api/quizzes/<int:quiz_id>")
    def delete_quiz(quiz_id: int):
        deleted = quiz_repository.delete_quiz(quiz_id)
        if not deleted:
            return jsonify({"error": f"Quiz {quiz_id} not found"}), 404
        return jsonify({"deleted": True, "id": quiz_id})

    @app.errorhandler(QuestionValidationError)
    def handle_question_validation_error(error: QuestionValidationError):
        return jsonify({"error": str(error)}), 400

    @app.errorhandler(QuizValidationError)
    def handle_quiz_validation_error(error: QuizValidationError):
        return jsonify({"error": str(error)}), 400

    @app.errorhandler(KeyError)
    def handle_key_error(error: KeyError):
        return jsonify({"error": error.args[0]}), 404

    return app
