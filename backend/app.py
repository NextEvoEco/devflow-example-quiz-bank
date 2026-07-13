"""Flask application factory."""

from __future__ import annotations

from pathlib import Path

from flask import Flask, abort, send_from_directory

from backend.config import FRONTEND_DIST
from backend.database import initialize_database
from backend.routes.exams import exams_bp
from backend.routes.questions import questions_bp
from backend.routes.quizzes import quizzes_bp


def create_app(db_path: Path | str | None = None) -> Flask:
    initialize_database(db_path)

    # Avoid static_url_path="" which registers /<filename> and can conflict with APIs.
    app = Flask(__name__)
    app.config["DB_PATH"] = db_path
    app.register_blueprint(questions_bp)
    app.register_blueprint(quizzes_bp)
    app.register_blueprint(exams_bp)

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    @app.get("/assets/<path:filename>")
    def dist_assets(filename: str):
        assets_dir = FRONTEND_DIST / "assets"
        if not assets_dir.exists():
            abort(404)
        return send_from_directory(assets_dir, filename)

    @app.get("/")
    def index():
        index_path = FRONTEND_DIST / "index.html"
        if index_path.exists():
            return send_from_directory(FRONTEND_DIST, "index.html")
        return (
            "<!DOCTYPE html><html><head><title>Quiz Bank</title></head>"
            "<body><h1>Quiz Bank</h1>"
            "<p>Frontend build not found. Run <code>npm run build</code> "
            "in <code>frontend/</code>.</p></body></html>",
            200,
            {"Content-Type": "text/html; charset=utf-8"},
        )

    return app
