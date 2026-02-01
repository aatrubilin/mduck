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
    prompts_dir_path: str = str(Path(__file__).parent.parent / "prompts")


class Redis(BaseSettings):
    """Redis settings."""

    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: str | None = None


class _TelegramWebhook(BaseSettings):
    """Telegram webhook settings."""

    host: str = "https://mduck.example.com"
    key: str = Field(default_factory=lambda: str(uuid.uuid4()))
    secret: str = Field(default_factory=lambda: str(uuid.uuid4()))


class Telegram(BaseSettings):
    """Telegram settings."""

    token: str = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
    webhook: _TelegramWebhook = _TelegramWebhook()


class MDuckSettings(BaseSettings):
    """MDuck settings."""

    response_probability_private: float = 0.3
    response_probability_group: float = 0.3
    response_probability_supergroup: float = 0.3
    max_queue_size: int = 10


class Settings(BaseSettings):
    """Main settings."""

    environment: Environment = Environment.DEV
    mduck: MDuckSettings = MDuckSettings()
    ollama: Ollama = Ollama()
    tg: Telegram = Telegram()
    redis: Redis = Redis()

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )


settings = Settings()
