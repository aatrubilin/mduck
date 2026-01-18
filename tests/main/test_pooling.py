import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from watchdog.events import FileSystemEvent

from mduck.main.pooling import (
    CodeChangeHandler,
    main,
    run_mduck_processor,
    run_reloader,
    start_pooling,
)


@pytest.mark.asyncio
@patch("mduck.main.pooling.ApplicationContainer")
async def test_start_pooling(mock_container: MagicMock) -> None:
    """Test the start_pooling function."""
    # Arrange
    mock_dispatcher = AsyncMock()
    mock_bot = AsyncMock()
    mock_container.return_value.dispatcher.return_value = mock_dispatcher
    mock_container.return_value.gateways.bot.return_value = mock_bot

    # Act
    await start_pooling()

    # Assert
    mock_dispatcher.start_polling.assert_called_once_with(mock_bot)


@pytest.mark.asyncio
async def test_start_pooling_with_container() -> None:
    """Test the start_pooling function with a container."""
    # Arrange
    mock_container = MagicMock()
    mock_dispatcher = AsyncMock()
    mock_bot = AsyncMock()
    mock_container.dispatcher.return_value = mock_dispatcher
    mock_container.gateways.bot.return_value = mock_bot

    # Act
    await start_pooling(mock_container)

    # Assert
    mock_dispatcher.start_polling.assert_called_once_with(mock_bot)


@patch("mduck.main.pooling.asyncio.run")
@patch("mduck.main.pooling.logging.basicConfig")
@patch("mduck.main.pooling.argparse.ArgumentParser")
def test_main(
    mock_argparse: MagicMock,
    mock_logging: MagicMock,
    mock_asyncio_run: MagicMock,
) -> None:
    """Test the main function."""
    # Arrange
    mock_args = MagicMock()
    mock_args.log_level = "info"
    mock_args.reload = False
    mock_argparse.return_value.parse_args.return_value = mock_args

    # Act
    main()

    # Assert
    mock_argparse.assert_called_once_with(description="Run the pooling application.")
    mock_logging.assert_called_once_with(level="INFO")
    mock_asyncio_run.assert_called_once()


@patch("mduck.main.pooling.run_reloader")
@patch("mduck.main.pooling.logging.basicConfig")
@patch("mduck.main.pooling.argparse.ArgumentParser")
def test_main_with_reload(
    mock_argparse: MagicMock,
    mock_logging: MagicMock,
    mock_run_reloader: MagicMock,
) -> None:
    """Test the main function with reload."""
    # Arrange
    mock_args = MagicMock()
    mock_args.log_level = "info"
    mock_args.reload = True
    mock_argparse.return_value.parse_args.return_value = mock_args

    # Act
    main()

    # Assert
    mock_argparse.assert_called_once_with(description="Run the pooling application.")
    mock_logging.assert_called_once_with(level="INFO")
    mock_run_reloader.assert_called_once()


@patch("mduck.main.pooling.sys.exit")
@patch("mduck.main.pooling.Observer")
@patch("mduck.main.pooling.CodeChangeHandler")
@patch("mduck.main.pooling.time.sleep", side_effect=KeyboardInterrupt)
def test_run_reloader(
    mock_sleep: MagicMock,
    mock_handler: MagicMock,
    mock_observer: MagicMock,
    mock_exit: MagicMock,
) -> None:
    """Test the run_reloader function."""
    # Arrange
    mock_observer_instance = MagicMock()
    mock_observer.return_value = mock_observer_instance

    # Act
    run_reloader()

    # Assert
    mock_observer.assert_called_once()
    mock_observer_instance.schedule.assert_called_once()
    mock_observer_instance.start.assert_called_once()
    mock_sleep.assert_called_once()
    mock_observer_instance.stop.assert_called_once()
    mock_observer_instance.join.assert_called_once()
    mock_exit.assert_called_once_with(0)


@patch("mduck.main.pooling.time.time")
@patch("mduck.main.pooling.subprocess.Popen")
def test_code_change_handler(mock_popen: MagicMock, mock_time: MagicMock) -> None:
    """Test the CodeChangeHandler."""
    # Arrange
    mock_time.side_effect = [1.0, 2.0, 3.0]
    handler = CodeChangeHandler()
    mock_popen.assert_called_once()
    handler.on_any_event(FileSystemEvent("src"))

    # Assert
    assert mock_popen.call_count == 2


@pytest.mark.asyncio
async def test_run_mduck_processor() -> None:
    """Test the run_mduck_processor function."""
    # Arrange
    mock_mduck = MagicMock()
    mock_mduck.process_message_from_queue = AsyncMock(
        side_effect=[None, None, asyncio.CancelledError]
    )

    # Act
    with pytest.raises(asyncio.CancelledError):
        await run_mduck_processor(mock_mduck)

    # Assert
    assert mock_mduck.process_message_from_queue.call_count == 3
