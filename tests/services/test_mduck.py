from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiogram import types
from mduck.services.mduck import MDuckService


@pytest.fixture()
def mock_ollama_repo() -> MagicMock:
    """Fixture for a mocked OllamaRepository."""
    return MagicMock()


@pytest.fixture()
def mock_message() -> MagicMock:
    """Fixture for a mocked aiogram Message."""
    message = MagicMock(spec=types.Message)
    message.chat = MagicMock(spec=types.Chat)
    message.chat.id = 12345
    message.answer = AsyncMock()
    return message


@pytest.mark.asyncio()
async def test_handle_incoming_message_adds_to_queue(
    mock_ollama_repo: MagicMock, mock_message: MagicMock
) -> None:
    """Test that a message is added to the queue if probability check passes."""
    service = MDuckService(ollama_repository=mock_ollama_repo, response_probability=1.0)

    with patch("random.random", return_value=0.5):
        service.handle_incoming_message(mock_message)

    assert not service.message_queue.empty()
    assert mock_message.chat.id in service.chats_with_queued_message
    queued_message = service.message_queue.get_nowait()
    assert queued_message == mock_message


@pytest.mark.asyncio()
async def test_handle_incoming_message_skips_if_chat_already_queued(
    mock_ollama_repo: MagicMock, mock_message: MagicMock
) -> None:
    """Test that a message is not added if chat has a queued message."""
    service = MDuckService(ollama_repository=mock_ollama_repo, response_probability=1.0)
    service.chats_with_queued_message.add(mock_message.chat.id)

    service.handle_incoming_message(mock_message)

    assert service.message_queue.empty()


@pytest.mark.asyncio()
async def test_handle_incoming_message_skips_if_probability_fails(
    mock_ollama_repo: MagicMock, mock_message: MagicMock
) -> None:
    """Test that a message is not added if the probability check fails."""
    service = MDuckService(ollama_repository=mock_ollama_repo, response_probability=0.0)

    with patch("random.random", return_value=0.5):
        service.handle_incoming_message(mock_message)

    assert service.message_queue.empty()


@pytest.mark.asyncio()
async def test_process_message_from_queue(
    mock_ollama_repo: MagicMock, mock_message: MagicMock
) -> None:
    """Test that processing a message from the queue works as expected."""
    service = MDuckService(ollama_repository=mock_ollama_repo)
    service.message_queue.put_nowait(mock_message)
    service.chats_with_queued_message.add(mock_message.chat.id)

    # We run the processor once
    await service.process_message_from_queue()

    mock_message.answer.assert_awaited_once()
    assert service.message_queue.empty()
    assert not service.chats_with_queued_message


@pytest.mark.asyncio()
async def test_process_message_from_queue_handles_exception(
    mock_ollama_repo: MagicMock, mock_message: MagicMock
) -> None:
    """Test that `process_message_from_queue` handles exceptions during reply."""
    service = MDuckService(ollama_repository=mock_ollama_repo)
    service.message_queue.put_nowait(mock_message)
    service.chats_with_queued_message.add(mock_message.chat.id)

    # Configure mock_message.answer to raise an exception
    mock_message.answer.side_effect = Exception("Test exception")

    # Patch the logger to check if error was logged
    with patch("mduck.services.mduck.logger") as mock_logger:
        await service.process_message_from_queue()

    # Assert that answer was called (and raised)
    mock_message.answer.assert_awaited_once()

    # Assert that the error was logged
    mock_logger.error.assert_called_once()
    assert "Error replying to message" in mock_logger.error.call_args[0][0]

    # Crucially, assert that cleanup still happens
    assert service.message_queue.empty()
    assert not service.chats_with_queued_message
