"""Domain models and validation errors."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


class ValidationError(Exception):
    """Raised when question (or later quiz) payload validation fails."""

    def __init__(self, message: str, field: str | None = None):
        super().__init__(message)
        self.message = message
        self.field = field


class NotFoundError(Exception):
    """Raised when a requested record does not exist."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


VALID_CORRECT = frozenset({"A", "B", "C", "D"})
VALID_DIFFICULTY = frozenset({"Easy", "Medium", "Hard"})
DEFAULT_DIFFICULTY = "Medium"


@dataclass
class Question:
    id: int
    question: str
    a: str
    b: str
    c: str
    d: str
    correct: str
    difficulty: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ExamAttempt:
    id: int
    quiz_id: int
    score: int | None
    total: int | None
    started_at: str
    submitted_at: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ExamAnswer:
    id: int
    attempt_id: int
    question_id: int
    selected_option: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def normalize_question_payload(data: dict[str, Any] | None) -> dict[str, Any]:
    """Validate and normalize a question create/update payload."""
    if not isinstance(data, dict):
        raise ValidationError("Request body must be a JSON object")

    def require_text(key: str, label: str) -> str:
        if key not in data or data[key] is None:
            raise ValidationError(f"{label} is required", field=key)
        value = str(data[key]).strip()
        if not value:
            raise ValidationError(f"{label} is required", field=key)
        return value

    question = require_text("question", "Question text")
    a = require_text("a", "Option A")
    b = require_text("b", "Option B")
    c = require_text("c", "Option C")
    d = require_text("d", "Option D")

    if "correct" not in data or data["correct"] is None or str(data["correct"]).strip() == "":
        raise ValidationError("Correct answer is required", field="correct")
    correct = str(data["correct"]).strip().upper()
    if correct not in VALID_CORRECT:
        raise ValidationError(
            "Correct answer must be one of A, B, C, or D",
            field="correct",
        )

    if "difficulty" not in data or data["difficulty"] is None or str(data["difficulty"]).strip() == "":
        difficulty = DEFAULT_DIFFICULTY
    else:
        difficulty = str(data["difficulty"]).strip()
        # Accept common casing variants
        matched = next((v for v in VALID_DIFFICULTY if v.lower() == difficulty.lower()), None)
        if matched is None:
            raise ValidationError(
                "Difficulty must be Easy, Medium, or Hard",
                field="difficulty",
            )
        difficulty = matched

    return {
        "question": question,
        "a": a,
        "b": b,
        "c": c,
        "d": d,
        "correct": correct,
        "difficulty": difficulty,
    }
