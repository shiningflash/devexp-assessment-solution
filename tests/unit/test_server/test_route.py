import json

from fastapi.testclient import TestClient
from src.server.app import app
from config import settings

from src.sdk.utils.validators import generate_signature

client = TestClient(app)


def test_webhook_valid_request():
    payload = {
        "id": "msg123",
        "status": "delivered",
        "deliveredAt": "2024-12-01T12:00:00Z",
    }
    # Serialize payload to JSON with stable formatting
    serialized_payload = json.dumps(payload, separators=(",", ":")).encode("utf-8")

    # Generate a valid signature for the serialized payload
    signature = generate_signature(payload, settings.WEBHOOK_SECRET)

    # Send the request
    response = client.post(
        "/webhooks",
        content=serialized_payload,  # Send raw serialized JSON payload
        headers={"Authorization": f"Bearer {signature}"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Webhook processed successfully."}


def test_webhook_invalid_signature():
    payload = {
        "id": "msg123",
        "status": "delivered",
        "deliveredAt": "2024-12-01T12:00:00Z",
    }
    response = client.post(
        "/webhooks",
        json=payload,  # Send payload as JSON
        headers={"Authorization": "Bearer invalid-signature"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid signature."}


def test_webhook_invalid_payload():
    invalid_payload = {
        "id": "msg123",
        "status": 12345,  # Invalid status type
    }
    # Serialize payload for signature generation
    serialized_payload = json.dumps(invalid_payload, separators=(",", ":")).encode("utf-8")
    signature = generate_signature(invalid_payload, settings.WEBHOOK_SECRET)

    response = client.post(
        "/webhooks",
        json=invalid_payload,  # Use json= to send as JSON
        headers={"Authorization": f"Bearer {signature}"}
    )
    assert response.status_code == 422  # Ensure validation catches the invalid type
