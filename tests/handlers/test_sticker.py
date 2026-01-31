"""Tests for the sticker handler."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from aiogram import types
from aiogram.enums.parse_mode import ParseMode

from mduck.handlers.sticker import message_handler


@pytest.mark.asyncio
async def test_message_handler_with_sticker() -> None:
    """Test that the message handler replies with the sticker ID."""
    # Arrange
    mock_sticker = MagicMock(spec=types.Sticker)
    mock_sticker.file_id = "test_sticker_file_id"

    mock_message = AsyncMock(spec=types.Message)
    mock_message.sticker = mock_sticker
    mock_message.answer = AsyncMock()

    # Act
    await message_handler(mock_message)

    # Assert
    mock_message.answer.assert_called_once_with(
        f"Sticker id: `{mock_sticker.file_id}`", parse_mode=ParseMode.MARKDOWN
    )


@pytest.mark.asyncio
async def test_message_handler_without_sticker() -> None:
    """Test that the message handler does nothing if no sticker is present."""
    # Arrange
    mock_message = AsyncMock(spec=types.Message)
    mock_message.sticker = None
    mock_message.answer = AsyncMock()

    # Act
    await message_handler(mock_message)

    # Assert
    mock_message.answer.assert_not_called()
