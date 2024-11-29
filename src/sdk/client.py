import requests
from typing import Any
from .config import Config
from .utils.logger import logger
from .utils.requests import handle_request_errors


class ApiClient:
    """
    A base API client for handling HTTP requests with authentication and error handling.
    """

    def __init__(self):
        # Validate configuration
        Config.validate()
        self.base_url = Config.BASE_URL
        self.api_key = Config.API_KEY

    @handle_request_errors
    def request(self, method: str, endpoint: str, **kwargs) -> Any:
        """
        Sends an HTTP request to the API server.
        Args:
            method (str): The HTTP method (GET, POST, etc.).
            endpoint (str): The API endpoint path (e.g., "/contacts").
            **kwargs: Additional arguments for the request.

        Returns:
            dict: The JSON response from the API.
        """
        url = f"{self.base_url}{endpoint}"
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self.api_key}"
        headers["Content-Type"] = "application/json"

        logger.info(f"Sending {method} request to {url}")
        response = requests.request(method, url, headers=headers, **kwargs)
        logger.info(f"Received {response.status_code} response: {response.text}")
        response.raise_for_status()
        return response.json()
