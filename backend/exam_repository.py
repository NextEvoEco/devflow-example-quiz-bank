from .database import get_connection
from .models import exam_answer_from_row, exam_attempt_from_row

_ATTEMPT_COLUMNS = "id, quiz_id, score, total, started_at, submitted_at"
_ANSWER_COLUMNS = "id, attempt_id, question_id, selected_option"


class ExamAttemptRepository:
    """SQLite persistence for exam attempts and their per-question answers (o03).

    An attempt is created pending (score/total/submitted_at NULL). Answers are
    saved (insert-or-replace) as the user progresses, and submit finalizes the
    attempt with a score and total.
    """

    def __init__(self, db_path=None):
        self.db_path = db_path

    def _connect(self):
        return get_connection(self.db_path)

    def create_attempt(self, quiz_id: int) -> dict:
        conn = self._connect()
        try:
            cursor = conn.execute(
                "INSERT INTO exam_attempts (quiz_id) VALUES (?)", (quiz_id,)
            )
            attempt_id = cursor.lastrowid
            conn.commit()
        finally:
            conn.close()
        return self.get_attempt(attempt_id)

    def get_attempt(self, attempt_id: int):
        conn = self._connect()
        try:
            row = conn.execute(
                f"SELECT {_ATTEMPT_COLUMNS} FROM exam_attempts WHERE id = ?",
                (attempt_id,),
            ).fetchone()
        finally:
            conn.close()
        return exam_attempt_from_row(row).to_dict() if row else None

    def save_answer(self, attempt_id: int, question_id: int, selected_option):
        """Insert or replace the answer for a question within an attempt."""
        conn = self._connect()
        try:
            conn.execute(
                """
                INSERT OR REPLACE INTO exam_answers (attempt_id, question_id, selected_option)
                VALUES (?, ?, ?)
                """,
                (attempt_id, question_id, selected_option),
            )
            conn.commit()
        finally:
            conn.close()

    def submit_attempt(self, attempt_id: int, score: int, total: int):
        """Finalize an attempt: record score, total, and submission time."""
        conn = self._connect()
        try:
            cursor = conn.execute(
                """
                UPDATE exam_attempts
                   SET score = ?, total = ?, submitted_at = CURRENT_TIMESTAMP
                 WHERE id = ?
                """,
                (score, total, attempt_id),
            )
            conn.commit()
            changed = cursor.rowcount
        finally:
            conn.close()
        if changed == 0:
            return None
        return self.get_attempt(attempt_id)

    def get_attempt_with_answers(self, attempt_id: int):
        """Return the attempt plus all its answer rows, or None if not found."""
        conn = self._connect()
        try:
            attempt_row = conn.execute(
                f"SELECT {_ATTEMPT_COLUMNS} FROM exam_attempts WHERE id = ?",
                (attempt_id,),
            ).fetchone()
            if attempt_row is None:
                return None
            answer_rows = conn.execute(
                f"SELECT {_ANSWER_COLUMNS} FROM exam_answers WHERE attempt_id = ? ORDER BY id",
                (attempt_id,),
            ).fetchall()
        finally:
            conn.close()

        attempt = exam_attempt_from_row(attempt_row).to_dict()
        attempt["answers"] = [exam_answer_from_row(r).to_dict() for r in answer_rows]
        return attempt
