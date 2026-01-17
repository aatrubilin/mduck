"""Application container."""

from aiogram import Dispatcher
from config.settings import Settings, settings
from dependency_injector import containers, providers

from mduck.containers.gateways import GatewaysContainer
from mduck.dp import init_dispatcher


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

    dispatcher: providers.Provider[Dispatcher] = providers.Resource(init_dispatcher)
