from aiogram import Bot
from config.settings import Settings
from dependency_injector import containers, providers


class GatewaysContainer(containers.DeclarativeContainer):
    """Container for application gateways."""

    config: providers.Provider[Settings] = providers.Configuration()

    bot: providers.Singleton[Bot] = providers.Singleton(
        Bot,
        token=config.provided.tg.token,
    )
