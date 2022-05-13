from typing import Any, Dict, List, Literal
from fastapi import APIRouter, Query, Response, status

from src.db import DBHandler

from src.models import Base200Response, Base400ResponseError
from src.models.db_field import DBField

db: DBHandler = None
field_router = APIRouter(prefix="/fields")

class MultipleFieldsResponse(Base200Response):
    data: Dict[str, List[DBField]] = {"fields": [DBField(message_id="ab34", name="field_name", value=123)]}

class SingleFieldResponse(Base200Response):
    data: Dict[str, DBField] = {"field": DBField(message_id="ab34", name="field_name", value=123)}

@field_router.get("/{message_id}", tags=["Fields"], response_model=MultipleFieldsResponse, responses={400: {"model": Base400ResponseError}})
async def get_fields_by_message_id(response: Response, message_id: str = Query(..., regex="^[0-9A-Fa-f]{4}$")):
    success, message_or_error_reason = db.get_fields_by_message_id(message_id)
    if not success:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return Base400ResponseError(reason=message_or_error_reason)
    return MultipleFieldsResponse(data={"fields": message_or_error_reason.fields})

@field_router.get("/{message_id}/{field_name}", tags=["Fields"], response_model=SingleFieldResponse, responses={400: {"model": Base400ResponseError}})
async def get_field_by_message_id_and_field_name(response: Response,  field_name: str, message_id: str = Query(..., regex="^[0-9A-Fa-f]{4}$")):
    success, field_or_error_reason = db.get_field_by_name_and_message_id(field_name, message_id)
    if not success:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return Base400ResponseError(reason=field_or_error_reason)
    return SingleFieldResponse(data={"field": field_or_error_reason})

@field_router.put("/{message_id}/{field_name}", tags=["Fields"], response_model=SingleFieldResponse, responses={400: {"model": Base400ResponseError}})
async def upsert_field_by_message_id_and_field_name(response: Response, field_name: str, value: Any, message_id: str = Query(..., regex="^[0-9A-Fa-f]{4}$") ):
    success, field_or_error_reason = db.upsert_field(message_id, field_name, value)
    if not success:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return Base400ResponseError(reason=field_or_error_reason)
    return SingleFieldResponse(data={"field": field_or_error_reason})

@field_router.delete("/{message_id}/{field_name}", tags=["Fields"], response_model=Base200Response, responses={400: {"model": Base400ResponseError}})
async def delete_field_by_message_id_and_field_name(response: Response, field_name: str, message_id: str = Query(..., regex="^[0-9A-Fa-f]{4}$")):
    success, reason = db.delete_field_by_name_and_message_id(field_name, message_id)
    if not success:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return Base400ResponseError(reason=reason)
    return Base200Response()
    