import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Ensure the logs directory exists relative to the project root
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Create our base logger
logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)
logger.propagate = False  # Prevent propagation to uvicorn's default loggers


# Formatter for console: no traceback details
class NoTracebackFormatter(logging.Formatter):
    def formatException(self, exc_info):
        return ""


# Filter to drop log records from uvicorn.error so that they don't duplicate in console
class UvicornErrorFilter(logging.Filter):
    def filter(self, record):
        # Exclude records from the uvicorn.error logger
        return not record.name.startswith("uvicorn.error")


# Console handler: DEBUG and above, without traceback details and filtered uvicorn errors
console_formatter = NoTracebackFormatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(console_formatter)
console_handler.addFilter(UvicornErrorFilter())

# File handler: INFO and above, with full traceback details
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler = RotatingFileHandler(
    filename=str(LOG_DIR / "app.log"),
    maxBytes=10 * 1024 * 1024,  # 10 MB
    backupCount=5,
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(file_formatter)

# Attach handlers to our base logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
