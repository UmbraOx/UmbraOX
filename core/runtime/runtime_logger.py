import logging
import os
from datetime import datetime

_LOG_DIR = os.path.join(os.getcwd(), "sessions", "logs")


def get_logger(name="umbra_runtime", level=None):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    log_level = level or os.environ.get("UMBRA_LOG_LEVEL", "INFO")
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(numeric_level)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console = logging.StreamHandler()
    console.setLevel(numeric_level)
    console.setFormatter(formatter)
    logger.addHandler(console)

    try:
        os.makedirs(_LOG_DIR, exist_ok=True)
        log_file = os.path.join(
            _LOG_DIR,
            f"umbra_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception:
        pass

    return logger


class UmbraLogger:

    def __init__(self, name="umbra_runtime"):
        self._logger = get_logger(name)

    def info(self, msg):
        self._logger.info(msg)

    def warning(self, msg):
        self._logger.warning(msg)

    def error(self, msg):
        self._logger.error(msg)

    def debug(self, msg):
        self._logger.debug(msg)

    def critical(self, msg):
        self._logger.critical(msg)