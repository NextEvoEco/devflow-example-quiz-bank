VALID_ANSWERS = ("A", "B", "C", "D")
VALID_DIFFICULTIES = ("Easy", "Medium", "Hard")
DEFAULT_DIFFICULTY = "Medium"

REQUIRED_TEXT_FIELDS = ("question", "a", "b", "c", "d")


class ValidationError(ValueError):
    """Raised when a question payload fails the V1 validation rules.

    Carries a per-field ``errors`` mapping so callers (API layer, tests) can
    report exactly which fields were invalid.
    """

    def __init__(self, errors: dict):
        self.errors = errors
        message = "; ".join(f"{field}: {msg}" for field, msg in errors.items())
        super().__init__(message)


def validate_question(payload: dict) -> dict:
    """Validate and normalize a raw question payload.

    Returns a normalized dict with keys: question, a, b, c, d, correct, difficulty.
    Raises ValidationError with a per-field error map when the payload is invalid.
    """
    if not isinstance(payload, dict):
        raise ValidationError({"payload": "must be an object"})

    errors: dict = {}
    data: dict = {}

    for field in REQUIRED_TEXT_FIELDS:
        value = payload.get(field)
        text = value.strip() if isinstance(value, str) else ""
        if not text:
            errors[field] = "is required and must not be empty"
        else:
            data[field] = text

    correct_raw = payload.get("correct")
    correct = correct_raw.strip().upper() if isinstance(correct_raw, str) else ""
    if not correct:
        errors["correct"] = "is required"
    elif correct not in VALID_ANSWERS:
        errors["correct"] = f"must be one of {', '.join(VALID_ANSWERS)}"
    else:
        data["correct"] = correct

    difficulty_raw = payload.get("difficulty")
    if difficulty_raw is None or (isinstance(difficulty_raw, str) and not difficulty_raw.strip()):
        data["difficulty"] = DEFAULT_DIFFICULTY
    elif isinstance(difficulty_raw, str):
        difficulty = difficulty_raw.strip().capitalize()
        if difficulty not in VALID_DIFFICULTIES:
            errors["difficulty"] = f"must be one of {', '.join(VALID_DIFFICULTIES)}"
        else:
            data["difficulty"] = difficulty
    else:
        errors["difficulty"] = f"must be one of {', '.join(VALID_DIFFICULTIES)}"

    if errors:
        raise ValidationError(errors)

    return data
