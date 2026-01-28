from unittest.mock import AsyncMock, MagicMock

import pytest
from aiogram import types

from mduck.handlers.chat_member import new_chat_member_handler
from mduck.services.mduck import MDuckService


@pytest.mark.asyncio
async def test_new_chat_member_handler() -> None:
    """Test that the new_chat_member_handler calls the mduck service."""
    # Arrange
    mock_event = AsyncMock(spec=types.ChatMemberUpdated)
    mock_service = MagicMock(spec=MDuckService)

    # Act
    await new_chat_member_handler(event=mock_event, mduck=mock_service)

    # Assert
    mock_service.handle_new_chat_member.assert_called_once_with(mock_event)
