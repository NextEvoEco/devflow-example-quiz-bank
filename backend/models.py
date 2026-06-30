from dataclasses import dataclass
from typing import Any


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
        return {
            "id": self.id,
            "question": self.question,
            "a": self.a,
            "b": self.b,
            "c": self.c,
            "d": self.d,
            "correct": self.correct,
            "difficulty": self.difficulty,
        }

    @classmethod
    def from_row(cls, row: Any) -> "Question":
        return cls(
            id=row["id"],
            question=row["question"],
            a=row["option_a"],
            b=row["option_b"],
            c=row["option_c"],
            d=row["option_d"],
            correct=row["correct"],
            difficulty=row["difficulty"],
        )


@dataclass
class QuizSummary:
    id: int
    name: str
    created_at: str
    question_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "createdAt": self.created_at,
            "questionCount": self.question_count,
        }


@dataclass
class QuizDetail:
    id: int
    name: str
    created_at: str
    question_ids: list[int]
    questions: list[Question]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "createdAt": self.created_at,
            "questionIds": self.question_ids,
            "questions": [question.to_dict() for question in self.questions],
        }


@dataclass
class ExamAttempt:
    id: int
    quiz_id: int
    score: int | None
    total: int | None
    started_at: str
    submitted_at: str | None

    @classmethod
    def from_row(cls, row: Any) -> "ExamAttempt":
        return cls(
            id=row["id"],
            quiz_id=row["quiz_id"],
            score=row["score"],
            total=row["total"],
            started_at=row["started_at"],
            submitted_at=row["submitted_at"],
        )


@dataclass
class ExamAnswer:
    id: int
    attempt_id: int
    question_id: int
    selected_option: str | None

    @classmethod
    def from_row(cls, row: Any) -> "ExamAnswer":
        return cls(
            id=row["id"],
            attempt_id=row["attempt_id"],
            question_id=row["question_id"],
            selected_option=row["selected_option"],
        )


@dataclass
class ExamAttemptWithAnswers:
    attempt: ExamAttempt
    answers: list[ExamAnswer]
