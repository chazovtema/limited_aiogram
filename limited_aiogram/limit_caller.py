from time import time
from typing import Coroutine
from asyncio import Task
import asyncio

from aiogram.types import Chat

from limiter import Limiter

GROUPS = ['group', 'supergroup', 'channel']

class LimitCaller:
    
    __slots__ = ('main_limiter', 'chats', 'groups')
    
    def __init__(self) -> None:
        
        """A class that controls the speed of sending requests."""
        
        self.main_limiter = Limiter(30)
        self.chats: dict[int, tuple[Limiter | float | Task]] = {}
        self.groups: dict[int, tuple[Limiter | float | Task]] = {}
        
    async def _delete_task(self, chat: int, 
                          storage: dict[int, tuple[Limiter | float | Task]]):
        
        """Task to clear the chat or group storage"""
        
        await asyncio.sleep(60)
        del storage[chat]
        
    async def _call_with_limit(self, chat_id: int, coro: Coroutine, 
                            storage:  dict[int, tuple[Limiter | float | Task]],
                            rate: int | float, burst: int):
        
        """Calls the api method
        
        Params:
            - chat_id: telegram chat id
            - coro: method
            - storage: chat or group storage
            - rate: call rate for limiters
            - burst: burst for limiters
        """
        
        async with self.main_limiter:
            limiter_list = self.chats.get(chat_id)
            if not limiter_list:
                limiter = Limiter(rate, burst)
                task = asyncio.create_task(self._delete_task(chat_id, storage))
                storage[chat_id] = [limiter, time(), task]
                async with limiter:
                    return await coro
            else:
                limiter_list[2].cancel()
                limiter_list[1] = time()
                limiter_list[2] = asyncio.create_task(self._delete_task(chat_id, storage))
                async with limiter_list[0]:
                    return await coro
    
    async def call(self, chat: Chat, coro: Coroutine):
        
        """Call the method"""
        
        chat_id = chat.id
        chat_type = chat.type
        if chat_type in GROUPS:
            return await self._call_with_limit(chat_id, coro, self.groups, 0.3333, 20)
        else:
            return await self._call_with_limit(chat_id, coro, self.groups, 1, 3)