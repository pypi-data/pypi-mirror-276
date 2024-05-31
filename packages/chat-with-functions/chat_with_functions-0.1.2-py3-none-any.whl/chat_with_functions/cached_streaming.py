import abc
import asyncio
import traceback
from abc import ABC
from asyncio import Future, Queue, Task, Lock
from dataclasses import dataclass, field
from typing import TypeVar, Generic, AsyncIterable, Callable, Awaitable, Tuple, AsyncGenerator

from returns.interfaces.unwrappable import Unwrappable
from returns.pipeline import is_successful
from returns.result import safe

from chat_with_functions.caches import AsyncCache

T = TypeVar('T')


class IStream(Generic[T], ABC):
    @abc.abstractmethod
    def stream(self) -> AsyncIterable[T]:
        pass

    @abc.abstractmethod
    async def result(self) -> list[T]:
        pass

    def amap(self, afun):
        return MappedStream(self, afun)

    def map(self, fun):
        async def mapper(item):
            return fun(item)

        return MappedStream(self, mapper)

    def accept(self, fun):
        async def accepter(item):
            return fun(item)

        return AcceptedStream.create(self, accepter)

    def collect_successful(self, fun: Callable[[T], Unwrappable]) -> "IStream":
        safe_fun = safe(fun)
        return self.map(safe_fun).accept(is_successful).map(lambda x: x.unwrap())


@dataclass
class SItem:
    item: T
    exception: Exception = field(default=None)
    finish: bool = field(default=False)


@dataclass
class AsyncStream(IStream[T]):
    queue: asyncio.Queue = field(default_factory=asyncio.Queue)
    future: Future = field(default_factory=asyncio.Future)
    published: list[T] = field(default_factory=list)
    listeners: list[asyncio.Queue] = field(default_factory=list)

    async def stream(self):
        queue = Queue()
        self.listeners.append(queue)
        for item in self.published:
            if item.finish:
                break
            if item.exception is not None:
                raise item.exception
            yield item.item
        if self.future.done():
            return
        while True:
            item = await queue.get()
            if item.finish:
                break
            if item.exception is not None:
                raise item.exception
                # raise RuntimeError(f"exception in stream:{item.exception}") from item.exception
                # raise item.exception
            yield item.item

    async def put(self, item):
        await self.queue.put(SItem(item=item))

    async def finish(self):
        await self.queue.put(SItem(None, finish=True))

    async def raise_exception(self, exc):
        await self.queue.put(SItem(None, exception=exc))

    async def _gather_task(self):
        buf = []
        while True:
            item = await self.queue.get()
            for listener in self.listeners:
                await listener.put(item)
            self.published.append(item)
            if item.finish:
                break
            if item.exception is not None:
                logger.warning(f"exception traceback:{traceback.format_tb(item.exception.__traceback__)}")
                # however, at this position, we have the traceback...
                logger.info(f"setting exception to future:{id(self.future)}")
                self.future.set_exception(item.exception)
                return
            buf.append(item.item)

        self.future.set_result(buf)

    def result(self) -> Future[list[T]]:
        return self.future

    @staticmethod
    def create():
        stream = AsyncStream()
        asyncio.create_task(stream._gather_task())
        return stream


@dataclass
class AcceptedStream(IStream[T]):
    src: IStream[T]
    a_accept: Callable[[T], Awaitable[bool]]
    accepted: AsyncStream = field(default=None)
    task: Task = field(default=None)

    @classmethod
    def create(cls, src, a_accept):
        self = cls(src, a_accept)
        self.accepted = AsyncStream.create()

        async def accepter():
            try:
                async for item in self.src.stream():
                    if await self.a_accept(item):
                        await self.accepted.put(item)
                await self.accepted.finish()
            except Exception as e:
                await self.accepted.raise_exception(e)

        self.task = asyncio.create_task(accepter())
        return self

    async def stream(self):
        async for item in self.accepted.stream():
            yield item
        await self.task

    async def result(self) -> list[T]:
        res = await self.accepted.result()
        await self.task
        return res


@dataclass
class MappedStream(IStream[T]):
    src: IStream[T]
    afun: Callable[[T], Awaitable[T]]
    mapped: AsyncStream = field(default=None)
    lock: Lock = field(default_factory=asyncio.Lock)

    async def ensure_mapped(self) -> IStream:
        if self.mapped is None:
            self.mapped = AsyncStream.create()

            async def mapper():
                try:
                    async for item in self.src.stream():
                        await self.mapped.put(await self.afun(item))
                    await self.mapped.finish()
                except Exception as e:
                    await self.mapped.raise_exception(e)

            asyncio.create_task(mapper())
        return self.mapped

    async def stream(self):

        async for item in (await self.ensure_mapped()).stream():
            yield item

    async def result(self) -> list[T]:
        mapped = await self.ensure_mapped()
        return await mapped.result()


@dataclass
class CachedStream(IStream):
    impl: Callable[[], Awaitable[IStream]]  # this src, must be lazy
    cache: AsyncCache
    backend: IStream = field(default=None)
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)
    subtask: Task = field(default=None)

    async def load_or_create(self) -> Tuple[IStream, Task]:
        if self.backend is None:
            if await self.cache.exists():
                self.backend: AsyncStream = AsyncStream.create()

                async def cache_load_task():
                    try:
                        data = await self.cache.get()
                        from loguru import logger
                        logger.debug(f"loaded {len(data)} items")
                        for item in data:
                            await self.backend.put(item)
                        await self.backend.finish()
                    except Exception as e:
                        await self.backend.raise_exception(e)

                self.subtask = asyncio.create_task(cache_load_task())
            else:
                # for some reason, the location of exception in this task, is not shown.
                self.backend: IStream = await self.impl()

                async def store_data():
                    # upon calling this task,
                    # the traceback of backend is lost for some reason!
                    f: Future = self.backend.result()
                    data = await f

                    await self.cache.set(data)

                # task is not guaranteed to be finished...
                self.subtask = asyncio.create_task(store_data())
        return self.backend, self.subtask

    async def stream(self):
        stream, task = await self.load_or_create()
        async for item in stream.stream():
            yield item
        await task

    async def result(self) -> list[T]:
        stream, task = await self.load_or_create()
        res = await stream.result()
        await task
        return res


@dataclass
class StreamedStr:
    future: Awaitable[str]
    stream: AsyncGenerator[str, None]

    @staticmethod
    async def create():
        queue = asyncio.Queue()
        gen_buf = asyncio.Queue()

        async def gather():
            buf = ""
            while True:
                msg = await queue.get()
                await gen_buf.put(msg)
                if msg is None:
                    break
                buf += msg
            return buf

        future = asyncio.create_task(gather())

        async def generator():
            while True:
                item = await gen_buf.get()
                if item is None:
                    break
                yield item

        return StreamStrConstructor(
            future=future,
            stream=generator(),
            queue=queue
        )


@dataclass
class StreamStrConstructor(StreamedStr):
    loop: asyncio.AbstractEventLoop = field(default_factory=asyncio.get_event_loop)
    queue: asyncio.Queue = field(default_factory=asyncio.Queue)

    def put(self, item):
        # self.loop.call_soon_threadsafe(self.queue.put_nowait,item)
        asyncio.run_coroutine_threadsafe(self.queue.put(item), self.loop)
        # asyncio.run_coroutine_threadsafe(print(item), self.loop)

    def finish(self):
        self.loop.call_soon_threadsafe(self.queue.put_nowait, None)

        # asyncio.run_coroutine_threadsafe(self.queue.put(None), self.loop)


