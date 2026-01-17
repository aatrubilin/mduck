"""Router for new chat members."""

import asyncio

from aiogram import Router, types
from aiogram.enums import ChatAction

router = Router(name="new_chat_member")


@router.message(lambda message: message.new_chat_members is not None)
async def new_chat_member_handler(message: types.Message) -> None:
    """Handle new chat members."""
    assert message.new_chat_members is not None
    assert message.bot is not None

    bot_info = await message.bot.get_me()
    is_bot_added = False
    for member in message.new_chat_members:
        if member.id == bot_info.id:
            is_bot_added = True
            break

    if is_bot_added:
        await message.answer("🦆 *MooDuck* entered the chat.", parse_mode="Markdown")
        await message.answer_sticker(
            "CAACAgIAAxkBAAM6aWn2HORULYp5Uiioos8LjHZrAUIAAvYAA1advQr3204hQD6lijgE",
        )
        await message.bot.send_chat_action(
            chat_id=message.chat.id,
            action=ChatAction.TYPING,
        )
        await asyncio.sleep(2)

        await message.answer(
            "Krak. Looks like this group needed more sarcasm.\n\n"
            "I don't help. I judge.\n"
            "I don't fix. I mock.\n\n"
            "Too late to regret now.",
        )
