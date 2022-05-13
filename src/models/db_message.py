from pydantic import BaseModel, Field
from typing import Any, Dict

class DBMessage(BaseModel):
    message_id: str = Field(
        ...,
        regex="^[0-9A-Fa-f]{4}$"
    ),
    fields: Dict[str, Any] = {}