"""Application container."""

from aiogram import Dispatcher
from dependency_injector import containers, providers

from config.settings import settings
from mduck.containers.gateways import GatewaysContainer
from mduck.dp import init_dispatcher
from mduck.log import init_logging
from mduck.services.mduck import MDuckService


class ApplicationContainer(containers.DeclarativeContainer):
    """Application container."""

    wiring_config: containers.WiringConfiguration = containers.WiringConfiguration(
        modules=[
            "mduck.handlers.chat_member",
            "mduck.handlers.message",
            "mduck.routers.webhook",
        ]
    )
    config: providers.Configuration = providers.Configuration(
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
        response_probability_private=config.mduck.response_probability_private,
        response_probability_group=config.mduck.response_probability_group,
        response_probability_supergroup=config.mduck.response_probability_supergroup,
    )

    dispatcher: providers.Provider[Dispatcher] = providers.Singleton(init_dispatcher)

    logging = providers.Resource(
        init_logging,
        log_level=config.log_level,
        log_format=config.log_format,
        service_name=config.service_name,
        log_file=config.log_file,
    )
