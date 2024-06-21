from typing import Coroutine

from cachetools import TTLCache
from limiter import Limiter
from .sender import Sender

class LimitCaller:
    __slots__ = ("main_limiter", "chats", "groups")

    def __init__(self) -> None:
        """A class that controls the speed of sending requests."""

        self.main_limiter = Limiter(30)
        self.groups = TTLCache[int, Sender](maxsize=9_223_372_036_854_775_807, ttl=60)
        self.chats = TTLCache[int, Sender](maxsize=9_223_372_036_854_775_807, ttl=60)

    async def _call_with_limit(
        self,
        chat_id: int,
        coro: Coroutine,
        storage: TTLCache[int, Sender],
        rate: int | float,
        burst: int,
    ):
        """Calls the api method

        Params:
            - chat_id: telegram chat id
            - coro: method
            - storage: chat or group storage
            - rate: call rate for limiters
            - burst: burst for limiters
        """

        async with self.main_limiter:
            sender = storage.get(chat_id)
            if not sender:
                limiter = Limiter(rate, burst)
                sender = Sender(limiter)
                storage[chat_id] = sender
            return await sender.send(coro)

    async def call(self, chat_id: int, coro: Coroutine):
        """Call the method"""

        if chat_id < 0:
            return await self._call_with_limit(chat_id, coro, self.groups, 0.33, 20)
        else:
            return await self._call_with_limit(chat_id, coro, self.chats, 1, 1)
