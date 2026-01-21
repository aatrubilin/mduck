from typing import Iterator
from unittest.mock import MagicMock

import aiogram
import pytest
from fastapi.testclient import TestClient

from mduck.containers.application import ApplicationContainer
from mduck.main.webhook import create_app


@pytest.fixture
def container() -> ApplicationContainer:
    """Return an application container."""
    container = ApplicationContainer()

    mock_bot = MagicMock(spec=aiogram.Bot)
    container.gateways.bot.override(mock_bot)

    return container


@pytest.fixture
def client(container: ApplicationContainer) -> Iterator[TestClient]:
    """Return a test client."""
    app = create_app(container=container, set_webhook_retry_timeout=0.0)
    with TestClient(app) as client:
        yield client
