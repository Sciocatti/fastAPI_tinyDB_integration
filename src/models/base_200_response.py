from typing import Dict
from pydantic import BaseModel

class Base200Response(BaseModel):
    status: str = "ok"
    data: dict = None

class Base400ResponseError(BaseModel):
    status: str = "error"
    reason: str = "Some error reason."