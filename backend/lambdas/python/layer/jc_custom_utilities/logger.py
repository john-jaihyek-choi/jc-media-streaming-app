import os, json
import logging
from logging import Logger
from dotenv import load_dotenv

# Load env variable
load_dotenv()

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
level_val = getattr(logging, log_level, logging.INFO)

# Set up the logging configuration with the desired format
config = {
    "level": level_val,
    "format": "|    %(asctime)s    |    %(name)s    |    %(filename)s:%(lineno)s    |\n"
    "%(levelname)s: %(message)s\n",
    "handlers": [logging.StreamHandler()],  # Also logs to console
}


def logger_config(name: str) -> Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level_val)

    # Clear any existing handlers to avoid duplicates
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create a stream handler (console)
    stream_handler = logging.StreamHandler()
    # Apply the CustomFormatter with your existing format
    formatter = CustomFormatter(config["format"])
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


class CustomFormatter(logging.Formatter):
    def format(self, record):
        # Check if the message is a dictionary or list
        if isinstance(record.msg, (dict, list)):
            # Convert it to a JSON string with indentation
            record.msg = json.dumps(record.msg, indent=4)

        # Use the base Formatter to format everything else
        return super().format(record)
