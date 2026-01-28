from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiogram import types
from aiogram.enums import ChatAction

from mduck.containers.application import ApplicationContainer
from mduck.handlers.commands import command_start_handler


@pytest.mark.asyncio
@patch("asyncio.sleep", return_value=None)
async def test_command_start_handler(
    mock_sleep: MagicMock, container: ApplicationContainer
) -> None:
    """Test the command_start_handler."""
    # Arrange
    bot = container.gateways.bot()
    mock_message = AsyncMock(spec=types.Message)
    mock_message.bot = bot
    mock_chat = MagicMock()
    mock_chat.id = 12345
    mock_message.chat = mock_chat
    mock_message.answer_sticker = AsyncMock()
    mock_message.answer = AsyncMock()

    # Act
    await command_start_handler(mock_message)

    # Assert
    mock_message.answer_sticker.assert_called_once_with(
        "CAACAgIAAxkBAAMaaWnlQfMMkd91ugpq_xKaf2_FH3UAAgUBAAJWnb0Kt-T9tg5FX3c4BA"
    )
    bot.send_chat_action.assert_any_call(chat_id=12345, action=ChatAction.TYPING)
    assert bot.send_chat_action.call_count == 2
    mock_sleep.assert_any_call(2)
    assert mock_sleep.call_count == 2
    mock_message.answer.assert_any_call(
        "I'm not your friend. I'm not your assistant. \n"
        "*I'm a DUCK* 🦆\n\n"
        "MooDuck that comments on your nonsense\n"
        "if you dare post it...",
        parse_mode="Markdown",
    )
    mock_message.answer.assert_any_call(
        "If you want sarcasm, swearing, and verbal violence —\n"
        "👉 Add me to your group.\n\n"
        "Otherwise, stop wasting my feathers."
    )
    assert mock_message.answer.call_count == 2
