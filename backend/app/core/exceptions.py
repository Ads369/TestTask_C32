class AppException(Exception):
    """Base exception for application"""

    status_code = 500
    detail = "Internal Server Error"


class DatabaseError(AppException):
    """Raised when database connection fails"""

    status_code = 503
    detail = "Database error"


class RedisError(AppException):
    status_code = 503
    detail = "Redis error"


class ExternalAPIClientError(AppException):
    status_code = 503
    detail = "Max retries exceeded"
