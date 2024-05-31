import json
from dataclasses import dataclass, field
from typing import Optional, List

from loguru import logger
from openai.types.chat import ChatCompletionChunk
from openai.types.chat.chat_completion_chunk import Choice, ChoiceDelta
from pydantic import BaseModel, validator
from rich.console import Group
from rich.panel import Panel

from chat_with_functions.util import indent_content, omit


class FunctionCall(BaseModel):
    name: str
    arguments_json: str  # This is a JSON string based on the usage of json.loads(response_message["function_call"]["arguments"])

    @property
    def arguments(self):
        return json.loads(self.arguments_json)


class Message(BaseModel):
    role: str
    content: str = ""
    name: str = None
    function_call: Optional[FunctionCall] = None

    @validator("content", pre=True, always=True)
    def content_must_not_be_none(cls, content):
        assert content is not None, "content must not be None"
        return content

    def __str__(self):
        # TODO indent the content
        indented = indent_content(self.content)

        return f"""{self.role}:
{indented}"""

    def __rich__(self):
        return Panel(
            Group(
                self.role,
                self.content
            ),
            title=self.name or self.role
        )


@dataclass
class MyChoice:
    finish_reason: str
    index: int
    message: Message

    @classmethod
    def from_dict(cls, data):
        data = data.copy()
        if 'function_call' in data['message']:
            fc = FunctionCall(**data['message']['function_call'])
            data['message']['function_call'] = fc
        message = Message(**data['message'])
        return cls(finish_reason=data['finish_reason'], index=data['index'], message=message)


@dataclass
class Usage:
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int

    def get_cost(self, model_name):
        return OPENAI_COST_PER_1K_TOKEN[model_name]["prompt"] * self.prompt_tokens / 1000 \
            + OPENAI_COST_PER_1K_TOKEN[model_name]["completion"] * self.completion_tokens / 1000


@dataclass
class ChatCompletion:
    choices: List[MyChoice]
    created: int
    id: str
    model: str
    object: Optional[str]
    usage: Optional[Usage]
    prompt_filter_results: Optional[List[dict]] = field(default=None)
    system_fingerprint: Optional[str] = field(default=None)

    @classmethod
    def from_dict(cls, data):
        choices = [MyChoice.from_dict(c) for c in data['choices']]
        try:
            usage = Usage(**data['usage'])

            return cls(choices=choices,
                       created=data['created'],
                       id=data['id'],
                       model=data['model'],
                       object=data['object'],
                       usage=usage,
                       )
        except Exception as e:
            logger.error(e)
            logger.error(f"input:{data}")
            raise e

    @property
    def result_text(self):
        return self.choices[0].message.content


@dataclass
class ChoiceAccumulator:
    finish_reason: Optional[str] = field(default=None)
    index: Optional[int] = field(default=None)
    role: Optional[str] = field(default=None)
    content: Optional[str] = field(default=None)

    fc_name: Optional[str] = field(default=None)
    fc_arguments: Optional[str] = field(default=None)

    def add(self, choice: Choice):
        """
        :param choise:Choice
        choice:
            - finish_reason: str
            - index: int
            - content:str
            - function_call:str
            - role:str
        :return:
        """
        #logger.info(f"acc choice:{choice}")
        delta: ChoiceDelta = choice.delta
        if choice.finish_reason is not None:
            self.finish_reason = choice.finish_reason
        if choice.index is not None:
            self.index = choice.index
        if delta.content is not None:
            if self.content is None:
                self.content = delta.content
            else:
                self.content += delta.content
        if delta.function_call is not None:
            match (self.fc_name, delta.function_call.name):
                case (None, str() as name):
                    self.fc_name = name
                case (_, None):
                    pass
                case (str() , str() as txt):
                    self.fc_name += txt
            if delta.function_call.arguments is not None:
                if self.fc_arguments is None:
                    self.fc_arguments = delta.function_call.arguments
                else:
                    self.fc_arguments += delta.function_call.arguments
        if delta.role is not None:
            self.role = delta.role

    def to_choice(self):
        if self.fc_name is not None:
            function_call = FunctionCall(name=self.fc_name, arguments_json=self.fc_arguments)
            name = self.fc_name
        else:
            function_call = None
            name = None

        message = Message(role=self.role, content=self.content or "", name=name, function_call=function_call)
        return MyChoice(finish_reason=self.finish_reason, index=self.index, message=message)


@dataclass
class ResponseAccumulator:
    choices: dict[int, ChoiceAccumulator] = field(default_factory=dict)
    other_data: dict = field(default_factory=dict)

    def add(self, chunk: ChatCompletionChunk):
        for choice in chunk.choices:
            idx = choice.index
            if idx not in self.choices:
                self.choices[idx] = ChoiceAccumulator()
            self.choices[idx].add(choice)
        # self.other_data = omit(chunk, 'choices')
        self.other_data = chunk.dict(exclude={'choices'})

    def to_chat_completion(self) -> ChatCompletion:
        logger.info(f"to_chat_completion:{self.choices}")
        choices = [self.choices[i].to_choice() for i in sorted(self.choices.keys())]
        if 'usage' not in self.other_data:
            self.other_data['usage'] = None
        return ChatCompletion(choices=choices, **self.other_data)


class ParameterProperty(BaseModel):
    type: str  # must be either 'string' or 'number'
    description: str


class FunctionParameters(BaseModel):
    type: str  # must be 'object'
    properties: dict[str, ParameterProperty]
    required: list[str]


class FunctionSpec(BaseModel):
    name: str
    description: str
    parameters: FunctionParameters


class FunctionSpecs(BaseModel):
    functions: list[FunctionSpec]


OPENAI_COST_PER_1K_TOKEN = {
    "gpt-3.5-turbo": dict(
        prompt=0.002,
        completion=0.002
    ),
    "gpt-4": dict(
        prompt=0.03,
        completion=0.06
    )
}
