from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import TypeVar, Generic, Callable

import aiofiles
import cloudpickle

from loguru import logger
from returns.maybe import Maybe, Nothing, Some

T = TypeVar('T')


class AsyncCache(Generic[T], ABC):
    @abstractmethod
    async def exists(self):
        pass

    @abstractmethod
    async def set(self, value):
        pass

    @abstractmethod
    async def get(self):
        pass


@dataclass
class DictAsyncCacheHandle(AsyncCache):
    src: dict
    key: str
    serializer: Callable[[T], bytes]
    deserializer: Callable[[bytes], T]

    async def exists(self):
        #src_keys= list(self.src.keys())
        #logger.debug(f"checking existence of {self.key} in {self.src}")
        res = self.key in self.src
        #logger.debug(f"checked existence of {self.key} in {self.src} with {res}")
        return res

    async def set(self, value):
        self.src[self.key] = self.serializer(value)
        logger.debug(f"written data to {self.key[:10]}")

    async def get(self):
        res = self.deserializer(self.src[self.key])
        logger.debug(f"loaded data from {self.key[:10]}")
        return res


@dataclass
class AsyncPickled(AsyncCache[T]):
    path: Path
    value: Maybe[T] = field(default=Nothing)

    async def exists(self) -> bool:
        return self.path.exists()

    async def set(self, value: T) -> None:
        self.value = Some(value)
        data = cloudpickle.dumps(value)
        async with aiofiles.open(self.path, 'wb') as f:
            await f.write(data)

    async def get(self) -> T:
        if self.value is not Nothing:
            return self.value.unwrap()
        async with aiofiles.open(self.path, 'rb') as f:
            data = await f.read()
        self.value = Some(cloudpickle.loads(data))
        return self.value.unwrap()
