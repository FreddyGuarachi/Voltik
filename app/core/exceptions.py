from typing import Any


class AppException(Exception):
    status_code: int = 500

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundException(AppException):
    status_code: int = 404

    def __init__(self, entity: str, value: Any):
        message = f"{entity} with '{value}' not found"
        super().__init__(message)


class AlreadyExistsException(AppException):
    status_code: int = 409

    def __init__(self, entity: str, value: Any):
        message = f"{entity} with '{value}' already exists"
        super().__init__(message)


class InsufficientStockError(AppException):
    status_code: int = 409

    def __init__(self, entity: str, available: int):
        message = f"Insufficient stock for '{entity}' (available: {available})"
        super().__init__(message)


class InvalidCredentialsError(AppException):
    status_code = 401

    def __init__(self):
        message = f"Invalid username or password"
        super().__init__(message)
