from pathlib import Path

from flask import Flask, send_from_directory

from backend.config import FRONTEND_DIR
from backend.database import initialize_database
from backend.question_repository import QuestionRepository
from backend.quiz_repository import QuizRepository
from backend.routes.questions import questions_bp
from backend.routes.quizzes import quizzes_bp


def create_app(db_path: Path | None = None) -> Flask:
    initialize_database(db_path)

    app = Flask(
        __name__,
        static_folder=str(FRONTEND_DIR),
        static_url_path="",
    )
    app.extensions["question_repository"] = QuestionRepository(db_path)
    app.extensions["quiz_repository"] = QuizRepository(db_path)

    app.register_blueprint(questions_bp)
    app.register_blueprint(quizzes_bp)

    @app.get("/")
    def index() -> object:
        return send_from_directory(FRONTEND_DIR, "index.html")

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/<path:asset_path>")
    def static_asset(asset_path: str) -> object:
        target = FRONTEND_DIR / asset_path
        if target.is_file():
            return send_from_directory(FRONTEND_DIR, asset_path)
        return send_from_directory(FRONTEND_DIR, "index.html")

    return app
