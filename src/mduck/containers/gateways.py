from aiogram import Bot
from config.settings import Settings
from dependency_injector import containers, providers

from mduck.repositories.ollama import OllamaRepository


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
        system_prompts=config.ollama.system_prompts,  # type: ignore
    )
