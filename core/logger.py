import os
from datetime import datetime
from core.config import LOG_PATH


class Logger:

    def __init__(self):
        os.makedirs(LOG_PATH, exist_ok=True)

        self.log_file = os.path.join(
            LOG_PATH,
            "umbra.log"
        )

    def log(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted = f"[{timestamp}] {message}"

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")

        print(formatted)


_logger = Logger()


def log(message: str):
    _logger.log(message)