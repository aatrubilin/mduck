from typing import Any, Awaitable, Callable

import aiogram
from aiogram.types import TelegramObject, Update

from mduck.log import chat_id_var, update_id_var, user_id_var


class LogContextMiddleware(aiogram.BaseMiddleware):
    """Middleware for setting log context variables from TelegramObject events."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        """
        Set log context variables from TelegramObject events.

        :param handler: The handler to be called.
        :param event: The TelegramObject event.
        :param data: The data associated with the event.
        :return: The result of the handler.
        """
        if isinstance(event, Update):
            update_id_var.set(str(event.update_id))
            if event.message:
                chat_id_var.set(str(event.message.chat.id))
                if event.message.from_user:
                    user_id_var.set(str(event.message.from_user.id))
        return await handler(event, data)
