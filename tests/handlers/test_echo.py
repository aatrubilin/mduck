from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiogram import types
from mduck.handlers.echo import echo


@pytest.mark.asyncio()
@patch("builtins.print")
async def test_echo_handler(mock_print: MagicMock) -> None:
    """Test that the echo handler prints the message."""
    # Arrange
    mock_message = AsyncMock(spec=types.Message)

    # Act
    await echo(mock_message)

    # Assert
    mock_print.assert_called_once_with(mock_message)
