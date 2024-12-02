from pydantic import BaseModel, Field
from typing import Optional
from typing import Literal


class WebhookPayload(BaseModel):
    id: str = Field(..., description="Unique message identifier")
    status: Literal["queued", "delivered", "failed"]
    deliveredAt: Optional[str] = Field(None, description="Delivery timestamp if delivered")
