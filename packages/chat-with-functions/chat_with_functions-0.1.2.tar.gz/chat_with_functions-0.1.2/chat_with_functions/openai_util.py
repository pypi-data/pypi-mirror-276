import asyncio
import inspect
import time
from asyncio import Future
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import timedelta
from pathlib import Path
from threading import Lock
from typing import List, Optional, Union, Generator

import openai
import tiktoken
from loguru import logger
from openai import OpenAI, Stream
from openai.types.chat import ChatCompletionChunk

from chat_with_functions.cached_streaming import AsyncStream, IStream, StreamedStr
from chat_with_functions.openai_api import Message, FunctionSpec, ChatCompletion, ResponseAccumulator
from pinjected import injected


@dataclass
class OpenAIConfig:
    api_key: str
    api_type: str = field(default="open_ai")
    api_base: str = field(default="https://api.openai.com/v1")
    api_version: str = field(default=None)

    def apply_global(self):
        import openai
        logger.warning(f"globally setting openai config to {self}")
        openai.api_key = self.api_key
        openai.api_base = self.api_base
        openai.api_version = self.api_version
        openai.api_type = self.api_type
        logger.warning(f"globally setting openai config done.")

    def assert_global_config(self):
        """Use this to check if the setting is applied"""
        assert openai.api_key == self.api_key
        assert openai.api_base == self.api_base
        assert openai.api_version == self.api_version
        assert openai.api_type == self.api_type

    def __repr__(self):
        return f"OpenAIConfig(api_key={self.api_key[:10]}***, api_type={self.api_type}, api_base={self.api_base}, api_version={self.api_version})"


@dataclass
class ChatCompletionModel:
    """
    a config class to manage complicated openai api parameters.
    """
    cfg: OpenAIConfig
    name: str
    temperature: float = field(default=0.9)

    def create_param_diff(self) -> dict:
        """
        creates params for openai.ChatCompletion.create, which are different for api_type and endpoint
        :return:
        """
        if self.cfg.api_type != "open_ai":
            raise NotImplementedError(f"api_type:{self.cfg.api_type} is not supported")
            # return dict(engine=self.name)
        else:
            return dict(model=self.name)

    def msgs_to_args(self, msgs: list[Message]):
        args = []
        for msg in msgs:
            arg = dict(
                role=msg.role,
                content=msg.content,
            )
            if msg.name is not None:
                arg['name'] = msg.name
            args.append(arg)
        return args

    def to_params(self,
                  messages: list[Message],
                  stream: bool = False,
                  functions: Optional[list[FunctionSpec]] = None,
                  function_call=None):
        """
        creates params for openai.ChatCompletion.create
        :return:
        """
        param = dict(
            messages=self.msgs_to_args(messages),
            model=self.name,
            stream=stream
        )
        param.update(self.create_param_diff())
        param['temperature'] = self.temperature
        if functions is not None and functions:
            param['functions'] = [f.dict() for f in functions]
        if function_call is not None and functions:
            param['function_call'] = function_call
        return param

    def call(self,
             messages: list[Message],
             stream: bool = False,
             functions: Optional[list[FunctionSpec]] = None,
             function_call=None
             ):
        """
        creates params for openai.ChatCompletion.create
        :return:
        """
        self.cfg.assert_global_config()
        param = self.to_params(
            messages,
            stream,
            functions,
            function_call
        )
        client = OpenAI()
        resp = client.chat.completions.create(**param)
        #resp = openai.ChatCompletion.create(**param)
        return resp

    async def acall(self, messages: list[Message], stream: bool = False, functions=None, function_call=None):
        """
        creates params for openai.ChatCompletion.create
        :return:
        """
        self.cfg.assert_global_config()
        param = self.to_params(messages, stream, functions, function_call)
        logger.debug(f"calling openai.ChatCompletion.acreate with {param}")
        resp = await openai.ChatCompletion.acreate(**param)
        return resp


@injected
def load_openai_config_from_path(path: Path) -> OpenAIConfig:
    import toml
    with path.expanduser().open() as f:
        logger.info(f"loading openai config from {f}")
        data = toml.load(f)
    conf = OpenAIConfig(
        **data
    )
    return conf


@dataclass
class Throttle:
    max_tokens: int
    duration: timedelta
    log = []
    time_log = []
    lock = Lock()

    def call(self, tokens):
        with self.lock:
            # remove old logs if time passed
            assert len(self.log) == len(
                self.time_log), f"len(self.log):{len(self.log)}, len(self.time_log):{len(self.time_log)}"
            while self.time_log and self.time_log[0] < time.time() - self.duration.total_seconds():
                self.time_log.pop(0)
                self.log.pop(0)
            consumed = sum(self.log)
            new_log = self.log + [tokens]
            estimated = sum(new_log)
            logger.info(f"consumed:{consumed}, estimated:{estimated}, max:{self.max_tokens} in {self.duration}")
            assert len(self.log) == len(
                self.time_log), f"len(self.log):{len(self.log)}, len(self.time_log):{len(self.time_log)}"
            if sum(new_log) > self.max_tokens:
                return False
            else:
                self.log.append(tokens)
                self.time_log.append(time.time())
                logger.info(f"Now consumed {sum(self.log)}")
                return True

    def wait(self, tokens):
        while not self.call(tokens):
            time.sleep(1)

    def consume(self, tokens):
        with self.lock:
            self.time_log.append(time.time())
            self.log.append(tokens)


@dataclass
class MessageThrottle:
    model_name: str
    throttle: Throttle

    def wait(self, messages: List[Message]):
        if self.model_name == 'gpt-35-turbo':
            encoding = tiktoken.encoding_for_model(model_name='gpt-3.5-turbo')
        else:
            encoding = tiktoken.encoding_for_model(model_name=self.model_name)
        token = sum([len(encoding.encode(msg.content or "")) for msg in messages])

        self.throttle.wait(token)


GLOBAL_THROTTLE = defaultdict(lambda: MessageThrottle(
    model_name="gpt-4",  # you cannot set undeifined here, as it uses the model_name for token counting
    throttle=Throttle(max_tokens=40000, duration=timedelta(minutes=1))
))
GLOBAL_THROTTLE_GPT4 = MessageThrottle(
    model_name="gpt-4",
    throttle=Throttle(max_tokens=40000, duration=timedelta(minutes=1))
)
GLOBAL_THROTTLE_GPT35_TURBO = MessageThrottle(
    model_name="gpt-3.5-turbo",
    throttle=Throttle(max_tokens=40000, duration=timedelta(minutes=1))
)
GLOBAL_THROTTLE_GPT4_TURBO = MessageThrottle(
    model_name = 'gpt-4-1106-preview',
    throttle=Throttle(max_tokens=120000, duration=timedelta(minutes=1))
)
GLOBAL_THROTTLE['gpt-4'] = GLOBAL_THROTTLE_GPT4
GLOBAL_THROTTLE['gpt-3.5-turbo'] = GLOBAL_THROTTLE_GPT35_TURBO


@dataclass
class AsyncChatResponse:
    message_tokens: StreamedStr
    function_calling_tokens: StreamedStr
    response: Future[ChatCompletion]

    def __post_init__(self):
        assert isinstance(self.message_tokens, StreamedStr)
        assert isinstance(self.function_calling_tokens, StreamedStr)
        assert inspect.isawaitable(self.response), f"expected awaitable but got {self.response}"


@dataclass
class OpenAIChatUtil:
    model_name: str = field(default=None)
    model_config: ChatCompletionModel = field(default=None)
    throttle: MessageThrottle = field(default=None)
    pool: ThreadPoolExecutor = field(default_factory=ThreadPoolExecutor)

    # we need to throttle the call with ratelimit and time.
    def __post_init__(self):
        match (self.model_name, self.model_config):
            case (str() as name, None):
                assert openai.api_key is not None, f"openai.api_key is None"
                self.model_config = ChatCompletionModel(
                    cfg=OpenAIConfig(openai.api_key),
                    name=name
                )
            case (None, ChatCompletionModel()):
                pass
            case (None, None):
                raise RuntimeError("model_name and model_config cannot be both None")

        if self.throttle is None:
            self.throttle = GLOBAL_THROTTLE[self.model_config.name]
        if self.model_config is None:
            self.model_config = ChatCompletionModel(
                cfg=OpenAIConfig(openai.api_key),
                name=self.model_name
            )

    def msgs_to_args(self, msgs: List[Message]):
        args = []
        for msg in msgs:
            arg = dict(
                role=msg.role,
                content=msg.content,
            )
            if msg.name is not None:
                arg['name'] = msg.name
            args.append(arg)
        return args

    def call(self,
             messages: List[Message],
             functions: Optional[List[FunctionSpec]] = None,
             function_call: str = None,
             stream: bool = False
             ) -> Union[ChatCompletion, Generator]:
        """
        :param messages:
        :param functions:
        :param function_call: 'auto'
        :param stream:
        :return:
        """
        self.throttle.wait(messages)
        try:
            resp = self.model_config.call(
                messages=messages,
                stream=stream,
                functions=functions,
                function_call=function_call
            )
            if stream:
                return resp
            else:
                return ChatCompletion.from_dict(resp.to_dict())
        except Exception as e:
            if 'overloaded' in str(e):
                logger.warning(f"Overloaded, trying again")
                return self.call(messages, functions=functions, function_call=function_call, stream=stream)
            else:
                raise e

    async def raw_stream(self,
                         messages: List[Message],
                         functions: Optional[List[FunctionSpec]] = None,
                         function_call: str = "auto",
                         ) -> AsyncStream[ChatCompletionChunk]:
        stream: AsyncStream = AsyncStream.create()
        loop = asyncio.get_event_loop()
        def task():
            try:
                resp:Stream[ChatCompletionChunk] = self.call(messages, functions=functions, function_call=function_call, stream=True)
                for chunk in resp:
                    #logger.info(f"putting chunk:{chunk}")
                    asyncio.run_coroutine_threadsafe(stream.put(chunk), loop)
                asyncio.run_coroutine_threadsafe(stream.finish(), loop)
            except Exception as e:
                import traceback
                logger.error(f"error in raw_stream:{e},{traceback.format_exc()}")
                logger.warning(f"traceback of exception:{e.__traceback__}")
                asyncio.run_coroutine_threadsafe(stream.raise_exception(e), loop)
                raise e

        self.pool.submit(task)
        return stream

    @staticmethod
    async def parse_raw_stream(src: IStream[ChatCompletionChunk]):
        acc = ResponseAccumulator()
        for chunk in await src.result():
            acc.add(chunk)
        return acc.to_chat_completion()

    async def stream(self,
                     messages: List[Message],
                     functions: Optional[List[FunctionSpec]] = None,
                     function_call: str = "auto"
                     ) -> AsyncChatResponse:

        msg_stream = await StreamedStr.create()
        fc_stream = await StreamedStr.create()
        loop = asyncio.get_event_loop()

        def task():
            acc = ResponseAccumulator()
            resp = self.call(messages, functions=functions, function_call=function_call, stream=True)
            assert resp is not None, f"resp is None"
            fc_msgs = []
            for chunk in resp:
                acc.add(chunk)
                msg = chunk['choices'][0]["delta"].get('content', None)
                if msg is not None:
                    msg_stream.put(msg)
                fc = chunk['choices'][0]["delta"].get('function_call', None)
                if fc is not None and fc.get("arguments", None) is not None:
                    fc_stream.put(fc["arguments"])
                    fc_msgs.append(fc["arguments"])
            msg_stream.finish()
            fc_stream.finish()
            logger.info(f"fc_msgs:{fc_msgs}")
            comp = acc.to_chat_completion()
            logger.info(f"res:{comp}")
            return comp

        resp = self.pool.submit(task)
        resp = asyncio.wrap_future(resp)

        return AsyncChatResponse(
            message_tokens=msg_stream,
            function_calling_tokens=fc_stream,
            response=resp
        )

    async def acall(self, messages: List[Message]):
        resp = await openai.ChatCompletion.create(
            model=self.model_name,
            messages=self.msgs_to_args(messages)
        )
        return ChatCompletion.from_dict(resp.to_dict())
