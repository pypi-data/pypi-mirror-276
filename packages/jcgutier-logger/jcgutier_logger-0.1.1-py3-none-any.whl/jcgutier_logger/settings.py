#!/usr/bin/env python

"""Config for this app"""

import os

# Logging settings
LOG_LEVEL = os.getenv("LOGLEVEL", "INFO")
LOG_FILENAME = (
    f"/tmp/{os.path.basename(os.path.dirname(os.path.realpath(__file__)))}.log"
)
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": (
                "%(asctime)s %(name)s %(filename)s:%(lineno)d %(levelname)-8s "
                " %(message)s"
            )
        },
        "long": {
            "format": (
                "%(asctime)s %(name)s %(module)s.%(funcName)s "
                "%(filename)s:%(lineno)d %(levelname)-8s  %(message)s"
            )
        },
    },
    "root": {"handlers": ["log_file", "console"], "level": LOG_LEVEL},
    "loggers": {
        "botocore": {
            "level": "CRITICAL",
            "handlers": ["log_file"],
            "propagate": "no",
        },
        "urllib3": {
            "level": "CRITICAL",
            "propagate": "no",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": LOG_LEVEL,
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
        "log_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "long",
            "filename": LOG_FILENAME,
            "maxBytes": 10485760,
            "backupCount": 2,
            "encoding": "utf8",
        },
    },
}
