from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiogram import types
from aiogram.enums import ChatAction

from mduck.handlers.new_chat_member import new_chat_member_handler


@pytest.mark.asyncio
@patch("asyncio.sleep", return_value=None)
async def test_new_chat_member_handler_with_bot(mock_sleep: MagicMock) -> None:
    """Test the new_chat_member_handler when the bot is added."""
    # Arrange
    mock_bot = AsyncMock()
    mock_bot.id = 12345
    mock_message = AsyncMock(spec=types.Message)
    mock_message.bot = mock_bot
    mock_chat = MagicMock()
    mock_chat.id = 54321
    mock_message.chat = mock_chat

    bot_user = types.User(id=12345, is_bot=True, first_name="Test Bot")
    mock_message.new_chat_members = [bot_user]
    mock_bot.get_me.return_value = bot_user
    mock_message.answer = AsyncMock()
    mock_message.answer_sticker = AsyncMock()

    # Act
    await new_chat_member_handler(mock_message)

    # Assert
    mock_message.answer.assert_any_call(
        "🦆 *MooDuck* entered the chat.", parse_mode="Markdown"
    )
    mock_message.answer_sticker.assert_called_once_with(
        "CAACAgIAAxkBAAM6aWn2HORULYp5Uiioos8LjHZrAUIAAvYAA1advQr3204hQD6lijgE",
    )
    mock_bot.send_chat_action.assert_called_once_with(
        chat_id=54321,
        action=ChatAction.TYPING,
    )
    mock_sleep.assert_called_once_with(2)
    mock_message.answer.assert_any_call(
        "Krak. Looks like this group needed more sarcasm.\n\n"
        "I don't help. I judge.\n"
        "I don't fix. I mock.\n\n"
        "Too late to regret now.",
    )
    assert mock_message.answer.call_count == 2


@pytest.mark.asyncio
async def test_new_chat_member_handler_with_other_user() -> None:
    """Test the new_chat_member_handler when another user is added."""
    # Arrange
    mock_bot = AsyncMock()
    mock_bot.id = 12345
    mock_message = AsyncMock(spec=types.Message)
    mock_message.bot = mock_bot
    mock_chat = MagicMock()
    mock_chat.id = 54321
    mock_message.chat = mock_chat

    bot_user = types.User(id=12345, is_bot=True, first_name="Test Bot")
    other_user = types.User(id=67890, is_bot=False, first_name="Test User")
    mock_message.new_chat_members = [other_user]
    mock_bot.get_me.return_value = bot_user
    mock_message.answer = AsyncMock()
    mock_message.answer_sticker = AsyncMock()

    # Act
    await new_chat_member_handler(mock_message)

    # Assert
    mock_message.answer.assert_not_called()
    mock_message.answer_sticker.assert_not_called()
