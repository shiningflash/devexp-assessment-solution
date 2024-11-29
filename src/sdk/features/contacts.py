from typing import List, Dict
from ..client import ApiClient
from ..utils.logger import logger


class Contacts:
    """
    A class to manage contact-related API operations.
    """

    def __init__(self, client: ApiClient):
        self.client = client

    def create_contact(self, name: str, phone: str) -> Dict:
        """
        Creates a new contact.

        Args:
            name (str): The contact's name.
            phone (str): The contact's phone number.

        Returns:
            dict: The created contact details.
        """
        logger.info(f"Creating contact: {name}, {phone}")
        payload = {"name": name, "phone": phone}
        return self.client.request("POST", "/contacts", json=payload)

    def list_contacts(self, page: int = 1, max: int = 10) -> List[Dict]:
        """
        Lists existing contacts with pagination.

        Args:
            page (int): The page number.
            max (int): The maximum number of contacts per page.

        Returns:
            list: A list of contact details.
        """
        logger.info(f"Listing contacts: page={page}, max={max}")
        params = {"pageIndex": page, "max": max}
        return self.client.request("GET", "/contacts", params=params)

    def get_contact(self, contact_id: str) -> Dict:
        """
        Retrieves a contact by ID.

        Args:
            contact_id (str): The unique ID of the contact.

        Returns:
            dict: The contact details.
        """
        logger.info(f"Fetching contact with ID: {contact_id}")
        return self.client.request("GET", f"/contacts/{contact_id}")

    def update_contact(self, contact_id: str, name: str, phone: str) -> Dict:
        """
        Updates a contact's details.

        Args:
            contact_id (str): The unique ID of the contact.
            name (str): The updated name.
            phone (str): The updated phone number.

        Returns:
            dict: The updated contact details.
        """
        logger.info(f"Updating contact {contact_id}: {name}, {phone}")
        payload = {"name": name, "phone": phone}
        return self.client.request("PATCH", f"/contacts/{contact_id}", json=payload)

    def delete_contact(self, contact_id: str) -> None:
        """
        Deletes a contact by ID.

        Args:
            contact_id (str): The unique ID of the contact.
        """
        logger.info(f"Deleting contact with ID: {contact_id}")
        self.client.request("DELETE", f"/contacts/{contact_id}")
        logger.info(f"Contact {contact_id} deleted successfully.")
