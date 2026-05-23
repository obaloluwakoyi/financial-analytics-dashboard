# logger.py
import logging
import sys


LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | "
    "%(name)s | %(filename)s:%(lineno)d | %(message)s"
)


def setup_logging(level: int = logging.INFO) -> None:
    root = logging.getLogger()
    root.setLevel(level)

    # Clear existing handlers (critical)
    root.handlers.clear()

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.INFO)
    stdout_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.ERROR)
    stderr_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    root.addHandler(stdout_handler)
    root.addHandler(stderr_handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"enterprise.{name}")