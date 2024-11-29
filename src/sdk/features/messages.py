from typing import Dict, List
from ..client import ApiClient
from ..schemas.messages import CreateMessageRequest, Message, ListMessagesResponse
from ..utils.validators import validate_request, validate_response
from ..utils.exceptions import handle_exceptions
from ..utils.logger import logger


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
        return self.client.request("GET", f"/messages/{message_id}")
