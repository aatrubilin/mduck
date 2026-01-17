import enum
import uuid
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, enum.Enum):
    """Environment enum."""

    DEV = "dev"
    STAGE = "stage"
    PROD = "prod"


class Ollama(BaseSettings):
    """Ollama settings."""

    host: str = "http://localhost:11434"
    model: str = "llama2"
    temperature: float = 0.8
    system_prompts_path: str = "./system_prompts.json"


class _TelegramWebhook(BaseSettings):
    """Telegram webhook settings."""

    base_url: str = "https://mduck.example.com"
    path: str = Field(default_factory=lambda: str(uuid.uuid4()))
    secret: str = Field(default_factory=lambda: str(uuid.uuid4()))


class Telegram(BaseSettings):
    """Telegram settings."""

    token: str = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
    webhook: _TelegramWebhook = _TelegramWebhook()


class MDuckSettings(BaseSettings):
    """MDuck settings."""

    response_probability: float = 0.3


class Settings(BaseSettings):
    """Main settings."""

    environment: Environment = Environment.DEV
    mduck: MDuckSettings = MDuckSettings()
    ollama: Ollama = Ollama()
    tg: Telegram = Telegram()

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )


settings = Settings()
