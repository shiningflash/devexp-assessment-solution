from typing import Dict, List
from httpx import HTTPStatusError

from ..client import ApiClient
from src.schemas.messages import CreateMessageRequest, Message, ListMessagesResponse
from src.core.validators import validate_request, validate_response
from src.core.exceptions import handle_exceptions, handle_404_error
from src.core.logger import logger
from src.core.security import verify_signature


class Messages:
    """
    Messages SDK module for managing messages via the API.

    Provides methods for sending, listing, and retrieving messages.
    """

    def __init__(self, client: ApiClient):
        """
        Initialize the Messages module.

        Args:
            client (ApiClient): The shared API client instance.
        """
        self.client = client

    @validate_request(CreateMessageRequest)
    @validate_response(Message)
    @handle_exceptions
    def send_message(self, payload: Dict) -> Message:
        """
        Send a new message to a contact.

        Args:
            payload (dict): A dictionary containing 'to', 'content', and 'sender'.

        Returns:
            Message: The details of the sent message.
        """
        logger.info(f"Sending message with payload: {payload}")
        return self.client.request("POST", "/messages", json=payload)

    @validate_response(ListMessagesResponse)
    @handle_exceptions
    def list_messages(self, page: int = 1, limit: int = 10) -> ListMessagesResponse:
        """
        List all sent messages with pagination.

        Args:
            page (int): The page number to retrieve. Defaults to 1.
            limit (int): The maximum number of messages per page. Defaults to 10.

        Returns:
            ListMessagesResponse: A paginated list of sent messages.
        """
        params = {"page": page, "limit": limit}
        logger.info(f"Listing messages with params: {params}")
        return self.client.request("GET", "/messages", params=params)

    @validate_response(Message)
    @handle_exceptions
    def get_message(self, message_id: str) -> Message:
        """
        Retrieve a specific message by ID.

        Args:
            message_id (str): The unique ID of the message.

        Returns:
            Message: The retrieved message details.
        """
        logger.info(f"Fetching message with ID: {message_id}")
        try:
            return self.client.request("GET", f"/messages/{message_id}")
        except HTTPStatusError as e:
            handle_404_error(e, message_id, "Message")
    
    
    def validate_webhook_signature(self, raw_body: bytes, signature: str, secret: str):
        """
        Validate the webhook signature using the SDK.

        Args:
            raw_body (bytes): Raw request body from webhook.
            signature (str): Authorization header containing the signature.
            secret (str): Secret key for signature validation.

        Raises:
            ValueError: If the signature validation fails.
        """
        logger.info("Validating webhook signature through SDK.")
        verify_signature(raw_body, signature, secret)
