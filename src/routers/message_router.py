from fastapi import APIRouter, Query, Response, status
from typing import Any, Dict
from pydantic import BaseModel, Field

from src.models import Base200Response, Base400ResponseError, IncomingMessage
from src.models.db_message import DBMessage

from src.db import DBHandler

db: DBHandler = None
message_router = APIRouter(prefix="/messages")

class MultipleMessagesResponse(Base200Response):
    data = {"messages": [DBMessage(message_id="ab34", fields={"field_name_1": "value1", "field_name_2": "value2"})]}

class SingleMessageResponse(Base200Response):
    data = {"message": DBMessage(message_id="ab34", fields={"field_name_1": "value1", "field_name_2": "value2"})}

@message_router.get("/", tags=["Messages"], response_model=MultipleMessagesResponse, responses={400: {"model": Base400ResponseError}})
async def get_all_fields_as_messages(response: Response):
    success, messages_or_error_reason = db.get_messages()
    if not success:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return Base400ResponseError(reason=messages_or_error_reason)
    return MultipleMessagesResponse(data={"messages": messages_or_error_reason})

@message_router.get("/{message_id}", tags=["Messages"], response_model=SingleMessageResponse, responses={400: {"model": Base400ResponseError}})
async def get_fields_by_message_id(response: Response, message_id: str = Query(..., regex="^[0-9A-Fa-f]{4}$")):
    success, message_or_error_reason = db.get_fields_by_message_id(message_id)
    if not success:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return Base400ResponseError(reason=message_or_error_reason)
    return SingleMessageResponse(data={"message": message_or_error_reason})

@message_router.put("/", tags=["Messages"], response_model=SingleMessageResponse, responses={400: {"model": Base400ResponseError}})
async def put_new_fields_as_message(response: Response, message: IncomingMessage):
    success, message_or_error_reason = db.upsert_message(message.message_id, message.fields)
    if not success:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return Base400ResponseError(reason=message_or_error_reason)
    return SingleMessageResponse(data={"message": message})

@message_router.delete("/{message_id}", tags=["Messages"], response_model=Base200Response, responses={400: {"model": Base400ResponseError}})
async def delete_data_by_id(response: Response, message_id: str = Query(..., regex="^[0-9A-Fa-f]{4}$")):
    success, message = db.delete_fields_by_message_id(message_id)
    if not success:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return Base400ResponseError(reason=message)
    return Base200Response()