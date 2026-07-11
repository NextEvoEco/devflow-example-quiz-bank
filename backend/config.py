from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATABASE_PATH = DATA_DIR / "quiz_bank.db"
FRONTEND_DIR = PROJECT_ROOT / "frontend"

HOST = "127.0.0.1"
PORT = 5000
