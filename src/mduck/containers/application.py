"""Application container."""

from aiogram import Dispatcher
from dependency_injector import containers, providers

from config.settings import Settings, settings
from mduck.containers.gateways import GatewaysContainer
from mduck.dp import init_dispatcher
from mduck.services.mduck import MDuckService


class ApplicationContainer(containers.DeclarativeContainer):
    """Application container."""

    wiring_config: containers.WiringConfiguration = containers.WiringConfiguration(
        packages=["mduck", "config"]
    )
    config: providers.Provider[Settings] = providers.Configuration(
        pydantic_settings=[settings],
    )

    gateways: providers.Container[GatewaysContainer] = providers.Container(
        GatewaysContainer,
        config=config,
    )

    mduck: providers.Provider[MDuckService] = providers.Singleton(
        MDuckService,
        bot=gateways.bot,
        ollama_repository=gateways.ollama,
        response_probability_private=config.mduck.response_probability_private,  # type: ignore
        response_probability_group=config.mduck.response_probability_group,  # type: ignore
        response_probability_supergroup=config.mduck.response_probability_supergroup,  # type: ignore
    )

    dispatcher: providers.Provider[Dispatcher] = providers.Resource(init_dispatcher)
