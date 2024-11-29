import pytest
from src.sdk.client import ApiClient
from src.sdk.features.contacts import Contacts
from src.sdk.features.messages import Messages

@pytest.fixture
def mock_client(mocker):
    client = ApiClient()
    mocker.patch.object(client, "request")
    return client

@pytest.fixture
def contacts(mock_client):
    return Contacts(mock_client)

@pytest.fixture
def messages(mock_client):
    return Messages(mock_client)
