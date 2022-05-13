from typing import Any
import tinydb
from pydantic import ValidationError

if __name__ == "__main__":
    # ! We always run python stuff from the top directory. However, to test files
    # ! while developing we can do this hack: If starting from this file, then
    # ! run as-if starting from top directory. So we can import stuff as we normally would.
    import os, sys
    src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    sys.path.append(src_path)

from src.models.db_message import DBMessage
from src.models.db_field import DBField

class DBHandler:
    def __init__(self, path: str) -> None:
        self.db = tinydb.TinyDB(path)

    def get_fields(self):
        fields = self.db.all()
        model_fields = []
        for field in fields:
            model_fields.append(DBField(**field))
        return True, model_fields

    def get_messages(self):
        _success, fields = self.get_fields()
        messages = {}
        for field in fields:
            field: DBField
            message = messages.get(field.message_id, {})
            message[field.name] = field.value
            messages[field.message_id] = message
        model_messages = []
        for message_id in messages:
            model_messages.append(DBMessage(message_id=message_id, fields=messages[message_id]))

        return True, model_messages

    def get_fields_by_message_id(self, message_id: str):
        try:
            _validation = DBMessage(message_id=message_id)
        except ValidationError:
            return False, f"Invalid 'message_id' format. Must be '^[0-9A-Fa-f]{4}$', but got '{message_id}.'"

        query = tinydb.Query()
        message_fields = self.db.search(query.message_id == message_id)
        if not message_fields:
            return False, f"Message with ID '{message_id}' does not exist."

        response_message_fields = {}
        for field in message_fields:
            response_message_fields[field["name"]] = field["value"]
        return(True, DBMessage(message_id=message_id, fields=response_message_fields))

    def get_field_by_name_and_message_id(self, name: str, message_id: str):
        try:
            _validation = DBField(name=name, message_id=message_id)
        except ValidationError:
            return False, f"Invalid field format."

        query = tinydb.Query()
        fields = self.db.search((query.message_id == message_id) & (query.name == name))
        if not fields:
            return False, f"No matching fields found."

        if len(fields) > 1:
            return False, f"Multiple result found. Expected 1."

        return True, fields[0]

    def upsert_field(self, message_id: str, name: str, value: Any):
        try:
            model_field = DBField(name=name, message_id=message_id, value=value)
            query = tinydb.Query()
            self.db.upsert(model_field.dict(), (query.message_id == message_id) & (query.name == name))
            return True, model_field
        except ValidationError:
            return False, f"Invalid field format."

    def upsert_message(self, message_id: str, fields: dict):
        try:
            _validation = DBMessage(message_id=message_id)
        except ValidationError:
            return False, f"Invalid 'message_id' format. Must be '^[0-9A-Fa-f]{4}$', but got '{message_id}.'"

        for field_name in fields:
            success, model_field_or_reason = self.upsert_field(message_id, field_name, fields[field_name])
            if not success:
                return success, model_field_or_reason

        return(self.get_fields_by_message_id(message_id))

    def delete_fields_by_message_id(self, message_id: str):
        query = tinydb.Query()
        self.db.remove(query.message_id == message_id)
        return(True, None)

    def delete_field_by_name_and_message_id(self, name: str, message_id: str):
        query = tinydb.Query()
        self.db.remove( (query.message_id == message_id) & (query.name == name))
        return(True, None)
        
    def truncate_all(self):
        self.db.truncate()


if __name__ == "__main__":
    json_file = "db_test.json"
    db = DBHandler(json_file)
    # db.truncate_all()
    message = {
        "message_id": "1235",
        "fields": {
            "test1": 123,
            "test2": 321,
            "test3": ["1", 4]
        }
    }

    messages = db.get_messages()
    print(messages)
    db.upsert_message(**message)
    messages = db.get_messages()
    print(db.get_messages())
    
    


