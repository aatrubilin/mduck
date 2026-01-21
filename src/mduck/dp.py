"""Dispatcher init."""

from aiogram import Dispatcher

from mduck.middlewares.log_context import LogContextMiddleware


def init_dispatcher() -> Dispatcher:
    """Init dispatcher."""
    from mduck.handlers import chat_member, commands, message

    dp = Dispatcher()

    dp.update.middleware.register(LogContextMiddleware())

    dp.include_router(commands.router)
    dp.include_router(chat_member.router)
    dp.include_router(message.router)
    return dp
