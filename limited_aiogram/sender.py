from dataclasses import dataclass
from typing import Any

import asyncio
from asyncio.queues import Queue
from asyncio import Event
from typing import Coroutine
from limiter import Limiter


@dataclass(slots=True)
class Result:
    value: Any | None = None
    exception: Exception | None = None


class Sender:
    __slots__ = ('limiter', 'que', '__task')

    def __init__(self, limiter: Limiter) -> None:
        self.limiter = limiter
        self.que = Queue()
        self.__task = asyncio.create_task(self.__sending_task())

    async def __send(self, coro: Coroutine, result: Result, event: Event) -> Result:
        try:
            res = await coro
            result.value = res
        except Exception as e:
            result.exception = e
        event.set()

    async def send(self, coro: Coroutine):
        res = Result()
        event = Event()
        await self.que.put(self.__send(coro, res, event))
        await event.wait()
        if res.exception:
            raise res.exception
        else:
            return res.value

    async def __sending_task(self):
        from time import time
        while True:
            coro = await self.que.get()
            t1 = time()
            with self.limiter:
                await coro
                print(time() - t1)

    def __del__(self):
        self.__task.cancel()
