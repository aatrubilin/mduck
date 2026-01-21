import argparse
import asyncio
import contextlib
import logging
import os
from typing import AsyncGenerator

import aiogram
import uvicorn
from fastapi import FastAPI

from mduck.containers.application import ApplicationContainer
from mduck.routers import healthcheck, webhook, whoami
from mduck.services.mduck import MDuckService
from mduck.version import __version__

logger = logging.getLogger("mduck.main.webhook")


async def run_mduck_processor(mduck: MDuckService) -> None:
    """Run mduck processor."""
    while True:
        await mduck.process_message_from_queue()


def create_app(
    container: ApplicationContainer | None = None,
    set_webhook_retries: int = 12,
    set_webhook_retry_timeout: float = 5.0,
) -> FastAPI:
    """Create and configure the FastAPI application."""
    if not container:
        container = ApplicationContainer()
        container.config.from_dict(
            {
                "log_level": os.environ.get("LOG_LEVEL", "info"),
                "log_format": os.environ.get("LOG_FORMAT", "json"),
                "log_file": os.environ.get("LOG_FILE"),
                "service_name": "webhook",
            }
        )
        container.logging()

    @contextlib.asynccontextmanager
    async def lifespan(app: FastAPI) -> "AsyncGenerator[None, None]":
        logger.info("On startup event...")

        # Start background task
        mduck: MDuckService = container.mduck()
        asyncio.create_task(run_mduck_processor(mduck))
        logger.info("MDuckService background processor started.")

        # Setup webhook
        host: str = container.config.tg.webhook.host()
        key: str = container.config.tg.webhook.key()
        secret: str = container.config.tg.webhook.secret()
        bot: aiogram.Bot = container.gateways.bot()
        dp: aiogram.Dispatcher = container.dispatcher()

        webhook_url = f"{host}/webhook/{key}"
        for i in range(1, set_webhook_retries):
            logger.info("Setting webhook URL %s", webhook_url)
            try:
                is_set = await bot.set_webhook(
                    url=webhook_url,
                    allowed_updates=dp.resolve_used_update_types(),
                    drop_pending_updates=True,
                    secret_token=secret,
                )
                if is_set:
                    logger.info("Webhook set up successful.")
                    break
                else:
                    logger.warning(
                        f"Webhook setup failed, attempt: {i}, retrying in 5 seconds..."
                    )
            except Exception:
                logger.error(
                    "Unexpected error while setting webhook URL", exc_info=True
                )
            finally:
                await asyncio.sleep(set_webhook_retry_timeout)
        else:
            raise RuntimeError("Webhook setup failed.")
        yield
        logger.info("On shutdown event...")

        # Remove webhook
        logger.info("Removing webhook...")
        await bot.delete_webhook()
        logger.info("Webhook removed.")

    app = FastAPI(version=__version__, lifespan=lifespan)
    app.state.container = container
    app.include_router(healthcheck.router)
    app.include_router(webhook.router)
    app.include_router(whoami.router)

    return app


def main() -> None:
    """Parse arguments and run the application."""
    parser = argparse.ArgumentParser(description="Run the FastAPI application.")
    parser.add_argument(
        "--host", type=str, default="0.0.0.0", help="Host address to bind to."
    )
    parser.add_argument("--port", type=int, default=8000, help="Port to listen on.")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reloading.")
    parser.add_argument(
        "--log-level",
        type=str,
        default="info",
        help="Log level.",
        choices=["critical", "error", "warning", "info", "debug", "trace"],
    )
    parser.add_argument(
        "--log-format",
        type=str,
        default="json",
        help="Log format.",
        choices=["human", "json"],
    )
    parser.add_argument("--log-file", type=str, help="Log file path.")
    parser.add_argument(
        "--forwarded-allow-ips",
        type=str,
        default="192.168.1.*,192.168.2.*",
        help="Comma-separated list of trusted proxy IPs.",
    )

    args = parser.parse_args()
    os.environ["LOG_LEVEL"] = args.log_level
    os.environ["LOG_FORMAT"] = args.log_format
    if args.log_file:
        os.environ["LOG_FILE"] = args.log_file

    uvicorn_params = {
        "app": "mduck.main.webhook:create_app",
        "host": args.host,
        "port": args.port,
        "reload": args.reload,
        "proxy_headers": True,
        "forwarded_allow_ips": args.forwarded_allow_ips,
        "log_config": None,
        "factory": True,
    }

    if args.reload:
        uvicorn_params["reload_dirs"] = ["src"]

    uvicorn.run(**uvicorn_params)


if __name__ == "__main__":  # pragma: no cover
    main()
