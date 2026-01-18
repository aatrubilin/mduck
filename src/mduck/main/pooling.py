import argparse
import asyncio
import logging
import subprocess
import sys
import time
from pathlib import Path
from typing import NoReturn

from aiogram import Bot, Dispatcher
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from mduck.containers.application import ApplicationContainer
from mduck.services.mduck import MDuckService

logger = logging.getLogger("mduck")

ROOT_PATH = Path(__file__).resolve().parent.parent.parent


class CodeChangeHandler(FileSystemEventHandler):
    """Handles file system events for code changes."""

    process: subprocess.Popen[bytes]

    def __init__(self) -> None:
        self.last_event_time = time.time()
        self.reload_process()

    def on_any_event(self, event: FileSystemEvent) -> None:
        """Reload the process on any file system event."""
        if time.time() - self.last_event_time < 1.0:
            return
        self.last_event_time = time.time()
        logger.info("Changes detected. Reloading...")
        self.reload_process()

    @staticmethod
    def reload_process() -> None:  # pragma: no cover
        """Kills the current process and starts a new one."""
        if (
            hasattr(CodeChangeHandler, "process")
            and CodeChangeHandler.process.poll() is None
        ):
            CodeChangeHandler.process.kill()
            CodeChangeHandler.process.wait()
        args = [sys.executable, "-m", "mduck.main.pooling"] + [
            arg for arg in sys.argv[1:] if arg != "--reload"
        ]
        CodeChangeHandler.process = subprocess.Popen(args)


def run_reloader() -> NoReturn:  # pragma: no cover
    """Monitor for code changes and reload the application."""
    logger.info("Starting reloader...")
    observer = Observer()
    observer.schedule(CodeChangeHandler(), str(ROOT_PATH), recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    sys.exit(0)


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
    parser = argparse.ArgumentParser(description="Run the pooling application.")
    parser.add_argument(
        "--log-level",
        type=str,
        default="info",
        help="Log level.",
        choices=["critical", "error", "warning", "info", "debug", "trace"],
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reloading.",
    )

    args = parser.parse_args()

    logging.basicConfig(level=args.log_level.upper())

    if args.reload:
        run_reloader()
    else:
        asyncio.run(start_pooling())


if __name__ == "__main__":  # pragma: no cover
    main()
