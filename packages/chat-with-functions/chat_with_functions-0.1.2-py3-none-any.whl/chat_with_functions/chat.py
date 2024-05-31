import asyncio
import json
import traceback
from asyncio import Future
from dataclasses import dataclass, replace
from json import JSONDecodeError
from typing import Callable, Awaitable, List

import rich
from loguru import logger
from rich.console import Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax

from chat_with_functions.data_structures import OpenAICallArgs
from chat_with_functions.function_calling_structure import IFunctionEnv, IStreamHandler, EnvFuncCallResult
from chat_with_functions.openai_api import Message, FunctionCall, ChatCompletion
from chat_with_functions.streaming import StreamResponse


@dataclass
class ChatWithFunctions:
    """
    An immutable chat. any operation on this chat will return a new chat.
    with this model, you can chat with functions.
    """
    chat_stream: Callable[[OpenAICallArgs], Awaitable[StreamResponse]]
    messages: List[Message]
    function_env: IFunctionEnv
    stream_handler: IStreamHandler

    def extract_triple_quotes(self, text: str, suffix='json') -> str:
        """
        extract the json string from the text.
        """
        return text.split(f"```{suffix}")[1].split("```")[0]

    def pure(self):
        return replace(self, function_env=self.function_env.empty(), messages=[])

    async def ask_to_fix_json(self, json_str, remaining_tries=3) -> str:
        try:
            json.loads(json_str)
            return json_str
        except JSONDecodeError as e:
            if remaining_tries == 0:
                raise e
            # the problem is it's json in json.
            prompt = f"""
Fix the following json string:
```json
{json_str}
```
The decoder raised the following error:
```python
{e}
```
Make sure to start the answer with "```json" and end with "```".
"""
            logger.info(f"asking to fix json with prompt:\n{prompt}")
            chat = await self.ask(prompt)
            new_json_str = self.extract_triple_quotes(chat.messages[-1].content)
            logger.info(f"got new json:\n{new_json_str}")
            return await chat.ask_to_fix_json(new_json_str, remaining_tries - 1)

    async def ask_to_load_python(self, python_expr, remaining_tries=3) -> dict:
        try:
            return eval(python_expr)
        except Exception as e:
            if remaining_tries == 0:
                raise e
            # the problem is it's json in json.
            prompt = f"""
Fix the following data into a eval-able python expression:
```data
{python_expr}
```
The decoder raised the following error:
```python
{e}
```
Make sure to start the answer with "```python" and end with "```".
Example:
```python
{{
    "name":"send_msg",
    "code":\"\"\"
        print("hello")
\"\"\",
}}
```
"""
            logger.info(f"asking to fix python with prompt:\n{prompt}")
            # actually, this chat automatically calls py_def, so
            chat = await self.ask(prompt)
            new_python_expr = self.extract_triple_quotes(chat.messages[-1].content, 'python')
            logger.info(f"got new python:\n{new_python_expr}")
            return await chat.ask_to_load_python(new_python_expr, remaining_tries - 1)

    async def fix_function_call(self, function_call: FunctionCall, remaining_retry=3) -> EnvFuncCallResult:
        """

        0. Recursively look into the data and fix?
            Do the json escaping programmatically.
        1. add metadata to AIFunction so that we can fix the data here
        2. add callback to AIFunction so that the AIFunction can fix it...
            - This seems to be better approachj
        3. convert json into xml or other escape-free format?
            - we can for example ask the json to be converted into eval-able python code.
        :param remaining_retry:
        :return:
        """

        arguments = await self.ask_to_load_python(function_call.arguments_json, remaining_tries=3)
        function_call = function_call.copy(update=dict(arguments_json=json.dumps(arguments)))
        try:
            result: EnvFuncCallResult = await self.function_env.eval(self, function_call)
            return result
        except Exception as e:
            if remaining_retry == 0:
                raise e
            prompt = f"""
Fix the following python function call args into a eval-able python expression:
```python
{function_call.dict()}
```
The function raised the following error:
```python
{e}
```
Make sure to start the answer with "```json" and end with "```".
Example:
```python
{{
    "name":"send_msg",
    "arguments":{{
        "message":"hello"
    }}
}}
```
"""
            """
            If I use 'ask' to fix the syntax, it actually can call the function and finish the chat.
            Because somehow gpt4 calls function_calling api with the python syntax...
            """
            chat = await self.ask(prompt)
            data = await chat.ask_to_load_python(chat.messages[-1].content)
            function_call = function_call.copy(
                update=dict(name=data['name'], arguments_json=json.dumps(data['arguments'])))
            return await chat.fix_function_call(function_call, remaining_retry=remaining_retry - 1)

    async def get_response(self):
        def debug_msgs():
            for msg in self.messages:
                if msg.content:
                    yield Panel(Markdown(msg.content), title=msg.role + ":message")
                if msg.function_call:
                    yield Panel(Syntax(msg.function_call.arguments_json,'json'), title=msg.role + f":function_call({msg.name})")

        rich.print(Panel(Group(*debug_msgs()), title="Messages", style='cyan'))
        return await self.chat_stream(OpenAICallArgs(messages=self.messages, functions=self.function_env.functions))

    @staticmethod
    async def _ask_turn(chat: "ChatWithFunctions", msg: str) -> "ChatWithFunctions":
        chat += Message(role="user", content=msg)
        await chat.stream_handler.handle_user_input(msg)
        resp: StreamResponse = await chat.get_response()
        return await ChatWithFunctions._handle_ai_response(chat, resp)

    async def ask(self, message) -> "ChatWithFunctions":
        return await ChatWithFunctions._ask_turn(self, message)

    async def call_function_without_fix(self, function_call):
        try:
            return await self.function_env.eval(self, function_call)
        except Exception as e:
            res = Future()
            res.set_result(f"""
The function raised the following error:
```error
{type(e)}
{e}
```
Please fix the function call and try again.
""")
            trace = traceback.format_exc()
            logger.error(f"function call failed with {e},{trace}")
            return EnvFuncCallResult(
                env=self.function_env,
                result=res
            )

    @staticmethod
    async def _handle_ai_response(chat, resp: StreamResponse):
        try:
            await chat.stream_handler.handle_stream(resp)
            _msg: ChatCompletion = await resp.parsed
        except Exception as e:
            await chat.stream_handler.handle_exception(resp)
            import traceback
            exc = traceback.format_exc()
            logger.error(f"Unexpected Exception Occured:{type(e)}->{e}\n{exc}")
            error_msg = Message(role="system", content=f"""
Unexpected exception happend: {type(e)}->{e}
""")
            raise e
            return chat + error_msg
        if len(_msg.choices) == 0:
            logger.warning(f"got empty choices from openai:{_msg}")
            return chat
        chat += _msg.choices[0].message
        function_call = _msg.choices[0].message.function_call

        if function_call is not None:
            # call_result = await chat.fix_function_call(function_call, remaining_retry=3)
            call_result = await chat.call_function_without_fix(function_call)
            _, result_str = await asyncio.gather(
                chat.stream_handler.handle_func_out(call_result),
                call_result.result
            )
            chat = replace(chat, function_env=call_result.env)
            chat += Message(role="function", content=result_str, name=function_call.name)
            summary: StreamResponse = await chat.get_response()
            chat = await ChatWithFunctions._handle_ai_response(chat, summary)
        else:
            logger.info(f"got no function call:{_msg.choices[0].message}")
        return chat

    def __add__(self, other):
        match other:
            case Message():
                return replace(
                    self,
                    messages=self.messages + [other]
                )
            case [*items] if all(isinstance(item, Message) for item in items):
                return replace(
                    self,
                    messages=self.messages + items
                )
            case _:
                raise ValueError(f"cannot add {other} to ChatWithFunctions")
