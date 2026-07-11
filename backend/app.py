from flask import Flask, send_from_directory

from backend.config import FRONTEND_DIR
from backend.db import init_database
from backend.routes.exams import exams_bp
from backend.routes.questions import questions_bp
from backend.routes.quizzes import quizzes_bp


def create_app() -> Flask:
    init_database()

    app = Flask(__name__, static_folder=None)
    app.register_blueprint(questions_bp)
    app.register_blueprint(quizzes_bp)
    app.register_blueprint(exams_bp)

    @app.get("/")
    def index():
        return send_from_directory(FRONTEND_DIR, "index.html")

    @app.get("/<path:asset_path>")
    def static_assets(asset_path: str):
        return send_from_directory(FRONTEND_DIR, asset_path)

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    return app
