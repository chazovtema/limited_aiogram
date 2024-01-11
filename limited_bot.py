import logging
import asyncio
from typing import Optional, TypeVar
from aiogram.client.session.base import BaseSession

from aiogram.methods import TelegramMethod
from aiogram import Bot, types

from .limit_caller import LimitCaller

T = TypeVar("T")

class RestrictedBot(Bot):
    
    def __init__(self, token: str, session: BaseSession | None = None, parse_mode: str | None = None, disable_web_page_preview: bool | None = None, protect_content: bool | None = None) -> None:
        super().__init__(token, session, parse_mode, disable_web_page_preview, protect_content)
        self.caller = LimitCaller()
    
    async def __call__(self, method: TelegramMethod[T], request_timeout: Optional[int] = None):
        
        coro = super().__call__(method, request_timeout)
        if hasattr(method, 'chat_id'):
            return await self.caller.call(method.chat_id, coro)
        else:
            return await coro

def path_bot():
    
    """Патчит бота в aiogram, эти изменения не обратимы"""
    
    Bot.__call__ = RestrictedBot.__call__
    
    