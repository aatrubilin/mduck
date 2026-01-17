import argparse
import asyncio
import logging

from aiogram import Bot, Dispatcher

from mduck.containers.application import ApplicationContainer
from mduck.services.mduck import MDuckService

logger = logging.getLogger("mduck")


async def run_mduck_processor(mduck: MDuckService) -> None:
    """Run mduck processor."""
    while True:
        await mduck.process_message_from_queue()


async def start_pooling(container: ApplicationContainer | None = None) -> None:
    """Run pooling."""
    container = container or ApplicationContainer()
    dp: Dispatcher = container.dispatcher()
    bot: Bot = container.gateways.bot()

    mduck: MDuckService = container.mduck()
    asyncio.create_task(run_mduck_processor(mduck))
    logger.info("MDuckService background processor started.")

    await dp.start_polling(bot)


def main() -> None:
    """Start pooling."""
    parser = argparse.ArgumentParser(description="Run the FastAPI application.")
    parser.add_argument(
        "--log-level",
        type=str,
        default="info",
        help="Log level.",
        choices=["critical", "error", "warning", "info", "debug", "trace"],
    )

    args = parser.parse_args()

    logging.basicConfig(level=args.log_level.upper())
    asyncio.run(start_pooling())


if __name__ == "__main__":  # pragma: no cover
    main()
