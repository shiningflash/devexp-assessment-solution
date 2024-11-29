def test_create_contact(contacts, mock_client):
    # Mock response
    mock_client.request.return_value = {"id": "123", "name": "John Doe", "phone": "+123456789"}

    # Call the method
    result = contacts.create_contact(name="John Doe", phone="+123456789")

    # Assert API call and response
    mock_client.request.assert_called_once_with(
        "POST", "/contacts", json={"name": "John Doe", "phone": "+123456789"}
    )
    assert result["id"] == "123"
    assert result["name"] == "John Doe"

def test_list_contacts(contacts, mock_client):
    # Mock response
    mock_client.request.return_value = {
        "contactsList": [{"id": "123", "name": "John Doe"}],
        "pageNumber": 1,
        "pageSize": 10,
    }

    # Call the method
    result = contacts.list_contacts(page=1, max=10)

    # Assert API call and response
    mock_client.request.assert_called_once_with(
        "GET", "/contacts", params={"pageIndex": 1, "max": 10}
    )
    assert len(result["contactsList"]) == 1
    assert result["contactsList"][0]["id"] == "123"

def test_get_contact(contacts, mock_client):
    # Mock response
    mock_client.request.return_value = {"id": "123", "name": "John Doe", "phone": "+123456789"}

    # Call the method
    result = contacts.get_contact(contact_id="123")

    # Assert API call and response
    mock_client.request.assert_called_once_with("GET", "/contacts/123")
    assert result["id"] == "123"
    assert result["name"] == "John Doe"

def test_update_contact(contacts, mock_client):
    # Mock response
    mock_client.request.return_value = {"id": "123", "name": "John Doe", "phone": "+987654321"}

    # Call the method
    result = contacts.update_contact(contact_id="123", name="John Doe", phone="+987654321")

    # Assert API call and response
    mock_client.request.assert_called_once_with(
        "PATCH", "/contacts/123", json={"name": "John Doe", "phone": "+987654321"}
    )
    assert result["phone"] == "+987654321"

def test_delete_contact(contacts, mock_client):
    # Call the method
    contacts.delete_contact(contact_id="123")

    # Assert API call
    mock_client.request.assert_called_once_with("DELETE", "/contacts/123")
