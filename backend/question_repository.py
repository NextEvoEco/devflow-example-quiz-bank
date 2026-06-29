import sqlite3
from pathlib import Path
from typing import Any

from backend.database import get_connection
from backend.errors import ValidationError
from backend.models import Question
from backend.validation import validate_question_payload


class QuestionNotFoundError(LookupError):
    pass


class QuestionRepository:
    def __init__(self, db_path: Path | None = None) -> None:
        self._db_path = db_path

    def create(self, payload: dict[str, Any]) -> Question:
        data = validate_question_payload(payload, require_all_fields=True)
        with get_connection(self._db_path) as connection:
            cursor = connection.execute(
                """
                INSERT INTO questions (
                    question, option_a, option_b, option_c, option_d, correct, difficulty
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
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
            connection.commit()
            question_id = cursor.lastrowid
            if question_id is None:
                raise RuntimeError("Failed to create question.")

            row = self._get_row(connection, question_id)
            if row is None:
                raise RuntimeError("Created question could not be loaded.")
            return Question.from_row(row)

    def get(self, question_id: int) -> Question:
        with get_connection(self._db_path) as connection:
            row = self._get_row(connection, question_id)
            if row is None:
                raise QuestionNotFoundError(f"Question {question_id} was not found.")
            return Question.from_row(row)

    def list_all(self) -> list[Question]:
        with get_connection(self._db_path) as connection:
            rows = connection.execute(
                "SELECT * FROM questions ORDER BY id ASC"
            ).fetchall()
            return [Question.from_row(row) for row in rows]

    def search(self, query: str) -> list[Question]:
        normalized_query = query.strip().lower()
        if not normalized_query:
            return self.list_all()

        with get_connection(self._db_path) as connection:
            rows = connection.execute(
                """
                SELECT * FROM questions
                WHERE LOWER(question) LIKE ?
                ORDER BY id ASC
                """,
                (f"%{normalized_query}%",),
            ).fetchall()
            return [Question.from_row(row) for row in rows]

    def update(self, question_id: int, payload: dict[str, Any]) -> Question:
        existing = self.get(question_id)
        data = validate_question_payload(
            payload,
            require_all_fields=False,
        )

        if not data:
            raise ValidationError("At least one field must be provided for update.")

        merged = existing.to_dict()
        merged.update(data)
        validated = validate_question_payload(merged, require_all_fields=True)

        with get_connection(self._db_path) as connection:
            connection.execute(
                """
                UPDATE questions
                SET question = ?, option_a = ?, option_b = ?, option_c = ?, option_d = ?,
                    correct = ?, difficulty = ?, updated_at = datetime('now')
                WHERE id = ?
                """,
                (
                    validated["question"],
                    validated["a"],
                    validated["b"],
                    validated["c"],
                    validated["d"],
                    validated["correct"],
                    validated["difficulty"],
                    question_id,
                ),
            )
            connection.commit()
            row = self._get_row(connection, question_id)
            if row is None:
                raise QuestionNotFoundError(f"Question {question_id} was not found.")
            return Question.from_row(row)

    def delete(self, question_id: int) -> None:
        with get_connection(self._db_path) as connection:
            cursor = connection.execute(
                "DELETE FROM questions WHERE id = ?",
                (question_id,),
            )
            connection.commit()
            if cursor.rowcount == 0:
                raise QuestionNotFoundError(f"Question {question_id} was not found.")

    @staticmethod
    def _get_row(
        connection: sqlite3.Connection,
        question_id: int,
    ) -> sqlite3.Row | None:
        return connection.execute(
            "SELECT * FROM questions WHERE id = ?",
            (question_id,),
        ).fetchone()
