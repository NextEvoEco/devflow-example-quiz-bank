MIN_QUIZ_QUESTIONS = 3


class QuizValidationError(Exception):
    def __init__(self, message: str, errors: dict[str, str] | None = None):
        super().__init__(message)
        self.message = message
        self.errors = errors or {}


def _normalize_question_ids(value: object) -> list[int]:
    if not isinstance(value, list):
        raise QuizValidationError(
            "Invalid quiz payload.",
            {"questionIds": "questionIds must be an array of question IDs."},
        )

    question_ids: list[int] = []
    for index, item in enumerate(value):
        if isinstance(item, bool) or not isinstance(item, int):
            raise QuizValidationError(
                "Invalid quiz payload.",
                {"questionIds": f"questionIds[{index}] must be an integer."},
            )
        question_ids.append(item)

    return question_ids


def validate_quiz_create_payload(payload: dict) -> dict:
    if not isinstance(payload, dict):
        raise QuizValidationError("Quiz payload must be an object.")

    errors: dict[str, str] = {}
    validated: dict = {}

    name = payload.get("name")
    if name is None or str(name).strip() == "":
        errors["name"] = "name is required."
    else:
        validated["name"] = str(name).strip()

    try:
        question_ids = _normalize_question_ids(payload.get("questionIds"))
    except QuizValidationError as exc:
        errors.update(exc.errors)
        question_ids = []

    if "questionIds" not in errors:
        if len(question_ids) < MIN_QUIZ_QUESTIONS:
            errors["questionIds"] = (
                f"A quiz must include at least {MIN_QUIZ_QUESTIONS} questions."
            )
        elif len(set(question_ids)) != len(question_ids):
            errors["questionIds"] = "questionIds must not contain duplicates."
        else:
            validated["questionIds"] = question_ids

    if errors:
        raise QuizValidationError("Invalid quiz payload.", errors)

    return validated


def validate_quiz_update_payload(payload: dict) -> dict:
    if not isinstance(payload, dict):
        raise QuizValidationError("Quiz payload must be an object.")

    if "name" not in payload and "questionIds" not in payload:
        raise QuizValidationError(
            "Invalid quiz payload.",
            {"_form": "At least one of name or questionIds must be provided."},
        )

    errors: dict[str, str] = {}
    validated: dict = {}

    if "name" in payload:
        name = payload.get("name")
        if name is None or str(name).strip() == "":
            errors["name"] = "name must not be empty."
        else:
            validated["name"] = str(name).strip()

    if "questionIds" in payload:
        try:
            question_ids = _normalize_question_ids(payload.get("questionIds"))
        except QuizValidationError as exc:
            errors.update(exc.errors)
            question_ids = []

        if "questionIds" not in errors:
            if len(question_ids) < MIN_QUIZ_QUESTIONS:
                errors["questionIds"] = (
                    f"A quiz must include at least {MIN_QUIZ_QUESTIONS} questions."
                )
            elif len(set(question_ids)) != len(question_ids):
                errors["questionIds"] = "questionIds must not contain duplicates."
            else:
                validated["questionIds"] = question_ids

    if errors:
        raise QuizValidationError("Invalid quiz payload.", errors)

    return validated
