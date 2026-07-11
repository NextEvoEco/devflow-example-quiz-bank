from backend.db import get_connection
from backend.models import ExamAnswer, ExamAttempt
from backend.quiz_repository import QuizNotFoundError, QuizRepository


class ExamAttemptNotFoundError(Exception):
    def __init__(self, attempt_id: int):
        super().__init__(f"Exam attempt {attempt_id} was not found.")
        self.attempt_id = attempt_id


class ExamAttemptAlreadySubmittedError(Exception):
    def __init__(self, attempt_id: int):
        super().__init__(f"Exam attempt {attempt_id} was already submitted.")
        self.attempt_id = attempt_id


def _attempt_from_row(row) -> ExamAttempt:
    return ExamAttempt(
        id=row["id"],
        quiz_id=row["quiz_id"],
        score=row["score"],
        total=row["total"],
        started_at=row["started_at"],
        submitted_at=row["submitted_at"],
    )


def _answer_from_row(row) -> ExamAnswer:
    return ExamAnswer(
        id=row["id"],
        attempt_id=row["attempt_id"],
        question_id=row["question_id"],
        selected_option=row["selected_option"],
    )


class ExamAttemptRepository:
    def __init__(self):
        self.quiz_repository = QuizRepository()

    def create_attempt(self, quiz_id: int) -> ExamAttempt:
        if self.quiz_repository.get_by_id(quiz_id) is None:
            raise QuizNotFoundError(quiz_id)

        with get_connection() as connection:
            cursor = connection.execute(
                "INSERT INTO exam_attempts (quiz_id) VALUES (?)",
                (quiz_id,),
            )
            connection.commit()
            attempt_id = cursor.lastrowid

        attempt = self.get_attempt_with_answers(attempt_id)
        if attempt is None:
            raise RuntimeError("Failed to load exam attempt after creation.")
        return attempt["attempt"]

    def save_answer(
        self, attempt_id: int, question_id: int, selected_option: str | None
    ) -> None:
        attempt = self._get_attempt_row(attempt_id)
        if attempt is None:
            raise ExamAttemptNotFoundError(attempt_id)
        if attempt["submitted_at"] is not None:
            raise ExamAttemptAlreadySubmittedError(attempt_id)

        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO exam_answers (attempt_id, question_id, selected_option)
                VALUES (?, ?, ?)
                ON CONFLICT(attempt_id, question_id) DO UPDATE SET
                    selected_option = excluded.selected_option
                """,
                (attempt_id, question_id, selected_option),
            )
            connection.commit()

    def submit_attempt(self, attempt_id: int, score: int, total: int) -> ExamAttempt:
        attempt = self._get_attempt_row(attempt_id)
        if attempt is None:
            raise ExamAttemptNotFoundError(attempt_id)
        if attempt["submitted_at"] is not None:
            raise ExamAttemptAlreadySubmittedError(attempt_id)

        with get_connection() as connection:
            connection.execute(
                """
                UPDATE exam_attempts
                SET score = ?, total = ?, submitted_at = datetime('now')
                WHERE id = ?
                """,
                (score, total, attempt_id),
            )
            connection.commit()

        result = self.get_attempt_with_answers(attempt_id)
        if result is None:
            raise ExamAttemptNotFoundError(attempt_id)
        return result["attempt"]

    def get_attempt_with_answers(
        self, attempt_id: int
    ) -> dict[str, ExamAttempt | list[ExamAnswer]] | None:
        attempt = self._get_attempt_row(attempt_id)
        if attempt is None:
            return None

        with get_connection() as connection:
            answer_rows = connection.execute(
                """
                SELECT * FROM exam_answers
                WHERE attempt_id = ?
                ORDER BY question_id ASC
                """,
                (attempt_id,),
            ).fetchall()

        return {
            "attempt": _attempt_from_row(attempt),
            "answers": [_answer_from_row(row) for row in answer_rows],
        }

    def _get_attempt_row(self, attempt_id: int):
        with get_connection() as connection:
            return connection.execute(
                "SELECT * FROM exam_attempts WHERE id = ?",
                (attempt_id,),
            ).fetchone()
