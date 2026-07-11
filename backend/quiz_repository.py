from .database import get_connection
from .models import question_from_row
from .quiz_validation import validate_quiz
from .validation import ValidationError

_Q_COLUMNS = "q.id, q.question, q.option_a, q.option_b, q.option_c, q.option_d, q.correct, q.difficulty"


class QuizRepository:
    """SQLite persistence for quizzes and their ordered question references.

    Question content is never duplicated: quizzes reference questions by id
    through the `quiz_questions` join table, ordered by `position`.
    """

    def __init__(self, db_path=None):
        self.db_path = db_path

    def _connect(self):
        return get_connection(self.db_path)

    def list(self) -> list:
        conn = self._connect()
        try:
            rows = conn.execute(
                """
                SELECT quizzes.id, quizzes.name, quizzes.created_at,
                       COUNT(quiz_questions.question_id) AS question_count
                  FROM quizzes
                  LEFT JOIN quiz_questions ON quiz_questions.quiz_id = quizzes.id
                 GROUP BY quizzes.id
                 ORDER BY quizzes.id
                """
            ).fetchall()
        finally:
            conn.close()
        return [
            {
                "id": r["id"],
                "name": r["name"],
                "created_at": r["created_at"],
                "question_count": r["question_count"],
            }
            for r in rows
        ]

    def get(self, quiz_id: int):
        conn = self._connect()
        try:
            quiz = conn.execute(
                "SELECT id, name, created_at FROM quizzes WHERE id = ?",
                (quiz_id,),
            ).fetchone()
            if quiz is None:
                return None
            question_rows = conn.execute(
                f"""
                SELECT {_Q_COLUMNS}
                  FROM quiz_questions
                  JOIN questions AS q ON q.id = quiz_questions.question_id
                 WHERE quiz_questions.quiz_id = ?
                 ORDER BY quiz_questions.position
                """,
                (quiz_id,),
            ).fetchall()
        finally:
            conn.close()

        questions = [question_from_row(r).to_dict() for r in question_rows]
        return {
            "id": quiz["id"],
            "name": quiz["name"],
            "created_at": quiz["created_at"],
            "questionIds": [q["id"] for q in questions],
            "questions": questions,
        }

    def create(self, payload: dict) -> dict:
        data = validate_quiz(payload)
        conn = self._connect()
        try:
            self._ensure_questions_exist(conn, data["question_ids"])
            cursor = conn.execute("INSERT INTO quizzes (name) VALUES (?)", (data["name"],))
            quiz_id = cursor.lastrowid
            self._insert_question_rows(conn, quiz_id, data["question_ids"])
            conn.commit()
        finally:
            conn.close()
        return self.get(quiz_id)

    def update(self, quiz_id: int, payload: dict):
        data = validate_quiz(payload)
        conn = self._connect()
        try:
            exists = conn.execute(
                "SELECT 1 FROM quizzes WHERE id = ?", (quiz_id,)
            ).fetchone()
            if exists is None:
                return None
            self._ensure_questions_exist(conn, data["question_ids"])
            conn.execute("UPDATE quizzes SET name = ? WHERE id = ?", (data["name"], quiz_id))
            conn.execute("DELETE FROM quiz_questions WHERE quiz_id = ?", (quiz_id,))
            self._insert_question_rows(conn, quiz_id, data["question_ids"])
            conn.commit()
        finally:
            conn.close()
        return self.get(quiz_id)

    def delete(self, quiz_id: int) -> bool:
        conn = self._connect()
        try:
            cursor = conn.execute("DELETE FROM quizzes WHERE id = ?", (quiz_id,))
            conn.commit()
            deleted = cursor.rowcount
        finally:
            conn.close()
        # quiz_questions rows are removed by the ON DELETE CASCADE foreign key.
        return deleted > 0

    # --- helpers -------------------------------------------------------------

    def _ensure_questions_exist(self, conn, question_ids) -> None:
        placeholders = ",".join("?" * len(question_ids))
        rows = conn.execute(
            f"SELECT id FROM questions WHERE id IN ({placeholders})",
            question_ids,
        ).fetchall()
        existing = {r["id"] for r in rows}
        missing = [qid for qid in question_ids if qid not in existing]
        if missing:
            raise ValidationError(
                {"questionIds": f"question IDs do not exist: {missing}"}
            )

    def _insert_question_rows(self, conn, quiz_id, question_ids) -> None:
        conn.executemany(
            "INSERT INTO quiz_questions (quiz_id, question_id, position) VALUES (?, ?, ?)",
            [(quiz_id, qid, position) for position, qid in enumerate(question_ids)],
        )
