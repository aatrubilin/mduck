from unittest.mock import AsyncMock, MagicMock

import pytest
from aiogram import types

from mduck.handlers.message import message_handler
from mduck.services.mduck import MDuckService


@pytest.mark.asyncio
async def test_message_handler() -> None:
    """Test that the message handler calls the mduck service."""
    # Arrange
    mock_message = AsyncMock(spec=types.Message)
    mock_message.text = "Valid message text"  # Ensure message has text
    mock_service = MagicMock(spec=MDuckService)

    # Act
    await message_handler(message=mock_message, mduck=mock_service)

    # Assert
    mock_service.handle_incoming_message.assert_called_once_with(mock_message)
    # Note: Aiogram filters are applied by the dispatcher, not directly by
    # the handler function call.
    # This test verifies the handler's internal logic assuming the message
    # has passed the filter.
