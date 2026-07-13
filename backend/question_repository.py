"""Question persistence layer."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from backend.database import get_connection
from backend.models import NotFoundError, Question, normalize_question_payload


class QuestionRepository:
    def __init__(self, db_path: Path | str | None = None):
        self.db_path = db_path

    def _conn(self):
        return get_connection(self.db_path)

    @staticmethod
    def _row_to_question(row) -> Question:
        return Question(
            id=row["id"],
            question=row["question"],
            a=row["a"],
            b=row["b"],
            c=row["c"],
            d=row["d"],
            correct=row["correct"],
            difficulty=row["difficulty"],
        )

    def list_questions(self, search: str | None = None) -> list[Question]:
        conn = self._conn()
        try:
            if search and search.strip():
                pattern = f"%{search.strip()}%"
                rows = conn.execute(
                    "SELECT id, question, option_a AS a, option_b AS b, "
                    "option_c AS c, option_d AS d, correct, difficulty "
                    "FROM questions WHERE question LIKE ? "
                    "COLLATE NOCASE ORDER BY id DESC",
                    (pattern,),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT id, question, option_a AS a, option_b AS b, "
                    "option_c AS c, option_d AS d, correct, difficulty "
                    "FROM questions ORDER BY id DESC"
                ).fetchall()
            return [self._row_to_question(row) for row in rows]
        finally:
            conn.close()

    def get_question(self, question_id: int) -> Question:
        conn = self._conn()
        try:
            row = conn.execute(
                "SELECT id, question, option_a AS a, option_b AS b, "
                "option_c AS c, option_d AS d, correct, difficulty "
                "FROM questions WHERE id = ?",
                (question_id,),
            ).fetchone()
            if row is None:
                raise NotFoundError(f"Question {question_id} not found")
            return self._row_to_question(row)
        finally:
            conn.close()

    def create_question(self, data: dict[str, Any]) -> Question:
        payload = normalize_question_payload(data)
        question_id = int(data.get("id") or time.time_ns() // 1_000_000)
        conn = self._conn()
        try:
            # Ensure uniqueness if millisecond collision
            while conn.execute(
                "SELECT 1 FROM questions WHERE id = ?", (question_id,)
            ).fetchone():
                question_id += 1
            conn.execute(
                """
                INSERT INTO questions
                    (id, question, option_a, option_b, option_c, option_d,
                     correct, difficulty)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    question_id,
                    payload["question"],
                    payload["a"],
                    payload["b"],
                    payload["c"],
                    payload["d"],
                    payload["correct"],
                    payload["difficulty"],
                ),
            )
            conn.commit()
        finally:
            conn.close()
        return self.get_question(question_id)

    def update_question(self, question_id: int, data: dict[str, Any]) -> Question:
        payload = normalize_question_payload(data)
        conn = self._conn()
        try:
            existing = conn.execute(
                "SELECT id FROM questions WHERE id = ?",
                (question_id,),
            ).fetchone()
            if existing is None:
                raise NotFoundError(f"Question {question_id} not found")
            conn.execute(
                """
                UPDATE questions
                SET question = ?, option_a = ?, option_b = ?, option_c = ?,
                    option_d = ?, correct = ?, difficulty = ?,
                    updated_at = datetime('now')
                WHERE id = ?
                """,
                (
                    payload["question"],
                    payload["a"],
                    payload["b"],
                    payload["c"],
                    payload["d"],
                    payload["correct"],
                    payload["difficulty"],
                    question_id,
                ),
            )
            conn.commit()
        finally:
            conn.close()
        return self.get_question(question_id)

    def delete_question(self, question_id: int) -> None:
        conn = self._conn()
        try:
            cursor = conn.execute(
                "DELETE FROM questions WHERE id = ?",
                (question_id,),
            )
            conn.commit()
            if cursor.rowcount == 0:
                raise NotFoundError(f"Question {question_id} not found")
        finally:
            conn.close()
