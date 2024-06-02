#!/usr/bin/env python

"""
Set up logging for python script
"""

import logging.config

from jcgutier_logger.settings import LOGGING_CONFIG


class Logger:
    """Logging configuration"""

    def __init__(self, debug: bool) -> None:
        self.debug = debug
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel("DEBUG")

    def setup_logging(self) -> None:
        """Setup logging"""
        if self.debug:
            LOGGING_CONFIG["root"]["level"] = "DEBUG"
            LOGGING_CONFIG["handlers"]["console"]["level"] = "DEBUG"
            LOGGING_CONFIG["handlers"]["log_file"]["level"] = "DEBUG"
        logging.config.dictConfig(LOGGING_CONFIG)

    def get_logger(self) -> logging.Logger:
        """Get logger

        Returns:
            logging.Logger: Logger
        """
        return self.logger


if __name__ == "__main__":
    log = Logger(False)
    logger = log.get_logger()
    logger.info("Info log")
    logger.warning("Warning log")
    logger.critical("Critical log")
    logger.error("Error log")
    logger.debug("Debug log")
