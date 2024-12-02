import json

from fastapi import FastAPI, HTTPException, Header, Request
from config import settings
from ..sdk.client import ApiClient
from .schemas import WebhookPayload
from ..sdk.features.messages import Messages
from ..sdk.utils.validators import verify_signature
from src.sdk.utils.logger import webhook_logger as logger

# Initialize FastAPI app
app = FastAPI()

# SDK instance for validation
# Initialize ApiClient and Messages
api_client = ApiClient()
messages_sdk = Messages(client=api_client)


@app.post("/webhooks")
async def handle_webhook(
    payload: WebhookPayload,  # Ensure FastAPI uses this schema for validation
    authorization: str = Header(...),
    request: Request = None,
):
    """
    Webhook endpoint to process incoming events.
    """
    try:
        # Extract raw request body
        raw_body = await request.body()

        # Validate signature using the SDK
        verify_signature(raw_body, authorization.removeprefix("Bearer "), settings.WEBHOOK_SECRET)

        # Log the received payload
        logger.info(f"Webhook received: {payload.model_dump()}")

        # Simulate event processing (printing is sufficient per task)
        print(f"Processed webhook payload: {payload.model_dump()}")

        return {"message": "Webhook processed successfully."}

    except ValueError as e:
        logger.error(f"Signature validation failed: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid signature.")

    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error.")
