import pytest
from unittest.mock import MagicMock, patch
from src.sdk.features.contacts import Contacts
from src.sdk.client import ApiClient
from src.sdk.utils.exceptions import UnauthorizedError, NotFoundError, ApiError, ValidationError
from src.sdk.schemas.contacts import CreateContactRequest


@pytest.fixture
def api_client():
    """Fixture to initialize a mock ApiClient."""
    return MagicMock(spec=ApiClient)


@pytest.fixture
def contacts(api_client):
    """Fixture to initialize the Contacts class."""
    return Contacts(client=api_client)


def test_create_contact_success(contacts, api_client):
    """Test successfully creating a contact."""
    # Mock response
    api_client.request.return_value = {"id": "123", "name": "John Doe", "phone": "+123456789"}

    # Call method
    payload = {"name": "John Doe", "phone": "+123456789"}
    response = contacts.create_contact(payload=payload)

    # Assertions
    api_client.request.assert_called_once_with("POST", "/contacts", json=payload)
    assert response["id"] == "123"
    assert response["name"] == "John Doe"


def test_create_contact_validation_error(contacts):
    """Test validation error when payload is invalid."""
    payload = {"name": "John Doe"}  # Missing 'phone'
    with pytest.raises(ValueError, match="Invalid payload"):
        contacts.create_contact(payload=payload)


def test_create_contact_api_error(contacts, api_client):
    """Test API error during contact creation."""
    # Mock API error
    api_client.request.side_effect = ApiError("Unhandled API Error")

    payload = {"name": "John Doe", "phone": "+123456789"}
    with pytest.raises(ApiError, match="Unhandled API Error"):
        contacts.create_contact(payload=payload)


def test_list_contacts_success(contacts, api_client):
    """Test successfully listing contacts."""
    # Mock response
    mock_response = {
        "contactsList": [{"id": "123", "name": "John Doe", "phone": "+123456789"}],
        "pageNumber": 1,
        "pageSize": 10,
    }
    api_client.request.return_value = mock_response

    # Call method
    response = contacts.list_contacts(page=1, max=10)

    # Assertions
    api_client.request.assert_called_once_with("GET", "/contacts", params={"pageIndex": 1, "max": 10})
    assert len(response["contactsList"]) == 1
    assert response["contactsList"][0]["id"] == "123"


def test_get_contact_success(contacts, api_client):
    """Test successfully retrieving a specific contact."""
    # Mock response
    mock_response = {"id": "123", "name": "John Doe", "phone": "+123456789"}
    api_client.request.return_value = mock_response

    # Call method
    response = contacts.get_contact(contact_id="123")

    # Assertions
    api_client.request.assert_called_once_with("GET", "/contacts/123")
    assert response["id"] == "123"
    assert response["name"] == "John Doe"


def test_get_contact_not_found(contacts, api_client):
    """Test 404 Not Found error when retrieving a contact."""
    # Mock 404 error
    api_client.request.side_effect = NotFoundError("Resource not found.")

    with pytest.raises(NotFoundError, match="Resource not found."):
        contacts.get_contact(contact_id="non-existent")


def test_update_contact_success(contacts, api_client):
    """Test successfully updating a contact."""
    # Mock response
    mock_response = {"id": "123", "name": "Jane Doe", "phone": "+987654321"}
    api_client.request.return_value = mock_response

    # Call method
    payload = {"name": "Jane Doe", "phone": "+987654321"}
    response = contacts.update_contact(contact_id="123", payload=payload)

    # Assertions
    api_client.request.assert_called_once_with("PATCH", "/contacts/123", json=payload)
    assert response["name"] == "Jane Doe"


def test_delete_contact_success(contacts, api_client):
    """Test successfully deleting a contact."""
    # Call method
    contacts.delete_contact(contact_id="123")

    # Assertions
    api_client.request.assert_called_once_with("DELETE", "/contacts/123")


def test_delete_contact_not_found(contacts, api_client):
    """Test deleting a non-existent contact."""
    # Mock 404 error
    api_client.request.side_effect = NotFoundError("Resource not found.")

    with pytest.raises(NotFoundError, match="Resource not found."):
        contacts.delete_contact(contact_id="non-existent")
