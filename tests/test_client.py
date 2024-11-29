import pytest
from unittest.mock import patch, MagicMock
from src.sdk.client import ApiClient
from src.sdk.utils.exceptions import UnauthorizedError, NotFoundError, ServerError, ApiError
from src.sdk.config import Config


@pytest.fixture
def api_client():
    """Fixture to initialize the ApiClient."""
    with patch.object(Config, "validate"), patch.object(Config, "BASE_URL", "http://localhost:3000"), patch.object(Config, "API_KEY", "test-api-key"):
        return ApiClient()


def test_initialization(api_client):
    """Test that the ApiClient initializes correctly."""
    assert api_client.base_url == "http://localhost:3000"
    assert api_client.api_key == "test-api-key"


def test_initialization_failure():
    """Test initialization failure when Config validation raises an exception."""
    with patch.object(Config, "validate", side_effect=Exception("Config validation failed")):
        with pytest.raises(Exception, match="Config validation failed"):
            ApiClient()


@patch("src.sdk.client.requests.request")
def test_request_success(mock_request, api_client):
    """Test a successful API request."""
    # Mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.ok = True
    mock_response.json.return_value = {"success": True}
    mock_request.return_value = mock_response

    # Perform request
    response = api_client.request("GET", "/contacts")

    # Assertions
    mock_request.assert_called_once_with(
        "GET",
        "http://localhost:3000/contacts",
        headers={
            "Authorization": "Bearer test-api-key",
            "Content-Type": "application/json"
        }
    )
    assert response == {"success": True}


@patch("src.sdk.client.requests.request")
def test_request_unauthorized(mock_request, api_client):
    """Test 401 UnauthorizedError."""
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.ok = False
    mock_response.text = "Unauthorized"
    mock_request.return_value = mock_response

    with pytest.raises(UnauthorizedError, match="Unauthorized. Check your API key."):
        api_client.request("GET", "/contacts")


@patch("src.sdk.client.requests.request")
def test_request_not_found(mock_request, api_client):
    """Test 404 NotFoundError."""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.ok = False
    mock_response.text = "Not Found"
    mock_request.return_value = mock_response

    with pytest.raises(NotFoundError, match="Resource not found."):
        api_client.request("GET", "/contacts/non-existent")


@patch("src.sdk.client.requests.request")
def test_request_server_error(mock_request, api_client):
    """Test 500 ServerError."""
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.ok = False
    mock_response.text = "Internal Server Error"
    mock_request.return_value = mock_response

    with pytest.raises(ServerError, match="Server error. Please try again later."):
        api_client.request("GET", "/contacts")


@patch("src.sdk.client.requests.request")
def test_request_generic_error(mock_request, api_client):
    """Test a generic ApiError for unexpected status codes."""
    mock_response = MagicMock()
    mock_response.status_code = 418
    mock_response.ok = False
    mock_response.text = "I'm a teapot"
    mock_request.return_value = mock_response

    with pytest.raises(ApiError, match="Unhandled API Error: 418: I'm a teapot"):
        api_client.request("GET", "/contacts")


@patch("src.sdk.client.requests.request")
def test_retry_logic(mock_request, api_client):
    """Test retry logic for transient errors."""
    mock_response = MagicMock()
    mock_response.status_code = 503
    mock_response.ok = False
    mock_request.side_effect = [mock_response, mock_response, mock_response]

    with pytest.raises(RuntimeError, match="Failed after 3 retries."):
        api_client.request("GET", "/contacts")

    # Ensure retries happened 3 times
    assert mock_request.call_count == 3
