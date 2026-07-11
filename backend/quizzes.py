from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path

from .config import DATABASE_PATH
from .questions import Question


class QuizValidationError(ValueError):
    """Raised when quiz data does not satisfy Quiz Builder V1 rules."""


@dataclass(slots=True)
class QuizSummary:
    id: int
    name: str
    question_count: int


@dataclass(slots=True)
class QuizDetail:
    id: int
    name: str
    question_ids: list[int]
    questions: list[Question]


def validate_quiz_payload(payload: dict) -> dict[str, object]:
    if "name" not in payload:
        raise QuizValidationError("'name' is required")
    if "question_ids" not in payload:
        raise QuizValidationError("'question_ids' is required")

    name = payload["name"]
    if not isinstance(name, str) or not name.strip():
        raise QuizValidationError("'name' must be a non-empty string")

    question_ids = payload["question_ids"]
    if not isinstance(question_ids, list):
        raise QuizValidationError("'question_ids' must be an array")
    if len(question_ids) < 3:
        raise QuizValidationError("A quiz must contain at least 3 questions")
    if len(question_ids) != len(set(question_ids)):
        raise QuizValidationError("A quiz cannot contain duplicate question IDs")
    if any(not isinstance(question_id, int) for question_id in question_ids):
        raise QuizValidationError("'question_ids' must contain integers only")

    return {
        "name": name.strip(),
        "question_ids": question_ids,
    }


class QuizRepository:
    """SQLite-backed persistence layer for Quiz Builder V1."""

    def __init__(self, database_path: Path = DATABASE_PATH):
        self.database_path = Path(database_path)

    def list_quizzes(self) -> list[QuizSummary]:
        query = """
        SELECT quizzes.id, quizzes.name, COUNT(quiz_questions.question_id) AS question_count
        FROM quizzes
        LEFT JOIN quiz_questions ON quiz_questions.quiz_id = quizzes.id
        GROUP BY quizzes.id, quizzes.name
        ORDER BY quizzes.id DESC
        """
        with self._connect() as connection:
            rows = connection.execute(query).fetchall()
        return [
            QuizSummary(
                id=row["id"],
                name=row["name"],
                question_count=row["question_count"],
            )
            for row in rows
        ]

    def get_quiz(self, quiz_id: int) -> QuizDetail | None:
        query = """
        SELECT
            quizzes.id AS quiz_id,
            quizzes.name AS quiz_name,
            questions.id AS question_id,
            questions.question,
            questions.option_a,
            questions.option_b,
            questions.option_c,
            questions.option_d,
            questions.correct AS correct_answer,
            questions.difficulty,
            quiz_questions.position
        FROM quizzes
        LEFT JOIN quiz_questions ON quiz_questions.quiz_id = quizzes.id
        LEFT JOIN questions ON questions.id = quiz_questions.question_id
        WHERE quizzes.id = ?
        ORDER BY quiz_questions.position ASC
        """
        with self._connect() as connection:
            rows = connection.execute(query, (quiz_id,)).fetchall()
        if not rows:
            return None

        question_ids: list[int] = []
        questions: list[Question] = []
        for row in rows:
            if row["question_id"] is None:
                continue
            question_ids.append(row["question_id"])
            questions.append(
                Question(
                    id=row["question_id"],
                    question=row["question"],
                    option_a=row["option_a"],
                    option_b=row["option_b"],
                    option_c=row["option_c"],
                    option_d=row["option_d"],
                    correct_answer=row["correct_answer"],
                    difficulty=row["difficulty"],
                )
            )

        return QuizDetail(
            id=rows[0]["quiz_id"],
            name=rows[0]["quiz_name"],
            question_ids=question_ids,
            questions=questions,
        )

    def create_quiz(self, payload: dict) -> QuizDetail:
        record = validate_quiz_payload(payload)
        question_ids = record["question_ids"]
        assert isinstance(question_ids, list)

        with self._connect() as connection:
            self._validate_question_ids(connection, question_ids)
            cursor = connection.execute(
                "INSERT INTO quizzes (name) VALUES (?)",
                (record["name"],),
            )
            quiz_id = cursor.lastrowid
            self._replace_quiz_questions(connection, quiz_id, question_ids)
            connection.commit()

        created = self.get_quiz(quiz_id)
        assert created is not None
        return created

    def update_quiz(self, quiz_id: int, payload: dict) -> QuizDetail:
        record = validate_quiz_payload(payload)
        question_ids = record["question_ids"]
        assert isinstance(question_ids, list)

        with self._connect() as connection:
            existing = connection.execute(
                "SELECT id FROM quizzes WHERE id = ?",
                (quiz_id,),
            ).fetchone()
            if existing is None:
                raise KeyError(f"Quiz {quiz_id} does not exist")

            self._validate_question_ids(connection, question_ids)
            connection.execute(
                "UPDATE quizzes SET name = ? WHERE id = ?",
                (record["name"], quiz_id),
            )
            self._replace_quiz_questions(connection, quiz_id, question_ids)
            connection.commit()

        updated = self.get_quiz(quiz_id)
        assert updated is not None
        return updated

    def delete_quiz(self, quiz_id: int) -> bool:
        with self._connect() as connection:
            cursor = connection.execute("DELETE FROM quizzes WHERE id = ?", (quiz_id,))
            connection.commit()
        return cursor.rowcount > 0

    def _replace_quiz_questions(
        self,
        connection: sqlite3.Connection,
        quiz_id: int,
        question_ids: list[int],
    ) -> None:
        connection.execute("DELETE FROM quiz_questions WHERE quiz_id = ?", (quiz_id,))
        connection.executemany(
            """
            INSERT INTO quiz_questions (quiz_id, question_id, position)
            VALUES (?, ?, ?)
            """,
            [
                (quiz_id, question_id, position)
                for position, question_id in enumerate(question_ids, start=1)
            ],
        )

    def _validate_question_ids(
        self,
        connection: sqlite3.Connection,
        question_ids: list[int],
    ) -> None:
        placeholders = ", ".join("?" for _ in question_ids)
        rows = connection.execute(
            f"SELECT id FROM questions WHERE id IN ({placeholders})",
            question_ids,
        ).fetchall()
        found_ids = {row["id"] for row in rows}
        missing = [question_id for question_id in question_ids if question_id not in found_ids]
        if missing:
            raise QuizValidationError(
                f"Question IDs do not exist: {', '.join(str(item) for item in missing)}"
            )

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection
