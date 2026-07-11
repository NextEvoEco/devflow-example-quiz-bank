from dataclasses import asdict, dataclass


@dataclass
class Question:
    """Question entity matching the UI contract in .devflow/context/ui-spec.md."""

    id: int
    question: str
    a: str
    b: str
    c: str
    d: str
    correct: str
    difficulty: str

    def to_dict(self) -> dict:
        return asdict(self)


def question_from_row(row) -> Question:
    """Map a SQLite row (option_a..option_d columns) to a Question entity."""
    return Question(
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
class ExamAttempt:
    """An exam attempt on a quiz (o03). Pending until submitted.

    score/total/submitted_at are None while the attempt is in progress.
    """

    id: int
    quiz_id: int
    score: int
    total: int
    started_at: str
    submitted_at: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ExamAnswer:
    """A single selected answer within an attempt. selected_option may be None
    for an unanswered question."""

    id: int
    attempt_id: int
    question_id: int
    selected_option: str

    def to_dict(self) -> dict:
        return asdict(self)


def exam_attempt_from_row(row) -> ExamAttempt:
    return ExamAttempt(
        id=row["id"],
        quiz_id=row["quiz_id"],
        score=row["score"],
        total=row["total"],
        started_at=row["started_at"],
        submitted_at=row["submitted_at"],
    )


def exam_answer_from_row(row) -> ExamAnswer:
    return ExamAnswer(
        id=row["id"],
        attempt_id=row["attempt_id"],
        question_id=row["question_id"],
        selected_option=row["selected_option"],
    )
