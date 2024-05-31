import asyncio
import inspect
from asyncio import Task, Future
from dataclasses import dataclass
from typing import Callable, Awaitable

import cloudpickle
from openai.types.chat import ChatCompletionChunk
from openai.types.chat.chat_completion_chunk import ChoiceDelta, ChoiceDeltaFunctionCall
from pydantic import BaseModel
from returns.maybe import Some

from chat_with_functions.cached_streaming import CachedStream, IStream
from chat_with_functions.caches import AsyncCache, DictAsyncCacheHandle
from chat_with_functions.data_structures import OpenAICallArgs
from chat_with_functions.openai_api import Message, ChatCompletion
from chat_with_functions.openai_util import OpenAIChatUtil
from pinjected import Injected, injected, instance
from pinjected.decoration import update_if_registered
from pinjected.di.util import get_code_location, instances

from pinjected.di.metadata.bind_metadata import BindMetadata


@dataclass
class StreamResponse:
    src: IStream[ChatCompletionChunk]
    msgs: IStream[str]  # stream of tokens
    fcs: IStream[ChoiceDeltaFunctionCall]
    parsed: Future[ChatCompletion]

    def __post_init__(self):
        assert self.src is not None
        assert self.msgs is not None
        assert self.fcs is not None
        assert self.parsed is not None



def cached_stream(
        async_cache_provider: Injected,  # ["Key -> AsyncCache"]
        *additional_keys: Injected
):
    """
    use this to cache a function that returns IStream.
    :param async_cache_provider:
    :return:
    """
    parent_frame = inspect.currentframe().f_back

    def decorator_impl(additional_key, cache: "Key -> AsyncCache", func: "() -> Awaitable[IStream]"):
        async def impl(*args, **kwargs):
            key = (additional_key, args, kwargs)
            a_cache: AsyncCache = cache(key)

            async def factory():
                return await func(*args, **kwargs)

            return CachedStream(
                factory,
                a_cache,
            )

        return impl

    def decorator(func: Injected):
        res = Injected.bind(
            decorator_impl,
            cache=async_cache_provider,
            func=func,
            additional_key=Injected.mzip(*additional_keys)
        )
        return update_if_registered(func, res, Some(BindMetadata(code_location=Some(get_code_location(parent_frame)))))

    return decorator


def serialize_key(k) -> str:
    match k:
        case [*items]:
            return "".join([serialize_key(i) for i in items])
        case {**items}:
            return "".join([serialize_key(i) for i in items.items()])
        case BaseModel() as bm:
            return bm.json()
        case value:
            return str(value)


@injected
def dict_cache_provider(backend: dict):
    def impl(key):
        key = serialize_key(key)
        return DictAsyncCacheHandle(
            src=backend,
            key=key,
            serializer=cloudpickle.dumps,
            deserializer=cloudpickle.loads
        )

    # hmm,?

    return impl


@cached_stream(
    injected("cached_raw_stream_cache"),
    injected("chat_model_cache_key"),
)
@injected
async def a_cached_raw_stream(
        openai_client: OpenAIChatUtil, /,
        args: OpenAICallArgs):
    # cache needs to consider the model...
    return await openai_client.raw_stream(args.messages, args.functions, args.function_call)


@injected
async def a_raw_stream(
        openai_client: OpenAIChatUtil, /,
        args: OpenAICallArgs
):
    return await openai_client.raw_stream(args.messages, args.functions, args.function_call)


@injected
def raw_stream_to_chat_stream(
        stream_function: Callable[[OpenAICallArgs], Awaitable[IStream[ChatCompletionChunk]]]
) -> StreamResponse:
    async def impl(args):
        stream = await stream_function(args)
        # hmm, some times nothing is in the choices...

        msgs = stream.collect_successful(
            lambda chunk: chunk.choices[0].delta.content
        ).accept(
            lambda x: x is not None)
        fcs = stream.collect_successful(
            lambda chunk: chunk.choices[0].delta.function_call
        ).accept(
            lambda x: x is not None)
        parsed: Task = asyncio.create_task(OpenAIChatUtil.parse_raw_stream(stream))

        return StreamResponse(
            src=stream,
            msgs=msgs,
            fcs=fcs,
            parsed=parsed
        )

    return impl


@instance
def a_cached_chat_stream(
        a_cached_raw_stream,
        raw_stream_to_chat_stream,
):
    return raw_stream_to_chat_stream(a_cached_raw_stream)


@injected
async def test_raw_stream(
        a_cached_chat_stream: "args - > StreamResponse",
        /,
):
    stream: StreamResponse = await a_cached_chat_stream(
        OpenAICallArgs(messages=[Message(role="user", content="hello")]))
    async for item in stream.src.stream():
        print(item)
    async for item in stream.msgs.stream():
        print(item)


