from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Literal
from datetime import datetime


class CreateMessageRequest(BaseModel):
    """
    Schema for creating a new message.

    Attributes:
        to (str): Recipient's phone number in E.164 format.
        content (str): Message content, with a maximum length of 160 characters.
        sender (str): Sender's phone number in E.164 format.
    """
    to: str = Field(
        ...,
        description="Recipient's phone number in E.164 format.",
        json_schema_extra={"example": "+1234567890"}
    )
    content: str = Field(
        ...,
        min_length=1,
        max_length=160,
        description="Message content, limited to 160 characters.",
        json_schema_extra={"example": "Hello, World!"}
    )
    sender: str = Field(
        ...,
        description="Sender's phone number in E.164 format.",
        json_schema_extra={"example": "+0987654321"}
    )

    @field_validator("to", "sender")
    def validate_phone_number(cls, value):
        if not value.startswith("+"):
            raise ValueError("Phone numbers must include the '+' prefix.")
        if not value[1:].isdigit():
            raise ValueError("Phone numbers must contain only digits after the '+' prefix.")
        return value


class Message(BaseModel):
    """
    Schema for a message resource.

    Attributes:
        id (str): Unique identifier for the message.
        from_ (str): Sender's phone number.
        to (str): Recipient's phone number.
        content (str): Message content.
        status (str): Message status, one of 'queued', 'delivered', or 'failed'.
        created_at (datetime): Timestamp when the message was created.
    """
    id: str = Field(..., description="Unique identifier for the message.", json_schema_extra={"example": "msg123"})
    from_: str = Field(
        ..., 
        alias="from", 
        description="Sender's phone number.", 
        json_schema_extra={"example": "+0987654321"}
    )
    to: str = Field(..., description="Recipient's phone number.", json_schema_extra={"example": "+1234567890"})
    content: str = Field(..., description="Message content.", json_schema_extra={"example": "Hello, World!"})
    status: Literal["queued", "delivered", "failed"] = Field(
        ..., 
        description="Message status.", 
        json_schema_extra={"example": "delivered"}
    )
    created_at: datetime = Field(
        ..., 
        alias="createdAt", 
        description="Timestamp when the message was created.", 
        json_schema_extra={"example": "2024-12-01T12:00:00Z"}
    )

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class ListMessagesResponse(BaseModel):
    """
    Schema for listing messages with pagination support.

    Attributes:
        messages (List[Message]): List of message objects.
        page (int): Current page number.
        quantity_per_page (int): Number of messages per page.
    """
    messages: List[Message] = Field(..., description="List of message objects.")
    page: int = Field(..., description="Current page number.", json_schema_extra={"example": 1})
    quantity_per_page: int = Field(
        ..., 
        alias="quantityPerPage", 
        description="Number of messages per page.", 
        json_schema_extra={"example": 10}
    )

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )
