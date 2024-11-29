from typing import List, Dict
from ..client import ApiClient
from ..utils.logger import logger


class Messages:
    """
    A class to manage message-related API operations.
    """

    def __init__(self, client: ApiClient):
        self.client = client

    def send_message(self, to: str, content: str, sender: str) -> Dict:
        """
        Sends a new message.

        Args:
            to (str): The recipient's contact ID or phone number.
            content (str): The text content of the message.
            sender (str): The sender's phone number.

        Returns:
            dict: The sent message details.
        """
        logger.info(f"Sending message from {sender} to {to}")
        payload = {"to": to, "content": content, "from": sender}
        return self.client.request("POST", "/messages", json=payload)

    def list_messages(self, page: int = 1, limit: int = 10) -> List[Dict]:
        """
        Lists sent messages with pagination.

        Args:
            page (int): The page number.
            limit (int): The maximum number of messages per page.

        Returns:
            list: A list of sent message details.
        """
        logger.info(f"Listing messages: page={page}, limit={limit}")
        params = {"page": page, "limit": limit}
        return self.client.request("GET", "/messages", params=params)

    def get_message(self, message_id: str) -> Dict:
        """
        Retrieves a message by ID.

        Args:
            message_id (str): The unique ID of the message.

        Returns:
            dict: The message details.
        """
        logger.info(f"Fetching message with ID: {message_id}")
        return self.client.request("GET", f"/messages/{message_id}")
