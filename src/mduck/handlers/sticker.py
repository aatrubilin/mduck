"""Sticker handler."""

import aiogram
from aiogram import F, types
from aiogram.enums.parse_mode import ParseMode

router = aiogram.Router(name="sticker")


@router.message(F.sticker)
async def message_handler(message: types.Message) -> None:
    """Message handler."""
    if message.sticker:
        await message.answer(
            f"Sticker id: `{message.sticker.file_id}`", parse_mode=ParseMode.MARKDOWN
        )
