from typing import Any

from backend.errors import ValidationError

VALID_CORRECT_ANSWERS = {"A", "B", "C", "D"}
VALID_DIFFICULTIES = {"Easy", "Medium", "Hard"}
DEFAULT_DIFFICULTY = "Medium"

REQUIRED_OPTION_FIELDS = ("a", "b", "c", "d")


def validate_question_payload(
    payload: dict[str, Any],
    *,
    require_all_fields: bool = True,
) -> dict[str, Any]:
    """Validate and normalize a question payload for create or update."""
    normalized: dict[str, Any] = {}

    if require_all_fields or "question" in payload:
        question_text = _require_non_empty_string(payload.get("question"), "question")

        if question_text is None:
            raise ValidationError("Question text is required.", "question")
        normalized["question"] = question_text

    for field in REQUIRED_OPTION_FIELDS:
        if require_all_fields or field in payload:
            option_text = _require_non_empty_string(payload.get(field), field)

            if option_text is None:
                raise ValidationError(f"Option {field.upper()} is required.", field)
            normalized[field] = option_text

    if require_all_fields or "correct" in payload:
        correct = payload.get("correct")
        if correct is None or not isinstance(correct, str):
            raise ValidationError("Correct answer is required.", "correct")

        correct = correct.strip().upper()
        if correct not in VALID_CORRECT_ANSWERS:
            raise ValidationError(
                "Correct answer must be one of A, B, C, or D.",
                "correct",
            )
        normalized["correct"] = correct

    if "difficulty" in payload:
        difficulty = payload.get("difficulty")
        if difficulty is None or (
            isinstance(difficulty, str) and not difficulty.strip()
        ):
            normalized["difficulty"] = DEFAULT_DIFFICULTY
        else:
            if not isinstance(difficulty, str):
                raise ValidationError("Difficulty must be a string.", "difficulty")
            difficulty = difficulty.strip().title()
            if difficulty not in VALID_DIFFICULTIES:
                raise ValidationError(
                    "Difficulty must be one of Easy, Medium, or Hard.",
                    "difficulty",
                )
            normalized["difficulty"] = difficulty
    elif require_all_fields:
        normalized["difficulty"] = DEFAULT_DIFFICULTY

    return normalized


def _require_non_empty_string(value: Any, field: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValidationError(f"{field} must be a string.", field)
    stripped = value.strip()
    if not stripped:
        return None
    return stripped
