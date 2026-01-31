"""Tests for the LogContextMiddleware."""

from unittest.mock import MagicMock

import pytest
from aiogram import types
from aiogram.types import Chat, Message, Update, User

from mduck.log import chat_id_var, update_id_var, user_id_var
from mduck.middlewares.log_context import LogContextMiddleware


@pytest.mark.asyncio
async def test_log_context_middleware_with_message() -> None:
    """Test that the middleware sets log context variables correctly for a message."""
    # Arrange
    update_id = 12345
    chat_id = 67890
    user_id = 13579

    mock_user = User(id=user_id, is_bot=False, first_name="Test")
    mock_chat = Chat(id=chat_id, type="private")
    mock_message = Message(
        message_id=24680, date=0, chat=mock_chat, from_user=mock_user, text="test"
    )
    mock_update = Update(update_id=update_id, message=mock_message)

    async def handler(event: Update, data: dict) -> None:
        # Assert that context variables are set within the handler
        assert update_id_var.get() == str(update_id)
        assert chat_id_var.get() == str(chat_id)
        assert user_id_var.get() == str(user_id)

    middleware = LogContextMiddleware()

    # Act
    await middleware(handler, mock_update, {})


@pytest.mark.asyncio
async def test_log_context_middleware_without_message() -> None:
    """Test that the middleware handles updates without a message."""
    # Arrange
    update_id = 54321
    mock_update = Update(update_id=update_id, message=None)

    async def handler(event: Update, data: dict) -> None:
        # Assert that only update_id is set
        assert update_id_var.get() == str(update_id)
        assert chat_id_var.get() == ""
        assert user_id_var.get() == ""

    middleware = LogContextMiddleware()

    # Act
    await middleware(handler, mock_update, {})


@pytest.mark.asyncio
async def test_log_context_middleware_without_from_user() -> None:
    """Test that the middleware handles messages without a 'from_user'."""
    # Arrange
    update_id = 98765
    chat_id = 54321

    mock_chat = MagicMock(spec=types.Chat)
    mock_chat.id = chat_id
    mock_message = MagicMock(spec=types.Message)
    mock_message.chat = mock_chat
    mock_message.from_user = None

    mock_update = MagicMock(spec=types.Update)
    mock_update.update_id = update_id
    mock_update.message = mock_message

    async def handler(event: Update, data: dict) -> None:
        # Assert that update_id and chat_id are set
        assert update_id_var.get() == str(update_id)
        assert chat_id_var.get() == str(chat_id)
        assert user_id_var.get() == ""

    middleware = LogContextMiddleware()

    # Act
    await middleware(handler, mock_update, {})
