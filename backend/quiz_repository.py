from backend.db import get_connection
from backend.question_repository import QuestionRepository, _row_to_dict
from backend.quiz_validation import (
    QuizValidationError,
    validate_quiz_create_payload,
    validate_quiz_update_payload,
)


class QuizNotFoundError(Exception):
    def __init__(self, quiz_id: int):
        super().__init__(f"Quiz {quiz_id} was not found.")
        self.quiz_id = quiz_id


class QuizRepository:
    def __init__(self):
        self.question_repository = QuestionRepository()

    def _validate_question_ids_exist(self, question_ids: list[int]) -> None:
        missing_ids = [
            question_id
            for question_id in question_ids
            if self.question_repository.get_by_id(question_id) is None
        ]
        if missing_ids:
            raise QuizValidationError(
                "Invalid quiz payload.",
                {
                    "questionIds": (
                        f"Question IDs do not exist: {', '.join(str(item) for item in missing_ids)}"
                    )
                },
            )

    def _replace_quiz_questions(
        self, connection, quiz_id: int, question_ids: list[int]
    ) -> None:
        connection.execute(
            "DELETE FROM quiz_questions WHERE quiz_id = ?",
            (quiz_id,),
        )
        for position, question_id in enumerate(question_ids):
            connection.execute(
                """
                INSERT INTO quiz_questions (quiz_id, question_id, position)
                VALUES (?, ?, ?)
                """,
                (quiz_id, question_id, position),
            )

    def _get_question_count(self, connection, quiz_id: int) -> int:
        row = connection.execute(
            "SELECT COUNT(*) AS count FROM quiz_questions WHERE quiz_id = ?",
            (quiz_id,),
        ).fetchone()
        return row["count"]

    def _get_ordered_questions(self, connection, quiz_id: int) -> list[dict]:
        rows = connection.execute(
            """
            SELECT questions.*
            FROM quiz_questions
            JOIN questions ON questions.id = quiz_questions.question_id
            WHERE quiz_questions.quiz_id = ?
            ORDER BY quiz_questions.position ASC
            """,
            (quiz_id,),
        ).fetchall()
        return [_row_to_dict(row) for row in rows]

    def _quiz_summary(self, connection, row) -> dict:
        return {
            "id": row["id"],
            "name": row["name"],
            "questionCount": self._get_question_count(connection, row["id"]),
        }

    def create(self, payload: dict) -> dict:
        validated = validate_quiz_create_payload(payload)
        self._validate_question_ids_exist(validated["questionIds"])

        with get_connection() as connection:
            cursor = connection.execute(
                "INSERT INTO quizzes (name) VALUES (?)",
                (validated["name"],),
            )
            quiz_id = cursor.lastrowid
            self._replace_quiz_questions(
                connection, quiz_id, validated["questionIds"]
            )
            connection.commit()

        created = self.get_by_id(quiz_id)
        if created is None:
            raise RuntimeError("Failed to load quiz after creation.")
        return created

    def list_all(self) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute(
                "SELECT * FROM quizzes ORDER BY id ASC"
            ).fetchall()
            return [self._quiz_summary(connection, row) for row in rows]

    def get_by_id(self, quiz_id: int) -> dict | None:
        with get_connection() as connection:
            row = connection.execute(
                "SELECT * FROM quizzes WHERE id = ?",
                (quiz_id,),
            ).fetchone()
            if row is None:
                return None

            return {
                "id": row["id"],
                "name": row["name"],
                "questionCount": self._get_question_count(connection, quiz_id),
                "questions": self._get_ordered_questions(connection, quiz_id),
            }

    def update(self, quiz_id: int, payload: dict) -> dict:
        existing = self.get_by_id(quiz_id)
        if existing is None:
            raise QuizNotFoundError(quiz_id)

        validated = validate_quiz_update_payload(payload)
        if "questionIds" in validated:
            self._validate_question_ids_exist(validated["questionIds"])

        with get_connection() as connection:
            if "name" in validated:
                updated = connection.execute(
                    "UPDATE quizzes SET name = ? WHERE id = ?",
                    (validated["name"], quiz_id),
                )
                if updated.rowcount == 0:
                    raise QuizNotFoundError(quiz_id)

            if "questionIds" in validated:
                self._replace_quiz_questions(
                    connection, quiz_id, validated["questionIds"]
                )

            connection.commit()

        updated_quiz = self.get_by_id(quiz_id)
        if updated_quiz is None:
            raise QuizNotFoundError(quiz_id)
        return updated_quiz

    def delete(self, quiz_id: int) -> None:
        with get_connection() as connection:
            deleted = connection.execute(
                "DELETE FROM quizzes WHERE id = ?",
                (quiz_id,),
            )
            connection.commit()
            if deleted.rowcount == 0:
                raise QuizNotFoundError(quiz_id)
