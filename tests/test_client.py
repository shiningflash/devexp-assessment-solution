import pytest
from src.sdk.client import ApiClient
from src.sdk.config import Config

def test_client_initialization():
    Config.API_KEY = "test-key"
    client = ApiClient()
    assert client.api_key == "test-key"

def test_request_headers(mocker):
    mock_request = mocker.patch("src.sdk.client.requests.request")
    Config.API_KEY = "test-key"
    client = ApiClient()

    client.request("GET", "/test")
    mock_request.assert_called_with(
        "GET",
        "http://localhost:3000/test",
        headers={"Authorization": "Bearer test-key", "Content-Type": "application/json"}
    )
