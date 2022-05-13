from typing import Any, Dict
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

from src.routers import message_router, field_router
from src.models import Base200Response

from src.db import DBHandler

messages = {
    "1234": {
        "value1": 123,
        "value2": 321
    }
}

db = DBHandler('fastapi.json')

message_router.messages = messages
field_router.messages = messages

message_router.db = db
field_router.db = db

app = FastAPI()
app.include_router(message_router.message_router)
app.include_router(field_router.field_router)

# ! OpenAPI spec: http://127.0.0.1:8000/openapi.json
# ! API Docs:     http://127.0.0.1:8000/docs
# * Operations:
# *     GET:    To read data
# *     POST:   To create data
# *     PUT:    To update data -> As 'messages' is not actually something that exists, this will be the same as POST
# *     DELETE: To delete data

@app.get("/", tags=["System"])
async def root():
    return {"message": "Hello World"}

@app.get("/alive", tags=["System"])
async def get_alive():
    return Base200Response()
