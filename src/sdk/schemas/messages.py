from pydantic import BaseModel, Field, validator
from typing import Optional, List


class CreateMessageRequest(BaseModel):
    """
    Schema for creating a new message.
    """
    to: str = Field(
        ...,
        pattern=r"^\+\d{1,15}$",
        description="Recipient's phone number in E.164 format."
    )
    content: str = Field(
        ...,
        min_length=1,
        max_length=160,
        description="Message content with a maximum of 160 characters."
    )
    sender: str = Field(
        ...,
        pattern=r"^\+\d{1,15}$",
        description="Sender's phone number in E.164 format."
    )


class Message(BaseModel):
    """
    Schema for a message resource.
    """
    id: str
    from_: str = Field(..., alias="from", description="Sender's phone number.")
    to: str
    content: str
    status: str  # queued, delivered, or failed
    createdAt: str


class ListMessagesResponse(BaseModel):
    """
    Schema for listing messages with pagination support.
    """
    messages: List[Message]
    page: int
    quantityPerPage: int
