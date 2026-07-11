from flask import Flask, send_from_directory

from . import config
from .database import init_db
from .exam_repository import ExamAttemptRepository
from .question_repository import QuestionRepository
from .quiz_repository import QuizRepository
from .routes import exams_bp, questions_bp, quizzes_bp


def create_app(db_path=None) -> Flask:
    app = Flask(__name__, static_folder=str(config.FRONTEND_DIR), static_url_path="")

    init_db(db_path)
    app.config["QUESTION_REPOSITORY"] = QuestionRepository(db_path=db_path)
    app.config["QUIZ_REPOSITORY"] = QuizRepository(db_path=db_path)
    app.config["EXAM_REPOSITORY"] = ExamAttemptRepository(db_path=db_path)

    app.register_blueprint(questions_bp)
    app.register_blueprint(quizzes_bp)
    app.register_blueprint(exams_bp)

    @app.route("/")
    def index():
        return send_from_directory(config.FRONTEND_DIR, "index.html")

    return app
