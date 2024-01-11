from datetime import datetime
from typing import Coroutine

from limiter import Limiter


class LimitCaller():
    
    def __init__(self) -> None:
        self.main_limiter = Limiter(30)
        self.chats: dict[int, Limiter] = {}

    
    async def call(self, chat: int, coro: Coroutine):
        
        async with self.main_limiter:
            limiter = self.chats.get(chat)
            if not limiter:
                limiter = Limiter(3, 10)
                self.chats[chat] = limiter
                
            async with limiter:
                
                return await coro