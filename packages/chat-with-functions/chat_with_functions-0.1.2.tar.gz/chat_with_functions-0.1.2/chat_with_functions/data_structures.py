from typing import List

from pydantic import BaseModel

from chat_with_functions.openai_api import Message, FunctionSpec


class OpenAICallArgs(BaseModel):
    messages: List[Message]
    functions: list[FunctionSpec] = None
    function_call:str = "auto"
