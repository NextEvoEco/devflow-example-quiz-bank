class ValidationError(ValueError):
    def __init__(self, message: str, field: str | None = None) -> None:
        self.field = field
        super().__init__(message)
