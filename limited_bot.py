from typing import Optional, TypeVar
from aiogram.client.session.base import BaseSession
from copy import copy
from functools import wraps

from aiogram.methods import TelegramMethod
from aiogram import Bot

from limit_caller import LimitCaller

T = TypeVar("T")

class LimitedBot(Bot):
    
    async def __call__(self, method: TelegramMethod[T], request_timeout: Optional[int] = None):
        if not hasattr(self, 'caller'):
             self.caller = LimitCaller()
        coro = self.session(self, method, timeout=request_timeout)
        if hasattr(method, 'chat_id'):
            return await self.caller.call(method.chat_id, coro)
        else:
            return await coro

def path_bot():
    
    """Patches the bot, these changes are not reversible"""
    
    Bot.__call__ = LimitedBot.__call__