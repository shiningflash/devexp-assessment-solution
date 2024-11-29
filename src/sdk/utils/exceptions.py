from ..utils.logger import logger


class ApiError(Exception):
    """
    Base exception class for all API-related errors.

    Attributes:
        message (str): The error message describing the issue.
        status_code (int, optional): HTTP status code associated with the error (if applicable).
    """

    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        if status_code:
            logger.error(f"[API Error] {status_code}: {message}")
        else:
            logger.error(f"[API Error]: {message}")

    def __str__(self):
        return f"{self.message} (HTTP {self.status_code})" if self.status_code else self.message


class UnauthorizedError(ApiError):
    """
    Exception raised for 401 Unauthorized errors.
    """

    def __init__(self, message: str = "Unauthorized access. Check your API key."):
        super().__init__(message, status_code=401)
        logger.warning("[UnauthorizedError] Ensure your API key is valid.")


class NotFoundError(ApiError):
    """
    Exception raised for 404 Not Found errors.
    """

    def __init__(self, message: str = "Requested resource not found."):
        super().__init__(message, status_code=404)
        logger.warning("[NotFoundError] Resource does not exist.")


class ServerError(ApiError):
    """
    Exception raised for 500+ Server Error responses.
    """

    def __init__(self, message: str = "Internal server error. Please try again later.", status_code: int = 500):
        super().__init__(message, status_code=status_code)
        logger.error("[ServerError] The server encountered an issue.")


class ValidationError(ApiError):
    """
    Exception raised for validation errors in payloads or responses.

    Attributes:
        errors (list, optional): List of validation errors with field-level details.
    """

    def __init__(self, message: str = "Validation failed.", errors: list = None):
        super().__init__(message)
        self.errors = errors or []
        logger.error(f"[ValidationError] {message}")
        if self.errors:
            for error in self.errors:
                logger.error(f"Validation Detail: Field - {error['loc']}, Error - {error['msg']}")


class RateLimitError(ApiError):
    """
    Exception raised for 429 Rate Limit Exceeded responses.
    """

    def __init__(self, message: str = "Rate limit exceeded. Please wait and retry."):
        super().__init__(message, status_code=429)
        logger.warning("[RateLimitError] API rate limit reached. Retry after some time.")


class TransientError(ApiError):
    """
    Exception raised for transient server errors like 502 Bad Gateway or 503 Service Unavailable.
    """

    def __init__(self, message: str = "Transient server error. Please retry.", status_code: int = None):
        super().__init__(message, status_code=status_code)
        logger.warning(f"[TransientError] {message} (HTTP {status_code})")


def handle_exceptions(func):
    """
    Decorator to handle exceptions consistently across the SDK.

    Args:
        func (Callable): The function to wrap.

    Returns:
        Callable: The wrapped function with exception handling.

    Raises:
        ApiError: Reraises known API errors for logging and debugging.
        RuntimeError: Raises unexpected errors as runtime exceptions.
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ApiError as api_error:
            logger.error(f"[ApiError]: {api_error}")
            raise
        except Exception as unexpected_error:
            logger.error(f"[Unhandled Exception]: {unexpected_error}")
            raise RuntimeError(f"An unexpected error occurred: {unexpected_error}")

    return wrapper
