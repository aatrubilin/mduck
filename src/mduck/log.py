import logging
import logging.config
import sys
from contextlib import contextmanager
from contextvars import ContextVar
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

    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": filters,
        "formatters": formatters,
        "handlers": handlers,
        "loggers": {
            "mduck": {
                "handlers": ["default"],
                "level": log_level,
                "propagate": False,
            },
            "aiogram": {
                "handlers": ["default"],
                "level": log_level,
                "propagate": False,
            },
            "uvicorn": {
                "handlers": ["default"],
                "level": log_level,
                "propagate": False,
            },
            "uvicorn.error": {
                "handlers": ["default"],
                "level": log_level,
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["default"],
                "level": log_level,
                "propagate": False,
            },
        },
    }
    logging.config.dictConfig(LOGGING_CONFIG)
    yield
