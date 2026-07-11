from .validation import ValidationError

MIN_QUESTIONS = 3


def validate_quiz(payload: dict) -> dict:
    """Validate and normalize a raw quiz payload.

    Returns a normalized dict with keys: name, question_ids (ordered list).
    Structural rules only (name, list shape, min count, no duplicates);
    existence of the referenced questions is checked in the repository where
    the database is available.

    Raises ValidationError with a per-field error map when invalid.
    """
    if not isinstance(payload, dict):
        raise ValidationError({"payload": "must be an object"})

    errors: dict = {}
    data: dict = {}

    name = payload.get("name")
    name = name.strip() if isinstance(name, str) else ""
    if not name:
        errors["name"] = "is required and must not be empty"
    else:
        data["name"] = name

    raw_ids = payload.get("questionIds")
    if not isinstance(raw_ids, list):
        errors["questionIds"] = "must be a list of question IDs"
    else:
        # JSON integers arrive as int; reject bools and non-integers explicitly.
        ids = [v for v in raw_ids if isinstance(v, int) and not isinstance(v, bool)]
        if len(ids) != len(raw_ids):
            errors["questionIds"] = "must contain only integer question IDs"
        elif len(ids) < MIN_QUESTIONS:
            errors["questionIds"] = f"a quiz requires at least {MIN_QUESTIONS} questions"
        elif len(set(ids)) != len(ids):
            errors["questionIds"] = "duplicate question IDs are not allowed"
        else:
            data["question_ids"] = ids

    if errors:
        raise ValidationError(errors)

    return data
