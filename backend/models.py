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
