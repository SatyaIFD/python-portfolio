import logging
import sys


# ===================================================================
# Logger Utility
# ===================================================================
#
# This module provides a reusable standardized logger
# configuration for the application.
#
# Features:
# - Console logging to stdout
# - Timestamped log messages
# - Log level display
# - Component/module identification
# - Prevents duplicate handlers
#
# Example Usage:
#
#     logger = get_logger(__name__)
#
#     logger.info("Application started")
#     logger.error("Unexpected failure")
#
# Example Output:
#
#     2026-05-29 12:45:10 [INFO] app.core.engine:
#     Indexing started
#
# ===================================================================


def get_logger(name: str) -> logging.Logger:
    """
    Create and configure a standardized application logger.

    Args:
        name:
            Name of the logger.
            Typically use:
                __name__

    Returns:
        Configured logging.Logger instance
    """

    # ---------------------------------------------------------------
    # Retrieve existing logger instance (or create one)
    # ---------------------------------------------------------------
    logger = logging.getLogger(name)

    # ---------------------------------------------------------------
    # Prevent duplicate handlers
    # ---------------------------------------------------------------
    #
    # Without this check, importing the logger multiple times
    # may attach multiple console handlers and duplicate logs.
    #
    if not logger.hasHandlers():

        # Set minimum log level
        logger.setLevel(logging.INFO)

        # -----------------------------------------------------------
        # Define log message format
        # -----------------------------------------------------------
        #
        # Example:
        # 2026-05-29 12:00:00 [INFO] app.main: Server started
        #
        formatter = logging.Formatter(
            fmt='%(asctime)s [%(levelname)s] %(name)s: %(message)s',

            # Timestamp format
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # -----------------------------------------------------------
        # Configure console output handler
        # -----------------------------------------------------------
        #
        # Logs are printed to standard output (stdout)
        #
        console_handler = logging.StreamHandler(sys.stdout)

        # Apply formatting to console logs
        console_handler.setFormatter(formatter)

        # Attach handler to logger
        logger.addHandler(console_handler)

    # Return configured logger instance
    return logger