"""Exam attempt persistence layer."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from backend.database import get_connection
from backend.models import ExamAnswer, ExamAttempt, NotFoundError, ValidationError


class ExamAttemptRepository:
    def __init__(self, db_path: Path | str | None = None):
        self.db_path = db_path

    def _conn(self):
        return get_connection(self.db_path)

    def create_attempt(self, quiz_id: int) -> ExamAttempt:
        conn = self._conn()
        try:
            quiz = conn.execute(
                "SELECT id FROM quizzes WHERE id = ?", (quiz_id,)
            ).fetchone()
            if quiz is None:
                raise NotFoundError(f"Quiz {quiz_id} not found")
            attempt_id = time.time_ns() // 1_000_000
            while conn.execute(
                "SELECT 1 FROM exam_attempts WHERE id = ?", (attempt_id,)
            ).fetchone():
                attempt_id += 1
            conn.execute(
                """
                INSERT INTO exam_attempts (id, quiz_id, score, total, submitted_at)
                VALUES (?, ?, NULL, NULL, NULL)
                """,
                (attempt_id, quiz_id),
            )
            conn.commit()
            row = conn.execute(
                "SELECT * FROM exam_attempts WHERE id = ?", (attempt_id,)
            ).fetchone()
            return ExamAttempt(
                id=row["id"],
                quiz_id=row["quiz_id"],
                score=row["score"],
                total=row["total"],
                started_at=row["started_at"],
                submitted_at=row["submitted_at"],
            )
        finally:
            conn.close()

    def save_answer(
        self,
        attempt_id: int,
        question_id: int,
        selected_option: str | None,
    ) -> None:
        conn = self._conn()
        try:
            attempt = conn.execute(
                "SELECT * FROM exam_attempts WHERE id = ?", (attempt_id,)
            ).fetchone()
            if attempt is None:
                raise NotFoundError(f"Attempt {attempt_id} not found")
            if attempt["submitted_at"] is not None:
                raise ValidationError("Attempt already submitted")
            if selected_option is not None:
                selected_option = str(selected_option).strip().upper()
                if selected_option not in {"A", "B", "C", "D"}:
                    raise ValidationError(
                        "selected_option must be A, B, C, or D",
                        field="selected_option",
                    )
            existing = conn.execute(
                """
                SELECT id FROM exam_answers
                WHERE attempt_id = ? AND question_id = ?
                """,
                (attempt_id, question_id),
            ).fetchone()
            if existing:
                conn.execute(
                    """
                    UPDATE exam_answers
                    SET selected_option = ?
                    WHERE id = ?
                    """,
                    (selected_option, existing["id"]),
                )
            else:
                answer_id = time.time_ns() // 1_000_000
                while conn.execute(
                    "SELECT 1 FROM exam_answers WHERE id = ?", (answer_id,)
                ).fetchone():
                    answer_id += 1
                conn.execute(
                    """
                    INSERT INTO exam_answers
                    (id, attempt_id, question_id, selected_option)
                    VALUES (?, ?, ?, ?)
                    """,
                    (answer_id, attempt_id, question_id, selected_option),
                )
            conn.commit()
        finally:
            conn.close()

    def get_attempt_with_answers(
        self, attempt_id: int
    ) -> tuple[ExamAttempt, list[ExamAnswer]]:
        conn = self._conn()
        try:
            row = conn.execute(
                "SELECT * FROM exam_attempts WHERE id = ?", (attempt_id,)
            ).fetchone()
            if row is None:
                raise NotFoundError(f"Attempt {attempt_id} not found")
            attempt = ExamAttempt(
                id=row["id"],
                quiz_id=row["quiz_id"],
                score=row["score"],
                total=row["total"],
                started_at=row["started_at"],
                submitted_at=row["submitted_at"],
            )
            answers = [
                ExamAnswer(
                    id=r["id"],
                    attempt_id=r["attempt_id"],
                    question_id=r["question_id"],
                    selected_option=r["selected_option"],
                )
                for r in conn.execute(
                    "SELECT * FROM exam_answers WHERE attempt_id = ?",
                    (attempt_id,),
                ).fetchall()
            ]
            return attempt, answers
        finally:
            conn.close()

    def submit_attempt(
        self, attempt_id: int, score: int, total: int
    ) -> ExamAttempt:
        conn = self._conn()
        try:
            row = conn.execute(
                "SELECT * FROM exam_attempts WHERE id = ?", (attempt_id,)
            ).fetchone()
            if row is None:
                raise NotFoundError(f"Attempt {attempt_id} not found")
            if row["submitted_at"] is not None:
                raise ValidationError("Attempt already submitted")
            conn.execute(
                """
                UPDATE exam_attempts
                SET score = ?, total = ?, submitted_at = datetime('now')
                WHERE id = ?
                """,
                (score, total, attempt_id),
            )
            conn.commit()
        finally:
            conn.close()
        attempt, _ = self.get_attempt_with_answers(attempt_id)
        return attempt

    def score_attempt(self, attempt_id: int) -> dict[str, Any]:
        attempt, answers = self.get_attempt_with_answers(attempt_id)
        if attempt.submitted_at is not None:
            raise ValidationError("Attempt already submitted")

        conn = self._conn()
        try:
            questions = conn.execute(
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
                (attempt.quiz_id,),
            ).fetchall()
            quiz = conn.execute(
                "SELECT name FROM quizzes WHERE id = ?",
                (attempt.quiz_id,),
            ).fetchone()
        finally:
            conn.close()

        answer_map = {a.question_id: a.selected_option for a in answers}
        review = []
        score = 0
        for q in questions:
            selected = answer_map.get(q["id"])
            correct = q["correct"]
            is_correct = selected == correct
            if is_correct:
                score += 1
            option_map = {"A": q["a"], "B": q["b"], "C": q["c"], "D": q["d"]}
            review.append(
                {
                    "question_id": q["id"],
                    "question_text": q["question"],
                    "selected_option": selected,
                    "selected_text": option_map.get(selected) if selected else None,
                    "correct_option": correct,
                    "correct_text": option_map[correct],
                    "options": option_map,
                    "is_correct": is_correct,
                }
            )
        total = len(questions)
        percentage = round((score / total) * 100) if total else 0
        submitted = self.submit_attempt(attempt_id, score, total)
        return {
            "attempt_id": submitted.id,
            "quiz_id": submitted.quiz_id,
            "quiz_name": quiz["name"] if quiz else "",
            "score": score,
            "total": total,
            "percentage": percentage,
            "answers": review,
        }
