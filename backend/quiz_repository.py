"""Quiz persistence layer."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from backend.database import get_connection
from backend.models import NotFoundError, Question, ValidationError
from backend.question_repository import QuestionRepository


class QuizRepository:
    def __init__(self, db_path: Path | str | None = None):
        self.db_path = db_path
        self.questions = QuestionRepository(db_path)

    def _conn(self):
        return get_connection(self.db_path)

    def _validate_question_ids(self, question_ids: list[Any]) -> list[int]:
        if not isinstance(question_ids, list):
            raise ValidationError("question_ids must be a list", field="question_ids")
        ids: list[int] = []
        for item in question_ids:
            try:
                ids.append(int(item))
            except (TypeError, ValueError) as exc:
                raise ValidationError(
                    "question_ids must contain integers",
                    field="question_ids",
                ) from exc
        if len(ids) < 3:
            raise ValidationError(
                "A quiz requires at least 3 questions",
                field="question_ids",
            )
        if len(set(ids)) != len(ids):
            raise ValidationError(
                "A quiz cannot contain duplicate questions",
                field="question_ids",
            )
        conn = self._conn()
        try:
            for qid in ids:
                row = conn.execute(
                    "SELECT 1 FROM questions WHERE id = ?", (qid,)
                ).fetchone()
                if row is None:
                    raise ValidationError(
                        f"Question {qid} does not exist",
                        field="question_ids",
                    )
        finally:
            conn.close()
        return ids

    def list_quizzes(self) -> list[dict[str, Any]]:
        conn = self._conn()
        try:
            rows = conn.execute(
                """
                SELECT q.id, q.name, q.created_at,
                       COUNT(qq.question_id) AS question_count
                FROM quizzes q
                LEFT JOIN quiz_questions qq ON qq.quiz_id = q.id
                GROUP BY q.id
                ORDER BY q.id DESC
                """
            ).fetchall()
            return [
                {
                    "id": row["id"],
                    "name": row["name"],
                    "created_at": row["created_at"],
                    "question_count": row["question_count"],
                }
                for row in rows
            ]
        finally:
            conn.close()

    def get_quiz(self, quiz_id: int) -> dict[str, Any]:
        conn = self._conn()
        try:
            quiz = conn.execute(
                "SELECT * FROM quizzes WHERE id = ?", (quiz_id,)
            ).fetchone()
            if quiz is None:
                raise NotFoundError(f"Quiz {quiz_id} not found")
            rows = conn.execute(
                """
                SELECT qs.id, qs.question,
                       qs.option_a AS a, qs.option_b AS b,
                       qs.option_c AS c, qs.option_d AS d,
                       qs.correct, qs.difficulty
                FROM quiz_questions qq
                JOIN questions qs ON qs.id = qq.question_id
                WHERE qq.quiz_id = ?
                ORDER BY qq.position ASC
                """,
                (quiz_id,),
            ).fetchall()
            questions = [
                Question(
                    id=row["id"],
                    question=row["question"],
                    a=row["a"],
                    b=row["b"],
                    c=row["c"],
                    d=row["d"],
                    correct=row["correct"],
                    difficulty=row["difficulty"],
                ).to_dict()
                for row in rows
            ]
            return {
                "id": quiz["id"],
                "name": quiz["name"],
                "created_at": quiz["created_at"],
                "question_ids": [q["id"] for q in questions],
                "questions": questions,
                "question_count": len(questions),
            }
        finally:
            conn.close()

    def create_quiz(self, data: dict[str, Any] | None) -> dict[str, Any]:
        if not isinstance(data, dict):
            raise ValidationError("Request body must be a JSON object")
        name = str(data.get("name") or "").strip()
        if not name:
            raise ValidationError("Quiz name is required", field="name")
        question_ids = self._validate_question_ids(data.get("question_ids") or [])
        quiz_id = int(data.get("id") or time.time_ns() // 1_000_000)
        conn = self._conn()
        try:
            while conn.execute(
                "SELECT 1 FROM quizzes WHERE id = ?", (quiz_id,)
            ).fetchone():
                quiz_id += 1
            conn.execute(
                "INSERT INTO quizzes (id, name) VALUES (?, ?)",
                (quiz_id, name),
            )
            for position, qid in enumerate(question_ids):
                conn.execute(
                    """
                    INSERT INTO quiz_questions (quiz_id, question_id, position)
                    VALUES (?, ?, ?)
                    """,
                    (quiz_id, qid, position),
                )
            conn.commit()
        finally:
            conn.close()
        return self.get_quiz(quiz_id)

    def update_quiz(self, quiz_id: int, data: dict[str, Any] | None) -> dict[str, Any]:
        if not isinstance(data, dict):
            raise ValidationError("Request body must be a JSON object")
        existing = self.get_quiz(quiz_id)
        name = data.get("name", existing["name"])
        name = str(name or "").strip()
        if not name:
            raise ValidationError("Quiz name is required", field="name")
        if "question_ids" in data:
            question_ids = self._validate_question_ids(data.get("question_ids") or [])
        else:
            question_ids = existing["question_ids"]
            if len(question_ids) < 3:
                raise ValidationError(
                    "A quiz requires at least 3 questions",
                    field="question_ids",
                )
        conn = self._conn()
        try:
            conn.execute(
                "UPDATE quizzes SET name = ? WHERE id = ?",
                (name, quiz_id),
            )
            conn.execute(
                "DELETE FROM quiz_questions WHERE quiz_id = ?",
                (quiz_id,),
            )
            for position, qid in enumerate(question_ids):
                conn.execute(
                    """
                    INSERT INTO quiz_questions (quiz_id, question_id, position)
                    VALUES (?, ?, ?)
                    """,
                    (quiz_id, qid, position),
                )
            conn.commit()
        finally:
            conn.close()
        return self.get_quiz(quiz_id)

    def delete_quiz(self, quiz_id: int) -> None:
        conn = self._conn()
        try:
            cursor = conn.execute(
                "DELETE FROM quizzes WHERE id = ?", (quiz_id,)
            )
            conn.commit()
            if cursor.rowcount == 0:
                raise NotFoundError(f"Quiz {quiz_id} not found")
        finally:
            conn.close()
