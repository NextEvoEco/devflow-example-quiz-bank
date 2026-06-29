import sqlite3
from pathlib import Path
from typing import Any

from backend.database import get_connection
from backend.errors import ValidationError
from backend.models import Question, QuizDetail, QuizSummary
from backend.quiz_validation import validate_quiz_create_payload, validate_quiz_update_payload


class QuizNotFoundError(LookupError):
    pass


class QuizRepository:
    def __init__(self, db_path: Path | None = None) -> None:
        self._db_path = db_path

    def create(self, payload: dict[str, Any]) -> QuizDetail:
        data = validate_quiz_create_payload(payload)
        self._ensure_question_ids_exist(data["question_ids"])

        with get_connection(self._db_path) as connection:
            cursor = connection.execute(
                "INSERT INTO quizzes (name) VALUES (?)",
                (data["name"],),
            )
            quiz_id = cursor.lastrowid
            if quiz_id is None:
                raise RuntimeError("Failed to create quiz.")

            self._replace_quiz_questions(connection, quiz_id, data["question_ids"])
            connection.commit()

        return self.get(quiz_id)

    def list_all(self) -> list[QuizSummary]:
        with get_connection(self._db_path) as connection:
            rows = connection.execute(
                """
                SELECT
                    q.id,
                    q.name,
                    q.created_at,
                    COUNT(qq.question_id) AS question_count
                FROM quizzes q
                LEFT JOIN quiz_questions qq ON qq.quiz_id = q.id
                GROUP BY q.id, q.name, q.created_at
                ORDER BY q.id ASC
                """
            ).fetchall()
            return [self._summary_from_row(row) for row in rows]

    def get(self, quiz_id: int) -> QuizDetail:
        with get_connection(self._db_path) as connection:
            quiz_row = self._get_quiz_row(connection, quiz_id)
            if quiz_row is None:
                raise QuizNotFoundError(f"Quiz {quiz_id} was not found.")

            question_rows = connection.execute(
                """
                SELECT questions.*
                FROM quiz_questions
                JOIN questions ON questions.id = quiz_questions.question_id
                WHERE quiz_questions.quiz_id = ?
                ORDER BY quiz_questions.position ASC
                """,
                (quiz_id,),
            ).fetchall()
            questions = [Question.from_row(row) for row in question_rows]

            return QuizDetail(
                id=quiz_row["id"],
                name=quiz_row["name"],
                created_at=quiz_row["created_at"],
                question_ids=[question.id for question in questions],
                questions=questions,
            )

    def update(self, quiz_id: int, payload: dict[str, Any]) -> QuizDetail:
        data = validate_quiz_update_payload(payload)

        with get_connection(self._db_path) as connection:
            quiz_row = self._get_quiz_row(connection, quiz_id)
            if quiz_row is None:
                raise QuizNotFoundError(f"Quiz {quiz_id} was not found.")

            if "name" in data:
                connection.execute(
                    "UPDATE quizzes SET name = ? WHERE id = ?",
                    (data["name"], quiz_id),
                )

            if "question_ids" in data:
                self._ensure_question_ids_exist(data["question_ids"], connection)
                connection.execute(
                    "DELETE FROM quiz_questions WHERE quiz_id = ?",
                    (quiz_id,),
                )
                self._replace_quiz_questions(connection, quiz_id, data["question_ids"])

            connection.commit()

        return self.get(quiz_id)

    def delete(self, quiz_id: int) -> None:
        with get_connection(self._db_path) as connection:
            cursor = connection.execute("DELETE FROM quizzes WHERE id = ?", (quiz_id,))
            connection.commit()
            if cursor.rowcount == 0:
                raise QuizNotFoundError(f"Quiz {quiz_id} was not found.")

    def _ensure_question_ids_exist(
        self,
        question_ids: list[int],
        connection: sqlite3.Connection | None = None,
    ) -> None:
        if connection is None:
            with get_connection(self._db_path) as owned_connection:
                self._ensure_question_ids_exist(question_ids, owned_connection)
            return

        placeholders = ", ".join("?" for _ in question_ids)
        rows = connection.execute(
            f"SELECT id FROM questions WHERE id IN ({placeholders})",
            question_ids,
        ).fetchall()
        existing_ids = {row["id"] for row in rows}
        missing_ids = [question_id for question_id in question_ids if question_id not in existing_ids]
        if missing_ids:
            raise ValidationError(
                f"Question IDs do not exist: {', '.join(str(item) for item in missing_ids)}",
                "questionIds",
            )

    @staticmethod
    def _replace_quiz_questions(
        connection: sqlite3.Connection,
        quiz_id: int,
        question_ids: list[int],
    ) -> None:
        for position, question_id in enumerate(question_ids):
            connection.execute(
                """
                INSERT INTO quiz_questions (quiz_id, question_id, position)
                VALUES (?, ?, ?)
                """,
                (quiz_id, question_id, position),
            )

    @staticmethod
    def _get_quiz_row(
        connection: sqlite3.Connection,
        quiz_id: int,
    ) -> sqlite3.Row | None:
        return connection.execute(
            "SELECT id, name, created_at FROM quizzes WHERE id = ?",
            (quiz_id,),
        ).fetchone()

    @staticmethod
    def _summary_from_row(row: sqlite3.Row) -> QuizSummary:
        return QuizSummary(
            id=row["id"],
            name=row["name"],
            created_at=row["created_at"],
            question_count=row["question_count"],
        )
