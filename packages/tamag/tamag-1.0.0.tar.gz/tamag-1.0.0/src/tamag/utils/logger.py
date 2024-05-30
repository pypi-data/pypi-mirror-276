"""
Module: logging_utils
Description: Contains utility classes for handling logging in this package.
"""

import logging
import warnings

class VerboseLogger:
    """
    Logger class for handling verbose output.
    """
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.logger = logging.getLogger(__name__)
        if self.verbose:
            logging.basicConfig(level=logging.INFO)

    def info(self, message):
        if self.verbose:
            self.logger.info(message)

    def warn(self, message, warning_class=UserWarning,stacklevel=1):
        if self.verbose:
            self.logger.warning(message, stacklevel=stacklevel+1)
        if warning_class:
            warnings.warn(message, warning_class, stacklevel=stacklevel+1)

    def error(self, message):
        self.logger.error(message)

    def log(self, level, message):
        if self.verbose or level in [logging.WARNING, logging.ERROR]:
            self.logger.log(level, message)

