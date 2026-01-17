"""Dispatcher init."""

from aiogram import Dispatcher

from mduck.handlers import commands, echo, new_chat_member


def init_dispatcher() -> Dispatcher:
    """Init dispatcher."""
    dp = Dispatcher()
    dp.include_router(commands.router)
    dp.include_router(new_chat_member.router)
    dp.include_router(echo.router)
    return dp
