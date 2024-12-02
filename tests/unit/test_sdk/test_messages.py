import pytest
from unittest.mock import MagicMock, patch
from src.sdk.features.messages import Messages
from src.sdk.client import ApiClient
from src.sdk.utils.exceptions import UnauthorizedError, NotFoundError, ApiError, PayloadValidationError
from src.sdk.schemas.messages import CreateMessageRequest


@pytest.fixture
def api_client():
    """Fixture to initialize a mock ApiClient."""
    return MagicMock(spec=ApiClient)


@pytest.fixture
def messages(api_client):
    """Fixture to initialize the Messages class."""
    return Messages(client=api_client)


def test_send_message_success(messages, api_client):
    """Test successfully sending a message."""
    # Mock response
    api_client.request.return_value = {
        "id": "msg123",
        "from": "+123456789",
        "to": "+987654321",
        "content": "Hello, World!",
        "status": "queued",
        "createdAt": "2024-11-28T10:00:00Z"
    }

    # Call method
    payload = {"to": "+987654321", "content": "Hello, World!", "sender": "+123456789"}
    response = messages.send_message(payload=payload)

    # Assertions
    api_client.request.assert_called_once_with("POST", "/messages", json=payload)
    assert response["id"] == "msg123"
    assert response["status"] == "queued"
    assert response["content"] == "Hello, World!"


def test_send_message_validation_error(messages):
    """Test validation error when payload is invalid."""
    payload = {"to": "+987654321"}  # Missing 'content' and 'sender'
    with pytest.raises(ValueError, match="Invalid payload"):
        messages.send_message(payload=payload)


def test_send_message_api_error(messages, api_client):
    """Test API error during message sending."""
    # Mock API error
    api_client.request.side_effect = ApiError("Unhandled API Error")

    payload = {"to": "+987654321", "content": "Hello, World!", "sender": "+123456789"}
    with pytest.raises(ApiError, match="Unhandled API Error"):
        messages.send_message(payload=payload)


def test_list_messages_success(messages, api_client):
    """Test successfully listing messages."""
    # Mock response
    mock_response = {
        "messages": [
            {
                "id": "msg123",
                "from": "+123456789",
                "to": "+987654321",
                "content": "Hello, World!",
                "status": "queued",
                "createdAt": "2024-11-28T10:00:00Z"
            }
        ],
        "page": 1,
        "quantityPerPage": 10
    }
    api_client.request.return_value = mock_response

    # Call method
    response = messages.list_messages(page=1, limit=10)

    # Assertions
    api_client.request.assert_called_once_with("GET", "/messages", params={"page": 1, "limit": 10})
    assert len(response["messages"]) == 1
    assert response["messages"][0]["id"] == "msg123"


def test_get_message_success(messages, api_client):
    """Test successfully retrieving a specific message."""
    # Mock response
    mock_response = {
        "id": "msg123",
        "from": "+123456789",
        "to": "+987654321",
        "content": "Hello, World!",
        "status": "queued",
        "createdAt": "2024-11-28T10:00:00Z"
    }
    api_client.request.return_value = mock_response

    # Call method
    response = messages.get_message(message_id="msg123")

    # Assertions
    api_client.request.assert_called_once_with("GET", "/messages/msg123")
    assert response["id"] == "msg123"
    assert response["content"] == "Hello, World!"


def test_get_message_not_found(messages, api_client):
    """Test 404 Not Found error when retrieving a message."""
    # Mock 404 error
    api_client.request.side_effect = NotFoundError("Resource not found.")

    with pytest.raises(NotFoundError, match="Resource not found."):
        messages.get_message(message_id="non-existent")
