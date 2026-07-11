VALID_CORRECT_ANSWERS = frozenset({"A", "B", "C", "D"})
VALID_DIFFICULTIES = frozenset({"Easy", "Medium", "Hard"})
DEFAULT_DIFFICULTY = "Medium"

REQUIRED_OPTION_FIELDS = ("a", "b", "c", "d")


class ValidationError(Exception):
    def __init__(self, message: str, errors: dict[str, str] | None = None):
        super().__init__(message)
        self.message = message
        self.errors = errors or {}


def _require_non_empty_text(value: object, field: str) -> str:
    if value is None:
        raise ValidationError(
            "Invalid question payload.",
            {field: f"{field} is required."},
        )

    text = str(value).strip()
    if not text:
        raise ValidationError(
            "Invalid question payload.",
            {field: f"{field} must not be empty."},
        )
    return text


def validate_question_payload(payload: dict, *, partial: bool = False) -> dict:
    if not isinstance(payload, dict):
        raise ValidationError("Question payload must be an object.")

    validated: dict = {}
    errors: dict[str, str] = {}

    if not partial or "question" in payload:
        try:
            validated["question"] = _require_non_empty_text(
                payload.get("question"), "question"
            )
        except ValidationError as exc:
            errors.update(exc.errors)

    for field in REQUIRED_OPTION_FIELDS:
        if not partial or field in payload:
            try:
                validated[field] = _require_non_empty_text(payload.get(field), field)
            except ValidationError as exc:
                errors.update(exc.errors)

    if not partial or "correct" in payload:
        correct = payload.get("correct")
        if correct is None or str(correct).strip() == "":
            errors["correct"] = "correct is required."
        else:
            normalized_correct = str(correct).strip().upper()
            if normalized_correct not in VALID_CORRECT_ANSWERS:
                errors["correct"] = 'correct must be one of "A", "B", "C", or "D".'
            else:
                validated["correct"] = normalized_correct

    if "difficulty" in payload:
        difficulty = payload.get("difficulty")
        if difficulty is None or str(difficulty).strip() == "":
            validated["difficulty"] = DEFAULT_DIFFICULTY
        else:
            normalized_difficulty = str(difficulty).strip().lower()
            difficulty_map = {
                "easy": "Easy",
                "medium": "Medium",
                "hard": "Hard",
            }
            if normalized_difficulty in difficulty_map:
                validated["difficulty"] = difficulty_map[normalized_difficulty]
            else:
                errors["difficulty"] = (
                    'difficulty must be one of "Easy", "Medium", or "Hard".'
                )
    elif not partial:
        validated["difficulty"] = DEFAULT_DIFFICULTY

    if errors:
        raise ValidationError("Invalid question payload.", errors)

    return validated
