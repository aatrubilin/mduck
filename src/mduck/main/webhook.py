import argparse
import asyncio
import contextlib
import logging  # Add this
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI

from mduck.containers.application import ApplicationContainer
from mduck.routers import healthcheck
from mduck.services.mduck import MDuckService
from mduck.version import __version__

logger = logging.getLogger("mduck")  # Add this


async def run_mduck_processor(mduck: MDuckService) -> None:
    """Run mduck processor."""
    while True:
        await mduck.process_message_from_queue()


def create_app(container: ApplicationContainer | None = None) -> FastAPI:
    """Create and configure the FastAPI application."""
    container = container or ApplicationContainer()

    @contextlib.asynccontextmanager
    async def lifespan(app: FastAPI) -> "AsyncGenerator[None, None]":
        mduck: MDuckService = container.mduck()
        asyncio.create_task(run_mduck_processor(mduck))
        logger.info("MDuckService background processor started.")  # Add this
        yield

    app = FastAPI(version=__version__, lifespan=lifespan)
    app.state.container = container
    app.include_router(healthcheck.router)

    return app


def main() -> None:
    """Parse arguments and run the application."""
    parser = argparse.ArgumentParser(description="Run the FastAPI application.")
    parser.add_argument(
        "--host", type=str, default="0.0.0.0", help="Host address to bind to."
    )
    parser.add_argument("--port", type=int, default=8000, help="Port to listen on.")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reloading.")
    parser.add_argument("--log-level", type=str, default="info", help="Log level.")

    args = parser.parse_args()

    uvicorn_params = {
        "app": "mduck.main.webhook:create_app",
        "host": args.host,
        "port": args.port,
        "reload": args.reload,
        "log_level": args.log_level,
        "factory": True,
    }

    if args.reload:
        uvicorn_params["reload_dirs"] = ["src"]

    uvicorn.run(**uvicorn_params)


if __name__ == "__main__":  # pragma: no cover
    main()
