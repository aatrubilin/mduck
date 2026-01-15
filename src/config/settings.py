import enum
from pathlib import Path
from typing import Annotated

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
    system_prompts: Annotated[
        list[str],
        Field(min_length=1),
    ] = ["You are a helpful assistant."]


class Settings(BaseSettings):
    """Main settings."""

    environment: Environment = Environment.DEV
    ollama: Ollama = Ollama()

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )


settings = Settings()
