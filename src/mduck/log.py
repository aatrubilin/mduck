import logging
import logging.config
import sys
from contextlib import contextmanager
from contextvars import ContextVar
from pathlib import Path
from typing import Iterator

from pythonjsonlogger.json import JsonFormatter

service_name_var: ContextVar[str] = ContextVar("service_name", default="")
chat_id_var: ContextVar[str] = ContextVar("chat_id", default="")
user_id_var: ContextVar[str] = ContextVar("user_id", default="")
update_id_var: ContextVar[str] = ContextVar("update_id", default="")

logger = logging.getLogger("mduck")


class ContextFilter(logging.Filter):
    """Injects context variables into the log record."""

    def filter(self, record: logging.LogRecord) -> bool:
        """Inject context variables into the log record."""
        record.service_name = service_name_var.get() or None
        record.chat_id = chat_id_var.get() or None
        record.user_id = user_id_var.get() or None
        record.update_id = update_id_var.get() or None
        return True


@contextmanager
def init_logging(
    log_level: str = "INFO",
    log_format: str = "human",
    service_name: str = "undefined",
    log_file: str | None = None,
) -> Iterator[None]:
    """Initialize logging using dictConfig."""
    service_name_var.set(service_name)
    log_level = log_level.upper()

    filters = {
        "context_filter": {
            "()": "mduck.log.ContextFilter",
        }
    }

    formatters = {
        "json": {
            "()": JsonFormatter,
            "format": (
                "%(asctime)s %(levelname)s %(name)s %(service_name)s "
                "%(update_id)s %(chat_id)s %(user_id)s %(message)s"
            ),
            "rename_fields": {
                "asctime": "timestamp",
                "levelname": "level",
                "name": "logger_name",
            },
        },
        "human": {
            "format": (
                "%(asctime)s - %(levelname)-8s - %(service_name)s - "
                "%(update_id)s - %(chat_id)s - %(user_id)s - "
                "%(name)s - %(message)s"
            ),
        },
    }

    handlers = {
        "default": {
            "formatter": log_format,
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "filters": ["context_filter"],
        }
    }

    if log_file:
        log_file_path = Path(log_file)
        if log_file_path.is_dir():
            log_file_path = log_file_path / "mduck.log"
        log_file_path.parent.mkdir(parents=True, exist_ok=True)

        handlers["file"] = {
            "formatter": log_format,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": log_file,
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "filters": ["context_filter"],
        }

    logger_handlers = ["default"]
    if log_file:
        logger_handlers.append("file")

    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": filters,
        "formatters": formatters,
        "handlers": handlers,
        "loggers": {
            "mduck": {
                "handlers": logger_handlers,
                "level": log_level,
                "propagate": False,
            },
            "aiogram": {
                "handlers": logger_handlers,
                "level": log_level,
                "propagate": False,
            },
            "uvicorn": {
                "handlers": logger_handlers,
                "level": log_level,
                "propagate": False,
            },
            "uvicorn.error": {
                "handlers": logger_handlers,
                "level": log_level,
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": logger_handlers,
                "level": log_level,
                "propagate": False,
            },
        },
    }
    logging.config.dictConfig(LOGGING_CONFIG)
    yield
