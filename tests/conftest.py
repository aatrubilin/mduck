import json
from typing import Iterator
from unittest.mock import MagicMock

import aiogram
import httpx
import pytest
from fastapi.testclient import TestClient
from pytest_httpx import HTTPXMock

from config.settings import (
    Environment,
    MDuckSettings,
    Ollama,
    Settings,
    Telegram,
    _TelegramWebhook,
)
from mduck.containers.application import ApplicationContainer
from mduck.main.webhook import create_app


@pytest.fixture
def settings() -> Settings:
    """Return a test settings object."""
    return Settings(
        environment=Environment.DEV,
        mduck=MDuckSettings(
            response_probability_private=1.0,
            response_probability_group=1.0,
            response_probability_supergroup=1.0,
            max_queue_size=5,
        ),
        ollama=Ollama(
            host="http://ollama:11434",
            model="test_model",
            temperature=0.5,
            # prompts_dir_path used by default
        ),
        tg=Telegram(
            token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11",
            webhook=_TelegramWebhook(
                host="http://localhost:8000",
                key="test_key",
                secret="test_secret",
            ),
        ),
    )


@pytest.fixture
def bot_mock() -> MagicMock:
    """Return a mock bot object."""
    return MagicMock(spec=aiogram.Bot)


@pytest.fixture
def dispatcher_mock() -> MagicMock:
    """Return a mock dispatcher object."""
    return MagicMock(spec=aiogram.Dispatcher)


@pytest.fixture(autouse=True)
def mock_ollama_api(settings: Settings, httpx_mock: HTTPXMock) -> None:
    """Mock ollama api requests."""

    def echo_callback(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content)
        prompt = payload["messages"][-1]["content"]
        response_json = {
            "model": settings.ollama.model,
            "created_at": "2023-12-12T14:13:43.416799Z",
            "message": {"role": "assistant", "content": prompt},
            "done": True,
            "total_duration": 5191566416,
            "load_duration": 2154458,
            "prompt_eval_count": 26,
            "prompt_eval_duration": 383809000,
            "eval_count": 298,
            "eval_duration": 4799921000,
        }
        return httpx.Response(200, json=response_json)

    httpx_mock.add_callback(
        echo_callback,
        method="POST",
        url=f"{settings.ollama.host}/api/chat",
        is_optional=True,
    )


@pytest.fixture
def container(
    settings: Settings,
    bot_mock: MagicMock,
    dispatcher_mock: MagicMock,
) -> ApplicationContainer:
    """Return an application container."""
    container = ApplicationContainer()
    container.config.from_pydantic(settings)

    container.gateways.bot.override(bot_mock)
    container.dispatcher.override(dispatcher_mock)

    return container


@pytest.fixture
def client(container: ApplicationContainer) -> Iterator[TestClient]:
    """Return a test client."""
    app = create_app(container=container, set_webhook_retry_timeout=0.0)
    with TestClient(app) as client:
        yield client
