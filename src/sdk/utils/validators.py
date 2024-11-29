from pydantic import ValidationError
from functools import wraps
from typing import Any, Callable
from ..utils.logger import logger


def validate_request(model: Any):
    """
    Decorator to validate request payloads using a Pydantic model.
    Logs detailed errors for invalid inputs.
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if "payload" in kwargs:
                    model(**kwargs["payload"])  # Validate the payload
                return func(*args, **kwargs)
            except ValidationError as e:
                logger.error(f"Validation Error: {e.json()}")
                for error in e.errors():
                    logger.error(f"Field: {error['loc']}, Error: {error['msg']}")
                raise ValueError(f"Invalid payload: {e}")
        return wrapper
    return decorator


def validate_response(model: Any):
    """
    Decorator to validate API responses using a Pydantic model.
    Logs detailed errors for invalid responses.
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            try:
                model(**response)  # Validate the response
                return response
            except ValidationError as e:
                logger.error(f"Response Validation Error: {e.json()}")
                for error in e.errors():
                    logger.error(f"Field: {error['loc']}, Error: {error['msg']}")
                raise ValueError(f"Invalid response: {e}")
        return wrapper
    return decorator
