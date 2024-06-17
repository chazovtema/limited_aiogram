from typing import Optional, TypeVar

from aiogram.methods import TelegramMethod, GetChat
from aiogram import Bot

from .limit_caller import LimitCaller

T = TypeVar("T")

class LimitedBot(Bot):

    async def _call(
        self, method: TelegramMethod[T], request_timeout: Optional[int] = None
    ):
        """
        Just to not modify __init__ method
        """
        coro = self.session(self, method, timeout=request_timeout)
        if hasattr(method, "chat_id") and not isinstance(method, GetChat):
            return await self.caller.call(method.chat_id, coro)
        else:
            return await coro

    async def __call__(
        self, method: TelegramMethod[T], request_timeout: Optional[int] = None
    ):
        caller = getattr(self, "caller", None)
        if not caller:
            caller = LimitCaller()
            self.caller = caller
            self.__call__ = LimitedBot._call
        return await LimitedBot._call(self, method, request_timeout)


def patch_bot():
    """Patches the bot, these changes are not reversible"""

    Bot.__call__ = LimitedBot.__call__
