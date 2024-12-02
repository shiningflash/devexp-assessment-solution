# Messaging SDK

A Python SDK designed to simplify interaction with the messaging API and webhook functionalities. It ensures seamless message management, automatic signature validation, and provides a robust foundation for developing scalable messaging applications.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Setup](#setup)
4. [Project Structure](#project-structure)
5. [Usage Guide](#usage-guide)
6. [Testing](#testing)
7. [Architecture Diagram](#architecture-diagram)
8. [Lifecycle with Example](#lifecycle-with-example)
9. [Future Improvements](#future-improvements)

---

## Overview

The **Messaging SDK** is a Python library that allows developers to interact with the messaging API effortlessly. It handles authentication, API endpoint management, and webhook processing while ensuring security through HMAC signature validation. 

### Key Objectives
- Provide a seamless developer experience.
- Simplify API interactions with auto-completion and easy-to-use methods.
- Handle webhook signature validation and event processing.

---

## Features

- **SDK Functionalities**:
  - Send messages with validation.
  - List and manage contacts and messages.
  - Retry mechanism for transient errors.
  
- **Webhook Handling**:
  - Process event notifications.
  - Validate requests using HMAC signatures.
  
- **Environment Configuration**:
  - Dynamic settings via `.env` file.
  
- **Testing**:
  - Unit, Integration, and End-to-End tests included.

---

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/messaging-sdk.git
   cd messaging-sdk
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and adjust the values:
     ```env
     BASE_URL=http://localhost:3000
     API_KEY=your-api-key
     WEBHOOK_SECRET=mySecret
     ```

4. **Browse the API:**
   - The repository includes an **OpenAPI Specification** file located at: `./docs/openapi.yaml`. This file describes the API's endpoints and can be viewed using tools like **SwaggerUI** or **Redocly**.

   - To explore the API visually, you can use Docker to run the provided tools:
     1. Ensure Docker is installed on your machine.
     2. Start the servers:
        ```bash
        docker compose up
        ```
        (If prompted, update the Docker images using `docker compose pull`).

     3. The following servers will be available:
        - **Swagger UI**: [http://localhost:8080](http://localhost:8080)
        - **Redocly**: [http://localhost:8090](http://localhost:8090)
        - **API Server**: [http://localhost:3000](http://localhost:3000) (uses a local database).

     You can use either SwaggerUI or Redocly to browse and understand the API endpoints.

---

## Usage Guide

### SDK Usage
1. Initialize the SDK:
   ```python
   from src.sdk.client import ApiClient
   from src.sdk.features.messages import Messages

   api_client = ApiClient()
   messages = Messages(api_client)

   # Send a message
   response = messages.send_message({
       "to": "+123456789",
       "content": "Hello, World!",
       "sender": "+987654321"
   })
   print(response)
   ```

2. List messages:
   ```python
   response = messages.list_messages(page=1, limit=10)
   print(response)
   ```
   
#### Comprehensive User Guide for **[SDK Usage](docs/sdk_usage.md)**
For detailed usage and examples, please refer to the **[User Guide](docs/sdk_usage.md)**.

### Webhook Setup
1. Run the webhook server:
   ```bash
   uvicorn src.server.app:app --reload --port 3010
   ```

2. Configure the API to send events to your webhook endpoint (e.g., `http://localhost:3010/webhooks`).

#### Comprehensive User Guide for **[Webhook](docs/webhook_guide.md)**
For detailed usage and examples, please refer to the [User Guide](docs/webhook_guide.md).

---

## Testing

1. Run all tests:
   ```bash
   pytest
   ```

2. Generate a coverage report:
   ```bash
   pytest --cov=src --cov-report=term-missing
   ```

3. Run specific test modules:
   ```bash
   pytest tests/unit/test_sdk/
   ```

---


## Project Structure

A detailed overview of the project structure, including descriptions of key files and directories.

## Root Directory

```
├── .github/                   # GitHub workflows for CI/CD
├── src/                       # Source code directory
├── tests/                     # Testing files for unit, integration, and E2E
├── venv/                      # Python virtual environment (not versioned)
├── .env.example               # Example environment variables
├── config.py                  # Global configuration file for SDK and server
├── docker-compose.yml         # Docker Compose configuration
├── pytest.ini                 # Pytest configuration
├── requirements.in            # Base Python dependencies
├── requirements.txt           # Locked Python dependencies
├── README.md                  # Project documentation and usage guide
├── docs/                      # Additional documentation
│   ├── sdk_usage.md           # Comprehensive SDK usage documentation
│   └── webhook_guide.md       # Webhook-specific documentation
```

---

#### `/src` Directory

The main application source code is organized as follows:

```
/src
├── sdk/                        # SDK-related functionalities
│   ├── __init__.py             # SDK initialization
│   ├── client.py               # API client for interacting with the server
│   ├── features/               # API feature modules
│   │   ├── __init__.py         # Features initialization
│   │   ├── contacts.py         # Contacts-related SDK operations
│   │   └── messages.py         # Messages-related SDK operations
│   ├── schemas/                # Schema definitions for request/response
│   │   ├── __init__.py         # Schemas initialization
│   │   ├── contacts.py         # Contact-related schemas
│   │   └── messages.py         # Message-related schemas
│   └── utils/                  # Utility modules
│       ├── __init__.py         # Utilities initialization
│       ├── exceptions.py       # Custom exceptions for error handling
│       ├── logger.py           # Logging utilities
│       ├── requests.py         # Request helpers for SDK
│       ├── retry.py            # Retry logic for transient failures
│       └── validators.py       # Validators for request/response data
├── server/                     # Webhook server implementation
│   ├── __init__.py             # Server initialization
│   ├── app.py                  # Main FastAPI application
│   └── schemas.py              # Schemas specific to the webhook server
```

---

#### `/tests` Directory

The testing framework is organized as follows:

```
/tests
├── __init__.py                 # Test package initialization
├── conftest.py                 # Pytest fixtures and test setup
├── e2e/                        # End-to-End (E2E) tests
│   ├── __init__.py             # E2E tests initialization
│   ├── test_contacts_e2e.py    # E2E tests for contacts feature
│   └── test_messages_e2e.py    # E2E tests for messages feature
├── integration/                # Integration tests
│   ├── __init__.py             # Integration tests initialization
│   ├── test_contacts_integration.py # Integration tests for contacts
│   ├── test_end_to_end_workflows.py # Comprehensive workflow tests
│   ├── test_messages_integration.py # Integration tests for messages
│   └── test_webhook.py         # Integration tests for webhook functionality
└── unit/                       # Unit tests for SDK and server
    ├── test_sdk/               # SDK-specific unit tests
    │   ├── __init__.py         # SDK unit tests initialization
    │   ├── test_client.py      # Unit tests for API client
    │   ├── test_contacts.py    # Unit tests for contacts module
    │   └── test_messages.py    # Unit tests for messages module
    └── test_server/            # Server-specific unit tests
        ├── test_route.py       # Unit tests for API routes
        └── test_signature_validation.py # Unit tests for signature validation
```

---

## Architecture Diagram

Here is the comprehensive architectural diagram for better understanding.

```plaintext
+----------------------------------------------------------+
|                          User                            |
|    (Uses the SDK to send messages, manage contacts,      |
|       and handle webhook responses programmatically)     |
+----------------------------------------------------------+
                             |
                             |  1. SDK API Calls
                             |
+----------------------------------------------------------+
|                     Messaging SDK                        |
|                                                          |
|   +---------------------------------------------+        |
|   | Features:                                   |        |
|   | - `messages.py`: Send/manage messages       |        |
|   | - `contacts.py`: Manage contact lists       |        |
|   +---------------------------------------------+        |
|                                                          |
|   +---------------------------------------------+        |
|   | Utilities:                                  |        |
|   | - `logger.py`: Logs interactions            |        |
|   | - `validators.py`: Validates signatures     |        |
|   | - `exceptions.py`: Handles errors           |        |
|   | - `retry.py`: Implements retry logic        |        |
|   +---------------------------------------------+        |
|                                                          |
|   +---------------------------------------------+        |
|   | Client (`client.py`): Handles API requests   |        |
|   | - Appends authentication headers            |        |
|   | - Sends REST API calls (e.g., GET, POST)    |        |
|   +---------------------------------------------+        |
+----------------------------------------------------------+
                             |
                             |  2. REST API Calls
                             v
+----------------------------------------------------------+
|                     API Server                           |
|                                                          |
|   +---------------------------------------------+        |
|   | Message Queue Simulation:                   |        |
|   | - Marks messages as `queued`                |        |
|   | - Simulates delivery or failure             |        |
|   +---------------------------------------------+        |
|                                                          |
|   +---------------------------------------------+        |
|   | Webhook Trigger:                            |        |
|   | - Sends event notifications to              |        |
|   |   configured Webhook Server URL             |        |
|   +---------------------------------------------+        |
+----------------------------------------------------------+
                             |
                             |  3. Webhook Event Notifications
                             v
+----------------------------------------------------------+
|                     Webhook Server                       |
|                                                          |
|   +---------------------------------------------+        |
|   | Endpoints: `/webhooks`                      |        |
|   | - Receives POST requests                    |        |
|   +---------------------------------------------+        |
|                                                          |
|   +---------------------------------------------+        |
|   | Signature Validation:                       |        |
|   | - Validates HMAC signature from             |        |
|   |   Authorization header                      |        |
|   +---------------------------------------------+        |
|                                                          |
|   +---------------------------------------------+        |
|   | Payload Processing:                         |        |
|   | - Parses incoming JSON payload              |        |
|   | - Logs event details                        |        |
|   | - Prints payload to console                 |        |
|   +---------------------------------------------+        |
|                                                          |
|   +---------------------------------------------+        |
|   | Error Handling:                            |         |
|   | - 401 Unauthorized: Invalid Signature      |         |
|   | - 422 Unprocessable Entity: Bad Payload    |         |
|   +---------------------------------------------+        |
+----------------------------------------------------------+
                             |
                             |  4. Event Logs/Responses
                             v
+----------------------------------------------------------+
|                        Logging                           |
|                                                          |
|   - SDK Logs (via `logger.py`):                          |
|     Logs all user interactions, API calls,               |
|     and errors.                                          |
|                                                          |
|   - Webhook Server Logs:                                 |
|     Logs validated events and signature failures.        |
|                                                          |
+----------------------------------------------------------+
```

---

## Lifecycle with Example

Here is the comprehensive example for lifecycle of Messaging SDK and Webhook for more understanding.

```plaintext
1. User Sends a Message
+----------------------------------------------------------+
|                        User                              |
|  - Calls `messages.send_message()` from the SDK          |
|                                                          |
|  Example Code:                                           |
|  sdk.messages.send_message(                              |
|      to="+123456789",                                    |
|      sender="+987654321",                                |
|      content="Hello, World!"                             |
|  )                                                       |
+----------------------------------------------------------+
                             |
                             v
2. SDK Sends API Request
+----------------------------------------------------------+
|                    Messaging SDK                         |
|                                                          |
|  - Validates payload (e.g., phone number format).        |
|  - Prepares headers (`Authorization: Bearer <API_KEY>`). |
|  - Sends HTTP POST request to the API.                   |
|                                                          |
|  Request:                                                |
|  POST /messages                                          |
|  Headers:                                                |
|  - Authorization: Bearer <API_KEY>                       |
|  Body:                                                   |
|  {                                                       |
|      "to": "+123456789",                                 |
|      "content": "Hello, World!",                         |
|      "sender": "+987654321"                              |
|  }                                                       |
+----------------------------------------------------------+
                             |
                             v
3. API Server Processes the Message
+----------------------------------------------------------+
|                      API Server                          |
|                                                          |
|  - Marks message as `queued`.                            |
|  - Simulates a delay for processing.                     |
|  - Updates the message status to `delivered` or `failed`.|
|                                                          |
|  Example Response:                                       |
|  {                                                       |
|      "id": "msg123",                                     |
|      "status": "queued",                                 |
|      "createdAt": "2024-12-01T10:00:00Z"                 |
|  }                                                       |
+----------------------------------------------------------+
                             |
                             v
4. API Triggers Webhook Notification
+----------------------------------------------------------+
|                      Webhook Trigger                     |
|                                                          |
|  - Sends a POST request to the configured                |
|    webhook URL (e.g., `http://localhost:3010/webhooks`). |
|                                                          |
|  Request:                                                |
|  POST /webhooks                                          |
|  Headers:                                                |
|  - Authorization: Bearer <HMAC-SIGNATURE>                |
|  Body:                                                   |
|  {                                                       |
|      "id": "msg123",                                     |
|      "status": "delivered",                              |
|      "deliveredAt": "2024-12-01T12:00:00Z"               |
|  }                                                       |
+----------------------------------------------------------+
                             |
                             v
5. Webhook Server Processes the Event
+----------------------------------------------------------+
|                     Webhook Server                       |
|                                                          |
|  - Validates the HMAC signature.                         |
|  - Parses the payload.                                   |
|  - Logs and processes the event.                         |
|                                                          |
|  Example Log:                                            |
|  - "Webhook received: {'id': 'msg123', 'status': 'delivered', | 
|     'deliveredAt': '2024-12-01T12:00:00Z'}"              |
|                                                          |
|  Example Processing Code:                                |
|  try:                                                    |
|      verify_signature(payload, signature, secret)        |
|      print(f"Message {payload['id']} delivered.")        |
|  except ValueError:                                      |
|      print("Signature validation failed.")               |
+----------------------------------------------------------+
                             |
                             v
6. Event Logging and Completion
+----------------------------------------------------------+
|                        Logging                           |
|                                                          |
|  - SDK logs the sent message status and errors (if any). |
|  - Webhook server logs validated payloads and events.    |
|                                                          |
|  Final Console Output:                                   |
|  "Message msg123 delivered."                             |
+----------------------------------------------------------+
```

---

## Future Improvements

- Add more advanced retry strategies for transient errors.
- Implement caching for frequently used API requests.
- Enhance webhook security with IP whitelisting.
- Extend SDK functionality to support additional API endpoints.
