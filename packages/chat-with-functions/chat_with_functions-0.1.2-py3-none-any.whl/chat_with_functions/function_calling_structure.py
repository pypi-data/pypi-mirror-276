import abc
import asyncio
from abc import ABC, ABCMeta, abstractmethod
from asyncio import Future
from copy import copy
from dataclasses import dataclass, field, replace
from typing import List, Callable, Awaitable, Union

from langchain import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.vectorstores.base import VectorStoreRetriever

from loguru import logger
from rich.console import Group,Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.pretty import Pretty
from rich.syntax import Syntax

from chat_with_functions.openai_api import FunctionSpec, FunctionCall
from chat_with_functions.streaming import StreamResponse


@dataclass
class EnvFuncCall:
    chat: "ChatWithFunctions"
    env: "IFunctionEnv"
    name: str
    arguments: dict


@dataclass
class EnvFuncCallResult:
    env: "IFunctionEnv"
    result: Future[str]


@dataclass
class IFunctionEnv(ABC):
    @property
    @abc.abstractmethod
    def functions(self) -> List[FunctionSpec]:
        pass

    @abc.abstractmethod
    async def eval(self, chat: "ChatWithFunctions", function_call: FunctionCall) -> EnvFuncCallResult:
        pass

    @abc.abstractmethod
    def register(self, function: "AIFunction"):
        pass

    """
    I need to be able to make this env store arbitrary python data.
    1. set/get/keys
    2. dict-like interface
    """

    @abc.abstractmethod
    def set(self, key, value) -> "IFunctionEnv":
        pass

    @abc.abstractmethod
    def get(self, key):
        pass

    @abc.abstractmethod
    def __contains__(self, item):
        pass

    @abc.abstractmethod
    def keys(self) -> list[object]:
        pass

    def __add__(self, other):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_function(self, name):
        pass

    @abc.abstractmethod
    def empty(self) -> "IFunctionEnv":
        pass


@dataclass
class AIFunction:
    spec: FunctionSpec
    """
    an ai function shold not only alter AIFunction itself, but also the function env.
    This means we need to pass the function env to the function.
    And ask the function to return the new function env. (if needed)
    This works as a state monad.
    """
    impl: Callable[[EnvFuncCall], Awaitable[EnvFuncCallResult]]


@dataclass
class FunctionEnv(IFunctionEnv):
    ai_functions: List[AIFunction]
    key_value_store: dict = field(default_factory=dict)

    @property
    def functions(self) -> List[FunctionSpec]:
        return [f.spec for f in self.ai_functions]

    @property
    def func_table(self) -> dict[str, AIFunction]:
        return {f.spec.name: f for f in self.ai_functions}

    def empty(self) -> "IFunctionEnv":
        return FunctionEnv(ai_functions=[])

    async def eval(self, chat: "ChatWithFunctions", function_call: FunctionCall) -> EnvFuncCallResult:
        if function_call.name not in self.func_table:
            fut = Future()
            fut.set_result(f"{function_call.name} is not available. choose from {list(self.func_table.keys())}")
            res = EnvFuncCallResult(self, fut)
            return res
        func: AIFunction = self.func_table[function_call.name]
        assert func.spec.name == function_call.name, f"function name mismatch: {func.spec.name} != {function_call.name}"
        env_call = EnvFuncCall(chat, self, function_call.name, function_call.arguments)
        result = await func.impl(env_call)
        console = Console(stderr=True)
        console.print(Panel(Pretty(result.result), title="Function Result", style="magenta"))
        # logger.info(f"evaluated function {func.spec.name} with result {result}")
        return result

    def register(self, function: "AIFunction"):
        table = self.func_table
        if function.spec.name in table:
            logger.debug(f"replaced existing function {function.spec.name}")
        table[function.spec.name] = function
        functions = list(sorted(list(table.values()), key=lambda f: f.spec.name))
        return replace(self, ai_functions=functions)

    def set(self, key, value) -> "IFunctionEnv":
        copied = copy(self.key_value_store)
        copied[key] = value
        return replace(self, key_value_store=copied)

    def get(self, key):
        return self.key_value_store[key]

    def __contains__(self, item):
        return item in self.key_value_store

    def keys(self) -> list[object]:
        return list(self.key_value_store.keys())

    def get_function(self, name):
        return self.func_table[name]

    def __add__(self, other: Union[AIFunction, list[AIFunction]]):
        match other:
            case AIFunction():
                return self.register(other)
            case [*items] if all(isinstance(item, AIFunction) for item in items):
                res = self
                for item in items:
                    res += item
                return res
            case _:
                raise ValueError(f"cannot add {other} to FunctionEnv")


@dataclass
class IStreamHandler(ABC):
    """
    a handler to work with chat streams and function streams
    """

    @abc.abstractmethod
    async def handle_stream(self, resp: StreamResponse):
        pass

    @abc.abstractmethod
    async def handle_func_out(self, func_out: EnvFuncCallResult):
        pass

    @abc.abstractmethod
    async def handle_user_input(self, msg: str):
        pass

    @abc.abstractmethod
    async def handle_exception(self, e: Exception):
        pass


@dataclass
class PrintStreamHandler(IStreamHandler):
    async def handle_user_input(self, msg: str):
        logger.info(msg)

    async def handle_exception(self, e: Exception):
        logger.error(e)

    async def handle_stream(self, resp: StreamResponse):
        async for msg in resp.msgs.stream():
            logger.info(msg)

    async def handle_func_out(self, func_out: EnvFuncCallResult):
        logger.info(await func_out.result)


@dataclass
class RichStreamHandler(IStreamHandler):
    console: Console

    async def handle_stream(self, resp: StreamResponse):
        text = ""
        func_name = ""
        func_args = ""
        with Live(console=self.console) as live:
            def update_live():
                panels = []
                if func_name or func_args:
                    panels.append(Panel(Syntax(func_args, "json", word_wrap=True), title=f"Call {func_name}"))
                if text:
                    panels.append(Panel(Markdown(text), title="AI"))
                live.update(Group(
                    *panels
                ))
                live.refresh()

            async def update_fc():
                nonlocal func_name, func_args
                async for msg in resp.fcs.stream():
                    #print(f"updating fc.{msg}")
                    if msg.name is not None:
                        func_name += msg.name
                    if msg.arguments is not None:
                        func_args += msg.arguments
                    update_live()

            async def update_chat():
                nonlocal text
                async for msg in resp.msgs.stream():
                    text += msg
                    #print(f"updating chat.{msg}")
                    update_live()

            await asyncio.gather(update_fc(), update_chat())

    async def handle_func_out(self, func_out: EnvFuncCallResult):
        text = await func_out.result
        self.console.print(Panel(Markdown(text), title="Function Output", style="yellow"))

    async def handle_user_input(self, msg: str):
        self.console.print(Panel(msg, title="User Input", style="bold blue"))

    async def handle_exception(self, e: Exception):
        # print_exception
        self.console.print_exception(show_locals=False)


class IFuncRegistry(metaclass=ABCMeta):

    @property
    @abstractmethod
    def functions(self) -> list[AIFunction]:
        pass

    @abstractmethod
    def search(self, query) -> list[AIFunction]:
        pass

    @abstractmethod
    def add_function(self, func: AIFunction):
        pass

    @abstractmethod
    def remove_function(self, name: str):
        pass

    @abstractmethod
    def __add__(self, other: Union[AIFunction, list[AIFunction], "IFuncRegistry"]) -> "IFuncRegistry":
        pass


@dataclass
class InMemoryRegistry(IFuncRegistry):
    """
    I need a registry backed by file system or database for
    persistence.
    """

    _functions: List[AIFunction]
    vector_store: FAISS = field(default=None)
    retriever: VectorStoreRetriever = field(default=None)

    def __post_init__(self):
        if self.functions:
            docs = [
                Document(page_content=f.spec.description, metadata=dict(func=f)) for f in self.functions
            ]
            self.vector_store = FAISS.from_documents(docs, OpenAIEmbeddings())
            self.retriever = self.vector_store.as_retriever()

    def __getstate__(self):
        return dict(
            _functions=self._functions,
            vector_store=self.vector_store,
            retriever=self.retriever
        )

    def __setstate__(self, state):
        self._functions = state['_functions']
        self.vector_store = state['vector_store']
        self.retriever = state['retriever']

    @property
    def functions(self):
        return self._functions

    def search(self, query: str) -> list[AIFunction]:
        if not self.functions:
            return []
        docs = self.retriever.get_relevant_documents(query)
        return [d.metadata['func'] for d in docs]

    def add_function(self, func: AIFunction):
        other_funcs = [f for f in self.functions if f.spec.name != func.spec.name]
        funcs = other_funcs + [func]
        vec_store = FAISS.from_documents(
            [Document(page_content=func.spec.description, metadata=dict(func=func))],
            OpenAIEmbeddings()
        )
        # vec_store = copy(self.vector_store)
        # vec_store.add_documents([Document(page_content=func.spec.description, metadata=dict(func=func))])
        return replace(self, _functions=funcs, vector_store=vec_store, retriever=vec_store.as_retriever())

    def remove_function(self, name: str):
        funcs = [f for f in self.functions if f.spec.name != name]
        return InMemoryRegistry(funcs)

    def __add__(self, other: Union[AIFunction, list[AIFunction], "InMemoryRegistry"]):
        if not self.functions:
            match other:
                case AIFunction():
                    return InMemoryRegistry([other])
                case [*items] if all(isinstance(item, AIFunction) for item in items):
                    return InMemoryRegistry(items)
                case InMemoryRegistry():
                    return other
        match other:
            case AIFunction():
                return self.add_function(other)
            case [*items] if all(isinstance(item, AIFunction) for item in items):
                res = self
                for item in items:
                    res += item
                return res
            case InMemoryRegistry():
                return self + other.functions
