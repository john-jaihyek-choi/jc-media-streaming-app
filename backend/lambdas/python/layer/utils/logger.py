import os, sys

if os.getenv("AWS_EXECUTION_ENV"):
    sys.path.append("/opt/python")
import logging
from logging import Logger
from dotenv import load_dotenv

# Load env variable
load_dotenv()

config = {
    "level": os.getenv("LOG_LEVEL"),
    "format": "|    %(asctime)s    |    %(name)s    |    %(filename)s:%(lineno)s    |\n"
    "%(levelname)s: %(message)s\n",
    "handlers": [
        # logging.FileHandler("app.log"),   # If need to log to a file
        logging.StreamHandler()  # Also logs to console
    ],
}


def logger_config(name: str) -> Logger:
    # Configures basic logging format and handlers
    logging.basicConfig(**config)

    return logging.getLogger(name)
