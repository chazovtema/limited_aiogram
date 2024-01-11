from time import time
from typing import Coroutine
from asyncio import Task
import asyncio

from limiter import Limiter

class LimitCaller():
    
    def __init__(self) -> None:
        self.main_limiter = Limiter(30)
        self.chats: dict[int, tuple[Limiter | float | Task]] = {}
        
    async def delete_task(self, chat: int):
        
        await asyncio.sleep(60)
        del self.chats[chat]
        
    
    async def call(self, chat: int, coro: Coroutine):
        
        async with self.main_limiter:
            limiter_list = self.chats.get(chat)
            
            if not limiter_list:
                limiter = Limiter(3, 10)
                task = asyncio.create_task(self.delete_task(chat))
                self.chats[chat] = (limiter, time(), task)
            else:
                task.cancel()
                limiter_list[1] = time()
                limiter_list[2] = asyncio.create_task(self.delete_task(chat))
                async with limiter:
                    
                    return await coro