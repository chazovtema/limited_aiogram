from typing import Optional, TypeVar
from aiogram.client.session.base import BaseSession

from aiogram.methods import TelegramMethod, GetChat
from aiogram import Bot

from .limit_caller import LimitCaller

T = TypeVar("T")

class LimitedBot(Bot):
    
    async def __call__(self, method: TelegramMethod[T], request_timeout: Optional[int] = None):
        
        coro = self.session(self, method, timeout=request_timeout)
        if hasattr(method, 'chat_id') and not isinstance(method, GetChat):
            caller = self.__dict__.get('caller')
            if not caller:
                caller = LimitCaller()
                self.caller = caller
            chat = await self.get_chat(method.chat_id)
            return await caller.call(chat, coro)
        else:
            return await coro

def path_bot():
    
    """Patches the bot, these changes are not reversible"""
    
    Bot.__call__ = LimitedBot.__call__