"""Commands router."""

import asyncio

from aiogram import Router, filters, types
from aiogram.enums import ChatAction

router = Router(name="commands")


@router.message(filters.CommandStart())
async def command_start_handler(message: types.Message) -> None:
    """Handle messages with `/start` command."""
    assert message.bot is not None
    await message.answer_sticker(
        "CAACAgIAAxkBAAMaaWnlQfMMkd91ugpq_xKaf2_FH3UAAgUBAAJWnb0Kt-T9tg5FX3c4BA"
    )
    await message.bot.send_chat_action(
        chat_id=message.chat.id, action=ChatAction.TYPING
    )
    await asyncio.sleep(2)

    await message.answer(
        "I'm not your friend. I'm not your assistant. \n"
        "*I'm a DUCK* 🦆\n\n"
        "MooDuck that comments on your nonsense\n"
        "if you dare post it...",
        parse_mode="Markdown",
    )
    await message.bot.send_chat_action(
        chat_id=message.chat.id, action=ChatAction.TYPING
    )
    await asyncio.sleep(2)

    await message.answer(
        "If you want sarcasm, swearing, and verbal violence —\n"
        "👉 Add me to your group.\n\n"
        "Otherwise, stop wasting my feathers."
    )
