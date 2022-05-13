from pydantic import BaseModel, Field
from typing import Any

class DBField(BaseModel):
    message_id: str= Field(
        ...,
        regex="^[0-9A-Fa-f]{4}$"
    )
    name: str
    value: Any = None