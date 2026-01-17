from aiogram import Bot
from config.settings import Settings
from dependency_injector import containers, providers

from mduck.repositories.ollama import OllamaRepository


class GatewaysContainer(containers.DeclarativeContainer):
    """Container for application gateways."""

    config: providers.Provider[Settings] = providers.Configuration()

    bot: providers.Singleton[Bot] = providers.Singleton(
        Bot,
        token=config.provided.tg.token,
    )

    ollama: providers.Factory[OllamaRepository] = providers.Factory(
        OllamaRepository,
        host=config.provided.ollama.host,
        model=config.provided.ollama.model,
        temperature=config.provided.ollama.temperature,
        system_prompts=config.provided.ollama.system_prompts,
    )
