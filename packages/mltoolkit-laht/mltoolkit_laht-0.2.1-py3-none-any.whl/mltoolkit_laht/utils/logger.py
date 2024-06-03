import logging
import os


class Logger:

    @staticmethod
    def setup_logger(name):
        # Create logs directory if it doesn't exist
        if not os.path.exists("logs"):
            os.makedirs("logs")

        # Get log level from environment variable or default to INFO
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()

        # Logger configuration
        logging_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": log_level,
                    "formatter": "standard",
                    "stream": "ext://sys.stdout",
                },
                "file": {
                    "class": "logging.FileHandler",
                    "level": log_level,
                    "formatter": "standard",
                    "filename": "logs/app.log",
                    "mode": "a",  # Append mode
                },
            },
            "loggers": {
                name: {
                    "handlers": ["console", "file"],
                    "level": log_level,
                    "propagate": False,
                },
            },
        }

        logging.config.dictConfig(logging_config)
        return logging.getLogger(name)
