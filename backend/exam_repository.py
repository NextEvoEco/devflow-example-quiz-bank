from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path

from .config import DATABASE_PATH


@dataclass(slots=True)
class ExamAnswer:
    id: int
    attempt_id: int
    question_id: int
    selected_option: str | None


@dataclass(slots=True)
class ExamAttempt:
    id: int
    quiz_id: int
    score: int | None
    total: int | None
    started_at: str
    submitted_at: str | None
    answers: list[ExamAnswer]


class ExamAttemptRepository:
    """SQLite-backed persistence layer for Online Exam attempts."""

    def __init__(self, database_path: Path = DATABASE_PATH):
        self.database_path = Path(database_path)

    def create_attempt(self, quiz_id: int) -> ExamAttempt:
        with self._connect() as connection:
            cursor = connection.execute(
                "INSERT INTO exam_attempts (quiz_id) VALUES (?)",
                (quiz_id,),
            )
            attempt_id = cursor.lastrowid
            connection.commit()
        created = self.get_attempt_with_answers(attempt_id)
        assert created is not None
        return created

    def save_answer(
        self,
        attempt_id: int,
        question_id: int,
        selected_option: str | None,
    ) -> ExamAnswer:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO exam_answers (attempt_id, question_id, selected_option)
                VALUES (?, ?, ?)
                ON CONFLICT(attempt_id, question_id)
                DO UPDATE SET selected_option = excluded.selected_option
                """,
                (attempt_id, question_id, selected_option),
            )
            connection.commit()
            row = connection.execute(
                """
                SELECT id, attempt_id, question_id, selected_option
                FROM exam_answers
                WHERE attempt_id = ? AND question_id = ?
                """,
                (attempt_id, question_id),
            ).fetchone()
        assert row is not None
        return ExamAnswer(
            id=row["id"],
            attempt_id=row["attempt_id"],
            question_id=row["question_id"],
            selected_option=row["selected_option"],
        )

    def submit_attempt(self, attempt_id: int, score: int, total: int) -> ExamAttempt:
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE exam_attempts
                SET score = ?, total = ?, submitted_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (score, total, attempt_id),
            )
            connection.commit()
        submitted = self.get_attempt_with_answers(attempt_id)
        assert submitted is not None
        return submitted

    def get_attempt_with_answers(self, attempt_id: int) -> ExamAttempt | None:
        with self._connect() as connection:
            attempt_row = connection.execute(
                """
                SELECT id, quiz_id, score, total, started_at, submitted_at
                FROM exam_attempts
                WHERE id = ?
                """,
                (attempt_id,),
            ).fetchone()
            if attempt_row is None:
                return None

            answer_rows = connection.execute(
                """
                SELECT id, attempt_id, question_id, selected_option
                FROM exam_answers
                WHERE attempt_id = ?
                ORDER BY id ASC
                """,
                (attempt_id,),
            ).fetchall()

        return ExamAttempt(
            id=attempt_row["id"],
            quiz_id=attempt_row["quiz_id"],
            score=attempt_row["score"],
            total=attempt_row["total"],
            started_at=attempt_row["started_at"],
            submitted_at=attempt_row["submitted_at"],
            answers=[
                ExamAnswer(
                    id=row["id"],
                    attempt_id=row["attempt_id"],
                    question_id=row["question_id"],
                    selected_option=row["selected_option"],
                )
                for row in answer_rows
            ],
        )

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection
