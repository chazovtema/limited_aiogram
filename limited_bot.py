from typing import Optional, TypeVar
from aiogram.client.session.base import BaseSession
from copy import copy
from functools import wraps

from aiogram.methods import TelegramMethod
from aiogram import Bot

from limit_caller import LimitCaller

print(Bot.__call__)
T = TypeVar("T")
# ORIGINAL_CALL = FunctionType(Bot.__call__, '__call__')
ORIGINAL_CALL = copy(Bot.__call__)


class LimitedBot(Bot):
    
    def __init__(self, token: str, session: BaseSession | None = None, parse_mode: str | None = None, disable_web_page_preview: bool | None = None, protect_content: bool | None = None) -> None:
        super().__init__(token, session, parse_mode, disable_web_page_preview, protect_content)
        self.caller = LimitCaller()
    
    @wraps(ORIGINAL_CALL)
    async def __call__(self, method: TelegramMethod[T], request_timeout: Optional[int] = None):
        print(ORIGINAL_CALL)
        coro = ORIGINAL_CALL(method, request_timeout)
        return await ORIGINAL_CALL
        if hasattr(method, 'chat_id'):
            return await self.caller.call(method.chat_id, coro)
        else:
            return await coro


def path_bot():
    
    """Патчит бота в aiogram, эти изменения не обратимы"""
    
    fn = LimitedBot.__call__
    Bot.__call__ = fn
    print(ORIGINAL_CALL)
    print(Bot.__call__)
    print(LimitCaller.__call__)
    