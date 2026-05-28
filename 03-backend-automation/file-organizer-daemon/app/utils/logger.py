import logging
import sys

def get_logger(name: str) -> logging.Logger:
    """
    Creates and configures a logger for runtime logging.

    Designed for filesystem monitoring / daemon-style applications
    where consistent, structured console logs are required.
    """
    
    # Get (or create) a logger with the given name
    logger = logging.getLogger(name)

    # Prevent adding duplicate handlers if logger already exists
    if not logger.handlers:

        # Set logging level to INFO (captures info, warnings, errors)
        logger.setLevel(logging.INFO)

        # Define log message format
        # Includes timestamp, log level, logger name, and message
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Create console handler to output logs to stdout
        ch = logging.StreamHandler(sys.stdout)

        # Attach formatter to console handler
        ch.setFormatter(formatter)

        # Add handler to logger
        logger.addHandler(ch)

    # Return configured logger instance
    return logger