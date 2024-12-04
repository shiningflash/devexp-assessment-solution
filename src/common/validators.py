import hmac
import json
import hashlib

from pydantic import ValidationError
from functools import wraps
from typing import Any, Callable
from .logger import logger


def validate_request(model: Any):
    """
    Decorator to validate request payloads using a Pydantic model.
    Logs detailed errors for invalid inputs and halts execution.
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "payload" in kwargs:
                try:
                    logger.debug("Entering validate_request decorator.")
                    logger.info(f"Validating request payload: {kwargs['payload']}")
                    model(**kwargs["payload"])  # Validate the payload
                    logger.debug("Exiting validate_request decorator.")
                except ValidationError as e:
                    logger.error(f"Request Validation Error: {e.json()}")
                    for error in e.errors():
                        logger.error(f"Field: {error['loc']}, Error: {error['msg']}")
                    raise ValueError("Invalid payload")  # Halt execution here
            else:
                logger.warning("No payload provided for validation.")
            return func(*args, **kwargs)
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
            logger.debug("Entering validate_response decorator.")
            response = func(*args, **kwargs)
            try:
                model(**response)  # Validate the response
                logger.debug("Exiting validate_response decorator.")
                return response
            except ValidationError as e:
                logger.error(f"Response Validation Error: {e.json()}")
                for error in e.errors():
                    logger.error(f"Field: {error['loc']}, Error: {error['msg']}")
                raise ValueError(f"Invalid response: {e}")
        return wrapper
    return decorator


def generate_signature(payload: dict, secret: str) -> str:
    """
    Generate HMAC signature for a given payload.

    Args:
        payload (dict): The payload to sign.
        secret (str): The secret key.

    Returns:
        str: Hexadecimal HMAC signature.
    """
    try:
        # Serialize payload to JSON with stable formatting
        message = json.dumps(payload, separators=(",", ":")).encode("utf-8")  # Convert to bytes
        hmac_instance = hmac.new(secret.encode("utf-8"), message, hashlib.sha256)
        return hmac_instance.hexdigest()
    except Exception as e:
        raise ValueError(f"Error generating signature: {str(e)}")


def verify_signature(message: bytes, signature: str, secret: str):
    """
    Validate the HMAC signature of incoming webhooks.

    Args:
        message (bytes): Raw request body in bytes.
        signature (str): Authorization header signature.
        secret (str): Webhook secret.

    Raises:
        ValueError: If the signature is invalid.
    """
    logger.info("Validating HMAC signature.")
    try:
        # Create HMAC using secret and SHA256
        hmac_instance = hmac.new(secret.encode("utf-8"), message, hashlib.sha256)
        expected_signature = hmac_instance.hexdigest()

        # Validate the signature
        if not hmac.compare_digest(expected_signature, signature):
            raise ValueError("Invalid signature.")

        logger.info("HMAC signature validated successfully.")
        return True

    except Exception as e:
        logger.error(f"Error validating signature: {str(e)}")
        raise ValueError("Signature validation failed.")
