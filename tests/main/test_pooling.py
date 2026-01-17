from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from mduck.main.pooling import main, start_pooling


@pytest.mark.asyncio()
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


@pytest.mark.asyncio()
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


@patch("mduck.main.pooling.start_pooling", new_callable=AsyncMock)
@patch("mduck.main.pooling.logging.basicConfig")
@patch("mduck.main.pooling.argparse.ArgumentParser")
def test_main(
    mock_argparse: MagicMock,
    mock_logging: MagicMock,
    mock_start_pooling: AsyncMock,
) -> None:
    """Test the main function."""
    # Arrange
    mock_args = MagicMock()
    mock_args.log_level = "info"
    mock_argparse.return_value.parse_args.return_value = mock_args

    # Act
    main()

    # Assert
    mock_argparse.assert_called_once_with(description="Run the FastAPI application.")
    mock_logging.assert_called_once_with(level="INFO")
    mock_start_pooling.assert_called_once()
