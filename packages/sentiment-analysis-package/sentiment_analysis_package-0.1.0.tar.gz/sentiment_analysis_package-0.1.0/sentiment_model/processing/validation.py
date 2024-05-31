from pydantic import BaseModel, ValidationError
from typing import List

class TextInput(BaseModel):
    text: str

class TextsInput(BaseModel):
    texts: List[TextInput]

def validate_inputs(input_data):
    try:
        TextsInput(**input_data)
        return True, None
    except ValidationError as e:
        return False, e.errors()
