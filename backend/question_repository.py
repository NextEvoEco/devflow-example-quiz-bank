from backend.db import get_connection
from backend.validation import validate_question_payload


class QuestionNotFoundError(Exception):
    def __init__(self, question_id: int):
        super().__init__(f"Question {question_id} was not found.")
        self.question_id = question_id


def _row_to_dict(row) -> dict:
    return {
        "id": row["id"],
        "question": row["question"],
        "a": row["option_a"],
        "b": row["option_b"],
        "c": row["option_c"],
        "d": row["option_d"],
        "correct": row["correct"],
        "difficulty": row["difficulty"],
    }


class QuestionRepository:
    def create(self, payload: dict) -> dict:
        validated = validate_question_payload(payload)
        with get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO questions (
                    question, option_a, option_b, option_c, option_d, correct, difficulty
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    validated["question"],
                    validated["a"],
                    validated["b"],
                    validated["c"],
                    validated["d"],
                    validated["correct"],
                    validated["difficulty"],
                ),
            )
            connection.commit()
            question_id = cursor.lastrowid

        created = self.get_by_id(question_id)
        if created is None:
            raise RuntimeError("Failed to load question after creation.")
        return created

    def get_by_id(self, question_id: int) -> dict | None:
        with get_connection() as connection:
            row = connection.execute(
                "SELECT * FROM questions WHERE id = ?",
                (question_id,),
            ).fetchone()
        return _row_to_dict(row) if row else None

    def list_all(self) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute(
                "SELECT * FROM questions ORDER BY id ASC"
            ).fetchall()
        return [_row_to_dict(row) for row in rows]

    def search(self, query: str) -> list[dict]:
        normalized_query = query.strip().lower()
        if not normalized_query:
            return self.list_all()

        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT * FROM questions
                WHERE lower(question) LIKE '%' || ? || '%'
                ORDER BY id ASC
                """,
                (normalized_query,),
            ).fetchall()
        return [_row_to_dict(row) for row in rows]

    def update(self, question_id: int, payload: dict) -> dict:
        existing = self.get_by_id(question_id)
        if existing is None:
            raise QuestionNotFoundError(question_id)

        validated = validate_question_payload(payload, partial=False)
        with get_connection() as connection:
            updated = connection.execute(
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
            if updated.rowcount == 0:
                raise QuestionNotFoundError(question_id)

        updated_question = self.get_by_id(question_id)
        if updated_question is None:
            raise QuestionNotFoundError(question_id)
        return updated_question

    def delete(self, question_id: int) -> None:
        with get_connection() as connection:
            deleted = connection.execute(
                "DELETE FROM questions WHERE id = ?",
                (question_id,),
            )
            connection.commit()
            if deleted.rowcount == 0:
                raise QuestionNotFoundError(question_id)
