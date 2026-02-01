from aiogram import Bot
from dependency_injector import containers, providers
from redis.asyncio import Redis

from config.settings import Settings
from mduck.repositories.ollama import OllamaRepository
from mduck.repositories.redis import RedisResource


class GatewaysContainer(containers.DeclarativeContainer):
    """Container for application gateways."""

    config: providers.Provider[Settings] = providers.Configuration()

    bot: providers.Singleton[Bot] = providers.Singleton(
        Bot,
        token=config.tg.token,  # type: ignore
    )

    ollama: providers.Factory[OllamaRepository] = providers.Factory(
        OllamaRepository,
        host=config.ollama.host,  # type: ignore
        model=config.ollama.model,  # type: ignore
        temperature=config.ollama.temperature,  # type: ignore
        prompts_dir_path=config.ollama.prompts_dir_path,  # type: ignore
    )

    redis: providers.Resource[Redis] = providers.Resource(
        RedisResource,  # type: ignore[arg-type]
        host=config.redis.host,  # type: ignore
        port=config.redis.port,  # type: ignore
        db=config.redis.db,  # type: ignore
        password=config.redis.password,  # type: ignore
    )
