"""Application container."""

from config.settings import Settings, settings
from dependency_injector import containers, providers


class ApplicationContainer(containers.DeclarativeContainer):
    """Application container."""

    wiring_config = containers.WiringConfiguration(packages=["mduck", "config"])

    config: providers.Provider[Settings] = providers.Configuration(
        pydantic_settings=[settings],
    )
