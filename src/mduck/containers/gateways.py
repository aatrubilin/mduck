from aiogram import Bot
from dependency_injector import containers, providers

from config.settings import Settings
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
        prompts_dir_path=config.ollama.prompts_dir_path,  # type: ignore
    )
