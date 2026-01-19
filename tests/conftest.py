from typing import Iterator
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from mduck.containers.application import ApplicationContainer
from mduck.main.webhook import create_app


@pytest.fixture
def client() -> Iterator[TestClient]:
    """Return a test client."""
    container = ApplicationContainer()
    mock_bot = MagicMock()
    mock_bot.set_webhook = AsyncMock(return_value=True)
    container.gateways.bot.override(mock_bot)
    app = create_app(container=container, set_webhook_retry_timeout=0.0)
    with TestClient(app) as client:
        yield client
