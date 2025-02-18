from fastapi import HTTPException


class DatabaseConnectionError(HTTPException):
    def __init__(self):
        super().__init__(status_code=503, detail="Database connection error")


class ConstraintViolationError(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=409, detail=f"Data constraint violation: {message}"
        )


class RedisConnectionError(HTTPException):
    def __init__(self):
        super().__init__(status_code=503, detail="Redis connection error")


class RedisDataError(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=503, detail=f"Redis data error: {message}")
