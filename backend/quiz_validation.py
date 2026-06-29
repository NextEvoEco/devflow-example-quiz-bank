from typing import Any

from backend.errors import ValidationError

MIN_QUIZ_QUESTIONS = 3


def _normalize_question_ids(value: Any) -> list[int]:
    if value is None:
        raise ValidationError("questionIds is required.", "questionIds")

    if not isinstance(value, list):
        raise ValidationError("questionIds must be an array.", "questionIds")

    if not value:
        raise ValidationError(
            f"A quiz must include at least {MIN_QUIZ_QUESTIONS} questions.",
            "questionIds",
        )

    question_ids: list[int] = []
    for index, item in enumerate(value):
        if isinstance(item, bool) or not isinstance(item, int):
            raise ValidationError(
                f"questionIds[{index}] must be an integer.",
                "questionIds",
            )
        question_ids.append(item)

    if len(question_ids) < MIN_QUIZ_QUESTIONS:
        raise ValidationError(
            f"A quiz must include at least {MIN_QUIZ_QUESTIONS} questions.",
            "questionIds",
        )

    if len(set(question_ids)) != len(question_ids):
        raise ValidationError(
            "questionIds must not contain duplicate values.",
            "questionIds",
        )

    return question_ids


def _normalize_name(value: Any) -> str:
    if value is None or not isinstance(value, str):
        raise ValidationError("Quiz name is required.", "name")

    name = value.strip()
    if not name:
        raise ValidationError("Quiz name is required.", "name")
    return name


def validate_quiz_create_payload(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValidationError("Request body must be a JSON object.")

    return {
        "name": _normalize_name(payload.get("name")),
        "question_ids": _normalize_question_ids(payload.get("questionIds")),
    }


def validate_quiz_update_payload(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValidationError("Request body must be a JSON object.")

    normalized: dict[str, Any] = {}

    if "name" in payload:
        normalized["name"] = _normalize_name(payload.get("name"))

    if "questionIds" in payload:
        normalized["question_ids"] = _normalize_question_ids(payload.get("questionIds"))

    if not normalized:
        raise ValidationError("At least one field must be provided for update.")

    return normalized
