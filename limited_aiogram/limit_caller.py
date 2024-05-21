from typing import Coroutine

from cachetools import TTLCache
from limiter import Limiter


class LimitCaller:
    __slots__ = ("main_limiter", "chats", "groups")

    def __init__(self) -> None:
        """A class that controls the speed of sending requests."""

        self.main_limiter = Limiter(30)
        self.groups = TTLCache[Limiter](maxsize=9_223_372_036_854_775_807, ttl=60)
        self.chats = TTLCache[Limiter](maxsize=9_223_372_036_854_775_807, ttl=60)

    async def _call_with_limit(
        self,
        chat_id: int,
        coro: Coroutine,
        storage: TTLCache[Limiter],
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
            limiter = storage.get(chat_id)
            if not limiter:
                limiter = Limiter(rate, burst)
                storage[chat_id] = limiter
                async with limiter:
                    return await coro
            else:
                async with limiter:
                    return await coro

    async def call(self, chat_id: int, coro: Coroutine):
        """Call the method"""

        if chat_id < 0:
            return await self._call_with_limit(chat_id, coro, self.groups, 0.32, 20)
        else:
            return await self._call_with_limit(chat_id, coro, self.chats, 0.99, 1)
