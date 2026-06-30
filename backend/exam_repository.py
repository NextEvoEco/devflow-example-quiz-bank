import sqlite3
from pathlib import Path

from backend.database import get_connection
from backend.models import ExamAnswer, ExamAttempt, ExamAttemptWithAnswers


class ExamAttemptNotFoundError(LookupError):
    pass


class ExamAttemptRepository:
    def __init__(self, db_path: Path | None = None) -> None:
        self._db_path = db_path

    def create_attempt(self, quiz_id: int) -> ExamAttempt:
        with get_connection(self._db_path) as connection:
            cursor = connection.execute(
                "INSERT INTO exam_attempts (quiz_id) VALUES (?)",
                (quiz_id,),
            )
            connection.commit()
            attempt_id = cursor.lastrowid
            if attempt_id is None:
                raise RuntimeError("Failed to create exam attempt.")

            row = self._get_attempt_row(connection, attempt_id)
            if row is None:
                raise RuntimeError("Created exam attempt could not be loaded.")
            return ExamAttempt.from_row(row)

    def save_answer(
        self,
        attempt_id: int,
        question_id: int,
        selected_option: str | None,
    ) -> None:
        with get_connection(self._db_path) as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO exam_answers (
                    id, attempt_id, question_id, selected_option
                )
                VALUES (
                    (
                        SELECT id FROM exam_answers
                        WHERE attempt_id = ? AND question_id = ?
                    ),
                    ?, ?, ?
                )
                """,
                (attempt_id, question_id, attempt_id, question_id, selected_option),
            )
            connection.commit()

    def get_attempt_with_answers(self, attempt_id: int) -> ExamAttemptWithAnswers:
        with get_connection(self._db_path) as connection:
            attempt_row = self._get_attempt_row(connection, attempt_id)
            if attempt_row is None:
                raise ExamAttemptNotFoundError(f"Exam attempt {attempt_id} was not found.")

            answer_rows = connection.execute(
                """
                SELECT * FROM exam_answers
                WHERE attempt_id = ?
                ORDER BY question_id ASC
                """,
                (attempt_id,),
            ).fetchall()

            return ExamAttemptWithAnswers(
                attempt=ExamAttempt.from_row(attempt_row),
                answers=[ExamAnswer.from_row(row) for row in answer_rows],
            )

    def submit_attempt(self, attempt_id: int, score: int, total: int) -> ExamAttempt:
        with get_connection(self._db_path) as connection:
            cursor = connection.execute(
                """
                UPDATE exam_attempts
                SET score = ?, total = ?, submitted_at = datetime('now')
                WHERE id = ?
                """,
                (score, total, attempt_id),
            )
            connection.commit()
            if cursor.rowcount == 0:
                raise ExamAttemptNotFoundError(f"Exam attempt {attempt_id} was not found.")

            row = self._get_attempt_row(connection, attempt_id)
            if row is None:
                raise ExamAttemptNotFoundError(f"Exam attempt {attempt_id} was not found.")
            return ExamAttempt.from_row(row)

    @staticmethod
    def _get_attempt_row(
        connection: sqlite3.Connection,
        attempt_id: int,
    ) -> sqlite3.Row | None:
        return connection.execute(
            "SELECT * FROM exam_attempts WHERE id = ?",
            (attempt_id,),
        ).fetchone()
