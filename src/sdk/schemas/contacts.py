from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


class CreateContactRequest(BaseModel):
    """
    Schema for creating a new contact.
    """
    name: str = Field(..., description="The name of the contact.")
    phone: str = Field(
        ..., 
        pattern=r"^\+\d{1,15}$", 
        description="Phone number in E.164 format."
    )

    @field_validator("name")
    def validate_name(cls, value):
        if len(value) < 1 or len(value) > 50:
            raise ValueError("Name must be between 1 and 50 characters.")
        return value


class Contact(BaseModel):
    """
    Schema for a contact resource.
    """
    id: str
    name: str
    phone: str


class ListContactsResponse(BaseModel):
    """
    Schema for listing contacts with pagination support.
    """
    contactsList: List[Contact]
    pageNumber: int
    pageSize: int
