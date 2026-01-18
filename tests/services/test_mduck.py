import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiogram import Bot, types
from aiogram.enums import ChatAction, ChatType, ParseMode

from mduck.services.mduck import MDuckService


@pytest.fixture
def mock_ollama_repo() -> MagicMock:
    """Fixture for a mocked OllamaRepository."""
    repo = MagicMock()
    repo.generate_response = AsyncMock(return_value="Ollama response")
    return repo


@pytest.fixture
def mock_bot() -> MagicMock:
    """Fixture for a mocked aiogram Bot."""
    bot = MagicMock(spec=Bot)
    bot.send_chat_action = AsyncMock()
    return bot


@pytest.fixture
def mock_message() -> MagicMock:
    """Fixture for a mocked aiogram Message."""
    message = MagicMock(spec=types.Message)
    message.chat = MagicMock(spec=types.Chat)
    message.chat.id = 12345
    message.chat.type = ChatType.PRIVATE
    message.text = "User prompt"
    message.answer = AsyncMock()
    # No message.bot needed, as MDuckService now uses its own injected bot
    return message


@pytest.mark.asyncio
async def test_handle_incoming_message_adds_to_queue(
    mock_bot: MagicMock, mock_ollama_repo: MagicMock, mock_message: MagicMock
) -> None:
    """Test that a message is added to the queue if probability check passes."""
    service = MDuckService(
        bot=mock_bot,
        ollama_repository=mock_ollama_repo,
        response_probability_private=1.0,
    )

    with patch("random.random", return_value=0.5):
        await service.handle_incoming_message(mock_message)

    assert not service.message_queue.empty()
    assert mock_message.chat.id in service.chats_with_queued_message
    queued_message = service.message_queue.get_nowait()
    assert queued_message == mock_message


@pytest.mark.asyncio
async def test_handle_incoming_message_skips_if_chat_already_queued(
    mock_bot: MagicMock, mock_ollama_repo: MagicMock, mock_message: MagicMock
) -> None:
    """Test that a message is not added if chat has a queued message."""
    service = MDuckService(
        bot=mock_bot,
        ollama_repository=mock_ollama_repo,
        response_probability_private=1.0,
    )
    service.chats_with_queued_message.add(mock_message.chat.id)

    await service.handle_incoming_message(mock_message)

    assert service.message_queue.empty()


@pytest.mark.asyncio
async def test_handle_incoming_message_skips_if_probability_fails(
    mock_bot: MagicMock, mock_ollama_repo: MagicMock, mock_message: MagicMock
) -> None:
    """Test that a message is not added if the probability check fails."""
    service = MDuckService(
        bot=mock_bot,
        ollama_repository=mock_ollama_repo,
        response_probability_private=0.0,
    )

    with patch("random.random", return_value=0.5):
        await service.handle_incoming_message(mock_message)

    assert service.message_queue.empty()
    mock_message.answer.assert_awaited_once()


@pytest.mark.asyncio
async def test_process_message_from_queue(
    mock_bot: MagicMock, mock_ollama_repo: MagicMock, mock_message: MagicMock
) -> None:
    """Test that processing a message from the queue works as expected."""
    service = MDuckService(bot=mock_bot, ollama_repository=mock_ollama_repo)
    service.message_queue.put_nowait(mock_message)
    service.chats_with_queued_message.add(mock_message.chat.id)

    # Make ollama_repo.generate_response take some time to allow typing actions to occur
    async def delayed_generate_response(*args, **kwargs):
        await asyncio.sleep(0.1)  # Simulate some processing time
        return "Ollama response"

    mock_ollama_repo.generate_response.side_effect = delayed_generate_response

    await service.process_message_from_queue()

    # Assert that "typing" action was sent multiple times periodically
    # The exact number depends on the `_send_typing_periodically`
    # interval and `generate_response` delay
    # With interval=4 and delay=0.1, it should be called at least once
    # For more robust testing, a higher delay and checking for multiple calls is better.
    # Here we aim for at least one call given the minimal delay.
    mock_bot.send_chat_action.assert_called()
    assert (
        mock_bot.send_chat_action.call_count >= 1
    )  # It will be called at least once before the sleep in generate_response finishes
    mock_bot.send_chat_action.assert_any_call(
        chat_id=mock_message.chat.id, action=ChatAction.TYPING
    )

    # Assert that ollama repo was called
    mock_ollama_repo.generate_response.assert_called_once_with(mock_message.text)

    # Assert that the response was sent
    mock_message.answer.assert_awaited_once_with(
        "Ollama response", parse_mode=ParseMode.MARKDOWN
    )

    # Assert that cleanup still happens
    assert service.message_queue.empty()
    assert not service.chats_with_queued_message


@pytest.mark.asyncio
async def test_process_message_from_queue_handles_exception(
    mock_bot: MagicMock, mock_ollama_repo: MagicMock, mock_message: MagicMock
) -> None:
    """Test that `process_message_from_queue` handles exceptions during generation."""
    # Configure ollama repo to raise an exception
    mock_ollama_repo.generate_response.side_effect = Exception("Ollama failed")

    service = MDuckService(bot=mock_bot, ollama_repository=mock_ollama_repo)
    service.message_queue.put_nowait(mock_message)
    service.chats_with_queued_message.add(mock_message.chat.id)

    # Patch the logger to check if error was logged
    with patch("mduck.services.mduck.logger") as mock_logger:
        await service.process_message_from_queue()

    # Assert that a user-facing error message was sent
    mock_message.answer.assert_awaited_once_with(
        "Извините, произошла ошибка при обработке вашего сообщения."
    )

    # Assert that the error was logged
    mock_logger.error.assert_called_once()
    assert "Error processing message" in mock_logger.error.call_args[0][0]

    # Crucially, assert that cleanup still happens
    assert service.message_queue.empty()
    assert not service.chats_with_queued_message


@pytest.mark.asyncio
async def test_handle_incoming_message_skips_on_empty_text(
    mock_bot: MagicMock, mock_ollama_repo: MagicMock, mock_message: MagicMock
) -> None:
    """Test that handle_incoming_message skips if message text is empty."""
    mock_message.text = None  # Simulate empty text
    service = MDuckService(
        bot=mock_bot,
        ollama_repository=mock_ollama_repo,
        response_probability_private=1.0,
    )

    await service.handle_incoming_message(mock_message)

    assert service.message_queue.empty()
    assert mock_message.chat.id not in service.chats_with_queued_message


@pytest.mark.asyncio
async def test_process_message_from_queue_raises_on_empty_text(
    mock_bot: MagicMock, mock_ollama_repo: MagicMock, mock_message: MagicMock
) -> None:
    """Test process_message_from_queue raises RuntimeError if message text is None."""
    # Simulate a message with None text, bypassing normal handler flow
    mock_message.text = None
    service = MDuckService(bot=mock_bot, ollama_repository=mock_ollama_repo)
    service.message_queue.put_nowait(mock_message)
    service.chats_with_queued_message.add(mock_message.chat.id)

    with patch("mduck.services.mduck.logger") as mock_logger:
        await service.process_message_from_queue()

    # Assert that a user-facing error message was sent
    mock_message.answer.assert_awaited_once_with(
        "Извините, произошла ошибка при обработке вашего сообщения."
    )

    # Assert that the RuntimeError was logged
    mock_logger.error.assert_called_once()
    # Check the specific RuntimeError message
    assert "Empty message text" in str(mock_logger.error.call_args[0][2])

    # Ensure cleanup still happens
    assert service.message_queue.empty()
    assert not service.chats_with_queued_message


@pytest.mark.asyncio
async def test_process_message_handles_nested_exception(
    mock_bot: MagicMock, mock_ollama_repo: MagicMock, mock_message: MagicMock
) -> None:
    """Test that `process_message_from_queue` handles nested exceptions."""
    # Configure ollama repo to raise the first exception
    mock_ollama_repo.generate_response.side_effect = Exception("Ollama failed")

    # Configure message.answer to raise the second exception
    mock_message.answer.side_effect = Exception("Failed to send error message")

    service = MDuckService(bot=mock_bot, ollama_repository=mock_ollama_repo)
    service.message_queue.put_nowait(mock_message)
    service.chats_with_queued_message.add(mock_message.chat.id)

    with patch("mduck.services.mduck.logger") as mock_logger:
        await service.process_message_from_queue()

    # Assert that the first error was logged
    mock_logger.error.assert_any_call(
        "Error processing message in chat %s: %s",
        mock_message.chat.id,
        mock_ollama_repo.generate_response.side_effect,
        exc_info=True,
    )

    # Assert that the second, nested error was also logged
    mock_logger.error.assert_any_call(
        "Failed to send error message to chat %s: %s",
        mock_message.chat.id,
        mock_message.answer.side_effect,
        exc_info=True,
    )

    # Crucially, assert that cleanup still happens
    assert service.message_queue.empty()
    assert not service.chats_with_queued_message


@pytest.mark.asyncio
async def test_send_typing_periodically_handles_exception(
    mock_bot: MagicMock, mock_ollama_repo: MagicMock
) -> None:
    """Test that _send_typing_periodically handles exceptions."""
    service = MDuckService(bot=mock_bot, ollama_repository=mock_ollama_repo)
    mock_bot.send_chat_action.side_effect = Exception("Test Exception")
    stop_event = asyncio.Event()

    with patch("mduck.services.mduck.logger") as mock_logger:
        # We need to run the task and give it a moment to execute
        task = asyncio.create_task(
            service._send_typing_periodically(chat_id=123, stop_event=stop_event)
        )
        await asyncio.sleep(0.1)
        stop_event.set()
        await task

    mock_logger.warning.assert_called_once()
