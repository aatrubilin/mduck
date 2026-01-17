import argparse
import asyncio
import logging

from aiogram import Bot, Dispatcher

from mduck.containers.application import ApplicationContainer

logger = logging.getLogger("mduck")


async def start_pooling(container: ApplicationContainer | None = None) -> None:
    """Run pooling."""
    container = container or ApplicationContainer()
    dp: Dispatcher = container.dispatcher()
    bot: Bot = container.gateways.bot()
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
