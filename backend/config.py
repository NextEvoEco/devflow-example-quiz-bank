from __future__ import annotations

from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
DATABASE_PATH = DATA_DIR / "quiz_bank.db"
FRONTEND_DIR = ROOT_DIR / "frontend"

