from dataclasses import dataclass


@dataclass
class ExamAttempt:
    id: int
    quiz_id: int
    score: int | None
    total: int | None
    started_at: str
    submitted_at: str | None


@dataclass
class ExamAnswer:
    id: int
    attempt_id: int
    question_id: int
    selected_option: str | None
