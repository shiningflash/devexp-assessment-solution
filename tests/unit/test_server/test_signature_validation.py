import pytest
import hmac
import hashlib
import json

from config import settings
from src.sdk.utils.validators import verify_signature
from src.sdk.utils.validators import generate_signature


def test_valid_signature():
    payload = {"id": "msg123", "status": "delivered"}
    serialized_payload = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    signature = generate_signature(payload, settings.WEBHOOK_SECRET)
    assert verify_signature(serialized_payload, signature, settings.WEBHOOK_SECRET) is True

def test_invalid_signature():
    payload = {"id": "msg123", "status": "delivered"}
    invalid_signature = "invalidsignature"
    with pytest.raises(ValueError, match="Signature validation failed."):
        verify_signature(payload, invalid_signature, settings.WEBHOOK_SECRET)

def test_empty_signature():
    payload = {"id": "msg123", "status": "delivered"}
    empty_signature = ""
    with pytest.raises(ValueError, match="Signature validation failed."):
        verify_signature(payload, empty_signature, settings.WEBHOOK_SECRET)
