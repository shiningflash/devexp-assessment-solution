# SDK Usage Guide

Welcome to the SDK Usage Guide for the **messaging-sdk**. This guide will walk you through the installation, configuration, and practical usage of the SDK, providing detailed examples and instructions for integrating the SDK into your applications.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Basic Usage](#basic-usage)
    - [Sending Messages](#sending-messages)
    - [Managing Contacts](#managing-contacts)
5. [Advanced Usage](#advanced-usage)
6. [Error Handling](#error-handling)
7. [Testing](#testing)
8. [Logging](#logging)

---

## Introduction

The `messaging-sdk` is a Python library designed to simplify interactions with the messaging and contacts API. The SDK provides:

- Simplified API interactions without requiring manual configuration of authentication headers.
- IDE-friendly auto-completion for seamless development.
- Robust retry mechanisms for handling transient errors.
- Built-in validation to ensure API requests meet expected formats.

---

## Installation

To install the SDK, use `pip`:

```bash
pip install -r requirements.txt
```

---

## Configuration

1. Copy the `.env.example` file to `.env` in the root directory:

    ```bash
    cp .env.example .env
    ```

2. Open `.env` and update the variables accordingly.

---

## Basic Usage

### Sending Messages

The SDK provides a straightforward way to send messages:

```python
from src.sdk.features.messages import Messages
from src.sdk.client import ApiClient

client = ApiClient()
messages = Messages(client)

# Prepare the payload
payload = {
    "to": "+123456789",
    "content": "Hello, world!",
    "sender": "+987654321"
}

# Send the message
response = messages.send_message(payload=payload)
```

### Managing Contacts

You can create, list, and delete contacts using the SDK:

```python
from src.sdk.features.contacts import Contacts

contacts = Contacts(client)

# Create a new contact
new_contact = {
    "name": "John Doe",
    "phone": "+123456789"
}
response = contacts.create_contact(new_contact)

# List all contacts
contacts_list = contacts.list_contacts()

# Delete a contact
contacts.delete_contact(contact_id="contact123")
```

---

## Advanced Usage

### Pagination

Retrieve paginated lists for messages or contacts:

```python
# Retrieve paginated messages
messages_list = messages.list_messages(page=1, limit=5)
print(messages_list)

# Retrieve paginated contacts
contacts_list = contacts.list_contacts(page=1, max=5)
print(contacts_list)
```

### Retry Mechanisms

The SDK automatically retries failed requests for transient errors (e.g., `503 Service Unavailable`). You can customize retry logic in the `src/sdk/utils/retry.py` module.

---

## Error Handling

The SDK raises specific exceptions for various error scenarios:

- `UnauthorizedError`: Raised for `401 Unauthorized` responses.
- `NotFoundError`: Raised for `404 Not Found` responses.
- `ServerError`: Raised for `500 Internal Server Error` responses.
- `ApiError`: Raised for other unexpected API errors.

Example:

```python
try:
    messages.list_messages()
except UnauthorizedError as e:
    print(f"Authentication failed: {e}")
except ApiError as e:
    print(f"Unexpected error: {e}")
```

---

## Testing

The SDK includes unit, integration, and end-to-end tests. To run all tests:

```bash
pytest
```

To generate a coverage report:

```bash
pytest --cov=src --cov-report=term-missing
```

---

## Logging

The SDK includes comprehensive logging for debugging and auditing. Logs are categorized as follows:

- **Console Logs**: Informational and error logs for immediate feedback.
- **File Logs**: Warnings and errors logged to `logs/app.log`.

Example of enabling logger in your application:

```python
from src.sdk.utils.logger import logger

logger.info("Application started.")
```
