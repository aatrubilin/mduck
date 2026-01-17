"""Echo router."""

import aiogram
from aiogram import types

router = aiogram.Router(name="echo")


@router.message()
async def echo(message: types.Message) -> None:
    """Echo handler."""
    print(message)
