"""Dispatcher init."""

from aiogram import Dispatcher


def init_dispatcher() -> Dispatcher:
    """Init dispatcher."""
    from mduck.handlers import commands, message, new_chat_member

    dp = Dispatcher()
    dp.include_router(commands.router)
    dp.include_router(new_chat_member.router)
    dp.include_router(message.router)
    return dp
