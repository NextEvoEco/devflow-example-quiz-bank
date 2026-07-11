from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path

from .config import DATABASE_PATH


DEFAULT_DIFFICULTY = "Medium"
ALLOWED_DIFFICULTIES = {"Easy", "Medium", "Hard"}
ALLOWED_CORRECT_ANSWERS = {"A", "B", "C", "D"}


class QuestionValidationError(ValueError):
    """Raised when question data does not satisfy V1 validation rules."""


@dataclass(slots=True)
class Question:
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str
    difficulty: str = DEFAULT_DIFFICULTY
    id: int | None = None

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "Question":
        return cls(
            id=row["id"],
            question=row["question"],
            option_a=row["option_a"],
            option_b=row["option_b"],
            option_c=row["option_c"],
            option_d=row["option_d"],
            correct_answer=row["correct_answer"],
            difficulty=row["difficulty"],
        )

    def to_record(self) -> dict[str, str]:
        return {
            "question": self.question,
            "option_a": self.option_a,
            "option_b": self.option_b,
            "option_c": self.option_c,
            "option_d": self.option_d,
            "correct_answer": self.correct_answer,
            "difficulty": self.difficulty,
        }


def validate_question_payload(payload: dict, *, partial: bool = False) -> dict[str, str]:
    """Validate and normalize a question payload for create or update flows."""
    required_fields = (
        "question",
        "option_a",
        "option_b",
        "option_c",
        "option_d",
        "correct_answer",
    )
    normalized: dict[str, str] = {}

    for field in required_fields:
        if field not in payload:
            if partial:
                continue
            raise QuestionValidationError(f"'{field}' is required")

        value = payload[field]
        if not isinstance(value, str) or not value.strip():
            raise QuestionValidationError(f"'{field}' must be a non-empty string")
        normalized[field] = value.strip()

    if "correct_answer" in normalized:
        normalized["correct_answer"] = normalized["correct_answer"].upper()
        if normalized["correct_answer"] not in ALLOWED_CORRECT_ANSWERS:
            raise QuestionValidationError(
                "'correct_answer' must be one of A, B, C, or D"
            )

    if "difficulty" not in payload:
        if not partial:
            normalized["difficulty"] = DEFAULT_DIFFICULTY
    else:
        difficulty = payload["difficulty"]
        if not isinstance(difficulty, str) or not difficulty.strip():
            raise QuestionValidationError("'difficulty' must be a non-empty string")
        difficulty = difficulty.strip().title()
        if difficulty not in ALLOWED_DIFFICULTIES:
            raise QuestionValidationError(
                "'difficulty' must be one of Easy, Medium, or Hard"
            )
        normalized["difficulty"] = difficulty

    return normalized


class QuestionRepository:
    """SQLite-backed persistence layer for V1 Question Bank questions."""

    def __init__(self, database_path: Path = DATABASE_PATH):
        self.database_path = Path(database_path)

    def list_questions(self) -> list[Question]:
        query = """
        SELECT id, question, option_a, option_b, option_c, option_d, correct AS correct_answer, difficulty
        FROM questions
        ORDER BY id DESC
        """
        with self._connect() as connection:
            rows = connection.execute(query).fetchall()
        return [Question.from_row(row) for row in rows]

    def search_questions(self, search_term: str) -> list[Question]:
        normalized_term = search_term.strip()
        if not normalized_term:
            return self.list_questions()

        query = """
        SELECT id, question, option_a, option_b, option_c, option_d, correct AS correct_answer, difficulty
        FROM questions
        WHERE LOWER(question) LIKE LOWER(?)
        ORDER BY id DESC
        """
        with self._connect() as connection:
            rows = connection.execute(query, (f"%{normalized_term}%",)).fetchall()
        return [Question.from_row(row) for row in rows]

    def get_question(self, question_id: int) -> Question | None:
        query = """
        SELECT id, question, option_a, option_b, option_c, option_d, correct AS correct_answer, difficulty
        FROM questions
        WHERE id = ?
        """
        with self._connect() as connection:
            row = connection.execute(query, (question_id,)).fetchone()
        return Question.from_row(row) if row else None

    def create_question(self, payload: dict) -> Question:
        record = validate_question_payload(payload)
        query = """
        INSERT INTO questions (
            question, option_a, option_b, option_c, option_d, correct, difficulty
        ) VALUES (
            :question, :option_a, :option_b, :option_c, :option_d, :correct_answer, :difficulty
        )
        """
        with self._connect() as connection:
            cursor = connection.execute(query, record)
            connection.commit()
            question_id = cursor.lastrowid
        created = self.get_question(question_id)
        assert created is not None
        return created

    def update_question(self, question_id: int, payload: dict) -> Question:
        if self.get_question(question_id) is None:
            raise KeyError(f"Question {question_id} does not exist")

        record = validate_question_payload(payload)
        record["id"] = question_id
        query = """
        UPDATE questions
        SET
            question = :question,
            option_a = :option_a,
            option_b = :option_b,
            option_c = :option_c,
            option_d = :option_d,
            correct = :correct_answer,
            difficulty = :difficulty,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = :id
        """
        with self._connect() as connection:
            connection.execute(query, record)
            connection.commit()
        updated = self.get_question(question_id)
        assert updated is not None
        return updated

    def delete_question(self, question_id: int) -> bool:
        with self._connect() as connection:
            cursor = connection.execute("DELETE FROM questions WHERE id = ?", (question_id,))
            connection.commit()
        return cursor.rowcount > 0

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection
