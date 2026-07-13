"""Application configuration."""

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
DATABASE_PATH = DATA_DIR / "quiz_bank.db"
FRONTEND_DIST = ROOT_DIR / "frontend" / "dist"
HOST = "127.0.0.1"
PORT = 5000
