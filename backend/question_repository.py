from .database import get_connection
from .models import question_from_row
from .validation import validate_question

_COLUMNS = "id, question, option_a, option_b, option_c, option_d, correct, difficulty"


class QuestionRepository:
    """SQLite persistence for questions.

    All mutating operations validate their payload through
    ``validate_question`` so the storage layer is the single source of truth
    for question integrity, independent of any HTTP or frontend layer.
    """

    def __init__(self, db_path=None):
        self.db_path = db_path

    def _connect(self):
        return get_connection(self.db_path)

    def create(self, payload: dict) -> dict:
        data = validate_question(payload)
        conn = self._connect()
        try:
            cursor = conn.execute(
                """
                INSERT INTO questions
                    (question, option_a, option_b, option_c, option_d, correct, difficulty)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    data["question"],
                    data["a"],
                    data["b"],
                    data["c"],
                    data["d"],
                    data["correct"],
                    data["difficulty"],
                ),
            )
            new_id = cursor.lastrowid
            conn.commit()
        finally:
            conn.close()
        return self.get(new_id)

    def get(self, question_id: int):
        conn = self._connect()
        try:
            row = conn.execute(
                f"SELECT {_COLUMNS} FROM questions WHERE id = ?",
                (question_id,),
            ).fetchone()
        finally:
            conn.close()
        return question_from_row(row).to_dict() if row else None

    def list(self, search: str = None) -> list:
        query = f"SELECT {_COLUMNS} FROM questions"
        params = ()
        if search and search.strip():
            # LIKE is case-insensitive for ASCII in SQLite by default.
            query += " WHERE question LIKE ?"
            params = (f"%{search.strip()}%",)
        query += " ORDER BY id"

        conn = self._connect()
        try:
            rows = conn.execute(query, params).fetchall()
        finally:
            conn.close()
        return [question_from_row(row).to_dict() for row in rows]

    def update(self, question_id: int, payload: dict):
        data = validate_question(payload)
        conn = self._connect()
        try:
            cursor = conn.execute(
                """
                UPDATE questions
                   SET question = ?, option_a = ?, option_b = ?, option_c = ?,
                       option_d = ?, correct = ?, difficulty = ?
                 WHERE id = ?
                """,
                (
                    data["question"],
                    data["a"],
                    data["b"],
                    data["c"],
                    data["d"],
                    data["correct"],
                    data["difficulty"],
                    question_id,
                ),
            )
            conn.commit()
            changed = cursor.rowcount
        finally:
            conn.close()
        if changed == 0:
            return None
        return self.get(question_id)

    def delete(self, question_id: int) -> bool:
        conn = self._connect()
        try:
            cursor = conn.execute(
                "DELETE FROM questions WHERE id = ?",
                (question_id,),
            )
            conn.commit()
            deleted = cursor.rowcount
        finally:
            conn.close()
        return deleted > 0
