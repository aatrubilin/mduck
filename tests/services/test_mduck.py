"""Tests for the MDuckService."""

import asyncio
import contextvars
import random
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiogram import types
from aiogram.enums import ChatAction, ChatType

from mduck.containers.application import ApplicationContainer
from mduck.services.mduck import MDuckService


def _create_mock_message(
    chat_type: str, text: str = "test message", chat_id: int | None = None
) -> MagicMock:
    """Help to create a mock message."""
    mock_message = MagicMock(spec=types.Message)
    mock_message.text = text
    mock_message.chat = MagicMock(spec=types.Chat)
    mock_message.chat.id = (
        chat_id if chat_id is not None else random.randint(1000, 9999)
    )
    mock_message.chat.type = chat_type
    mock_message.reply_to_message = None
    mock_message.answer = AsyncMock()
    return mock_message


@pytest.mark.asyncio
async def test_bot_is_added_sends_welcome(container: ApplicationContainer) -> None:
    """Test that a welcome message is sent when the bot is added to a chat."""
    # Arrange
    mduck_service: MDuckService = container.mduck()
    mock_bot = container.gateways.bot()

    mock_event = AsyncMock(spec=types.ChatMemberUpdated)
    mock_event.chat = MagicMock(spec=types.Chat)
    mock_event.chat.id = 12345
    mock_event.new_chat_member = MagicMock(spec=types.ChatMember)
    mock_event.new_chat_member.user = MagicMock(spec=types.User)
    mock_event.new_chat_member.user.id = mock_bot.id
    mock_event.answer = AsyncMock()
    mock_event.answer_sticker = AsyncMock()

    # Act
    await mduck_service.handle_new_chat_member(mock_event)

    # Assert
    assert mock_event.answer.call_count > 0
    assert mock_event.answer_sticker.call_count == 1
    mock_bot.send_chat_action.assert_called_once()


@pytest.mark.asyncio
async def test_other_user_is_added_does_nothing(
    container: ApplicationContainer,
) -> None:
    """Test that nothing happens when a different user is added."""
    # Arrange
    mduck_service: MDuckService = container.mduck()
    mock_bot = container.gateways.bot()

    mock_event = AsyncMock(spec=types.ChatMemberUpdated)
    mock_event.chat = MagicMock(spec=types.Chat)  # Added this line
    mock_event.new_chat_member = MagicMock(spec=types.ChatMember)
    mock_event.new_chat_member.user = MagicMock(spec=types.User)
    mock_event.new_chat_member.user.id = 987654321  # Different user
    mock_event.answer = AsyncMock()
    mock_event.answer_sticker = AsyncMock()

    # Act
    await mduck_service.handle_new_chat_member(mock_event)

    # Assert
    mock_event.answer.assert_not_called()
    mock_event.answer_sticker.assert_not_called()
    mock_bot.send_chat_action.assert_not_called()


@pytest.mark.asyncio
@patch("random.random", return_value=0.5)
async def test_message_is_queued_on_probability_pass(
    mock_random: MagicMock, container: ApplicationContainer
) -> None:
    """Test that a message is queued if the probability check passes."""
    # Arrange
    mduck_service: MDuckService = container.mduck()
    mduck_service._response_probability[ChatType.PRIVATE] = 0.6
    mock_message = _create_mock_message(chat_type=ChatType.PRIVATE)

    # Act
    await mduck_service.handle_incoming_message(mock_message)

    # Assert
    assert mduck_service.message_queue.qsize() == 1
    assert mock_message.chat.id in mduck_service.chats_with_queued_message


@pytest.mark.asyncio
@patch("random.random", return_value=0.7)
async def test_message_is_skipped_on_probability_fail(
    mock_random: MagicMock, container: ApplicationContainer
) -> None:
    """Test that a message is skipped if the probability check fails."""
    # Arrange
    mduck_service: MDuckService = container.mduck()
    mduck_service._response_probability[ChatType.PRIVATE] = 0.6
    mock_message = _create_mock_message(chat_type=ChatType.PRIVATE)

    # Act
    await mduck_service.handle_incoming_message(mock_message)

    # Assert
    assert mduck_service.message_queue.qsize() == 0
    mock_message.answer.assert_called_once()  # Should send a private message


@pytest.mark.asyncio
async def test_reply_to_bot_is_always_queued(container: ApplicationContainer) -> None:
    """Test that a reply to the bot is always queued."""
    # Arrange
    mduck_service: MDuckService = container.mduck()
    mock_bot = container.gateways.bot()

    mock_message = _create_mock_message(chat_type=ChatType.GROUP)
    mock_message.reply_to_message = types.Message(
        message_id=2,
        date=0,
        chat=mock_message.chat,
        from_user=types.User(id=mock_bot.id, is_bot=True, first_name="TestBot"),
    )

    # Act
    await mduck_service.handle_incoming_message(mock_message)

    # Assert
    assert mduck_service.message_queue.qsize() == 1


@pytest.mark.asyncio
async def test_mention_bot_is_always_queued(container: ApplicationContainer) -> None:
    """Test that a message mentioning the bot is always queued."""
    # Arrange
    mduck_service: MDuckService = container.mduck()
    mock_bot = container.gateways.bot()
    bot_info = AsyncMock(spec=types.User)
    bot_info.username = "TestBot"
    mock_bot.me.return_value = bot_info

    mock_message = _create_mock_message(
        chat_type=ChatType.GROUP, text=f"Hello @{bot_info.username}"
    )

    # Act
    await mduck_service.handle_incoming_message(mock_message)

    # Assert
    assert mduck_service.message_queue.qsize() == 1


@pytest.mark.asyncio
async def test_message_not_queued_if_queue_full(
    container: ApplicationContainer,
) -> None:
    """Test that a message is not queued if the queue is full."""
    # Arrange
    mduck_service: MDuckService = container.mduck()
    mduck_service._max_queue_size = 0  # Set queue size to 0 to simulate full queue
    mock_message = _create_mock_message(chat_type=ChatType.PRIVATE)

    # Act
    await mduck_service.handle_incoming_message(mock_message)

    # Assert
    assert mduck_service.message_queue.qsize() == 0
    mock_message.answer.assert_not_called()


@pytest.mark.asyncio
async def test_message_not_queued_if_chat_already_in_queue(
    container: ApplicationContainer,
) -> None:
    """Test that a message is not queued if the chat already in queue."""
    # Arrange
    mduck_service: MDuckService = container.mduck()
    chat_id = 12345
    mduck_service.chats_with_queued_message.add(chat_id)
    mock_message = _create_mock_message(chat_id=chat_id, chat_type=ChatType.PRIVATE)

    # Act
    await mduck_service.handle_incoming_message(mock_message)

    # Assert
    assert mduck_service.message_queue.qsize() == 0
    mock_message.answer.assert_not_called()


@pytest.mark.asyncio
async def test_empty_message_text_is_ignored(container: ApplicationContainer) -> None:
    """Test that messages without text are ignored."""
    # Arrange
    mduck_service: MDuckService = container.mduck()
    mock_message = _create_mock_message(chat_type=ChatType.PRIVATE, text=None)

    # Act
    await mduck_service.handle_incoming_message(mock_message)

    # Assert
    assert mduck_service.message_queue.qsize() == 0
    mock_message.answer.assert_not_called()


@pytest.mark.asyncio
@patch("mduck.services.mduck.MDuckService._send_typing_periodically")
@patch("random.random", side_effect=[0.1, 0.1])  # For adding 🦆
async def test_process_message_from_queue_success(
    mock_send_typing: MagicMock,
    mock_random: MagicMock,
    container: ApplicationContainer,
) -> None:
    """Test the full processing of a message from the queue."""
    # Arrange
    mduck_service: MDuckService = container.mduck()

    chat_id = 12345
    prompt = "Hello there"
    mock_message = _create_mock_message(
        chat_type=ChatType.PRIVATE, chat_id=chat_id, text=prompt
    )
    mock_message.message_id = 1

    # Put a message in the queue
    context = contextvars.copy_context()
    mduck_service.message_queue.put_nowait((context, mock_message))
    mduck_service.chats_with_queued_message.add(chat_id)

    # Act
    await mduck_service.process_message_from_queue()

    # Assert
    mock_send_typing.assert_called_once()
    mock_message.answer.assert_called_once()

    # Check that metadata is included in the private chat response
    response_text = mock_message.answer.call_args[0][0]
    assert prompt in response_text  # The echo mock API returns the prompt
    assert "metadata" in response_text
    assert "Duration:" in response_text
    assert "Speed:" in response_text
    assert "🦆" in response_text  # Assert that the duck emoji is added

    assert chat_id not in mduck_service.chats_with_queued_message
    assert mduck_service.message_queue.empty()


@pytest.mark.asyncio
async def test_send_typing_periodically(container: ApplicationContainer) -> None:
    """Test that `_send_typing_periodically` sends 'typing' action in a loop."""
    # Arrange
    mduck_service: MDuckService = container.mduck()
    mock_bot = container.gateways.bot()
    chat_id = 12345
    stop_event = asyncio.Event()
    call_count = 0

    # Wrapper to count calls and stop the loop
    async def mock_send_chat_action(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count >= 2:
            stop_event.set()

    mock_bot.send_chat_action.side_effect = mock_send_chat_action

    # Act
    with patch("asyncio.sleep", return_value=None):  # Make sleep instant
        await mduck_service._send_typing_periodically(
            chat_id, stop_event, interval=0.01
        )

    # Assert
    assert call_count >= 2
    mock_bot.send_chat_action.assert_any_call(chat_id=chat_id, action=ChatAction.TYPING)
