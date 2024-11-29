def test_send_message(messages, mock_client):
    # Mock response
    mock_client.request.return_value = {
        "id": "456",
        "from": "+111111111",
        "to": "+222222222",
        "content": "Hello, World!",
        "status": "queued",
    }

    # Call the method
    result = messages.send_message(to="+222222222", content="Hello, World!", sender="+111111111")

    # Assert API call and response
    mock_client.request.assert_called_once_with(
        "POST", "/messages", json={"to": "+222222222", "content": "Hello, World!", "from": "+111111111"}
    )
    assert result["status"] == "queued"

def test_list_messages(messages, mock_client):
    # Mock response
    mock_client.request.return_value = {
        "messages": [{"id": "456", "content": "Hello, World!", "status": "delivered"}],
        "page": 1,
        "quantityPerPage": 10,
    }

    # Call the method
    result = messages.list_messages(page=1, limit=10)

    # Assert API call and response
    mock_client.request.assert_called_once_with(
        "GET", "/messages", params={"page": 1, "limit": 10}
    )
    assert len(result["messages"]) == 1
    assert result["messages"][0]["status"] == "delivered"

def test_get_message(messages, mock_client):
    # Mock response
    mock_client.request.return_value = {
        "id": "456",
        "from": "+111111111",
        "to": "+222222222",
        "content": "Hello, World!",
        "status": "delivered",
    }

    # Call the method
    result = messages.get_message(message_id="456")

    # Assert API call and response
    mock_client.request.assert_called_once_with("GET", "/messages/456")
    assert result["status"] == "delivered"
