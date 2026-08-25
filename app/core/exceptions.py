from typing import Any


class AppException(Exception):
    status_code: int = 500

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundException(AppException):
    status_code: int = 404

    def __init__(self, entity: str, field: str, value: Any):
        message = f"{entity} with {field} '{value}' not found"
        super().__init__(message)


class AlreadyExistsException(AppException):
    status_code: int = 409

    def __init__(self, entity: str, field: str, value: Any):
        message = f"{entity} with {field} '{value}' already exists"
        super().__init__(message)
