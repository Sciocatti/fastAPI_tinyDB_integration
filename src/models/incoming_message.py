from typing import Any, Dict
from pydantic import BaseModel, Field

class IncomingMessage(BaseModel):
    message_id: str = Field(
        ...,
        title="HEX_ID",
        description="The HEX_ID for the requested message.",
        regex="^[0-9A-Fa-f]{4}$"
    )
    fields: Dict[str, Any]