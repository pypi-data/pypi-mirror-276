import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name: str, log_file: str = None, level: int = logging.INFO, max_bytes: int = 10485760, backup_count: int = 5) -> logging.Logger:
    """
    Set up a logger with the specified name and level.
    Optionally, log to a file with rotation.

    :param name: Name of the logger.
    :param log_file: Path to the log file. If None, logs to console.
    :param level: Logging level.
    :param max_bytes: Maximum size of log file before rotation (default 10MB).
    :param backup_count: Number of backup files to keep (default 5).
    :return: Configured logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    if log_file:
        file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    else:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

def get_console_handler() -> logging.Handler:
    """
    Get a console handler with a standard formatter.

    :return: Configured console handler.
    """
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    return console_handler

def get_file_handler(log_file: str, max_bytes: int = 10485760, backup_count: int = 5) -> logging.Handler:
    """
    Get a file handler with a standard formatter.

    :param log_file: Path to the log file.
    :param max_bytes: Maximum size of log file before rotation (default 10MB).
    :param backup_count: Number of backup files to keep (default 5).
    :return: Configured file handler.
    """
    file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    return file_handler

def set_logger_level(logger: logging.Logger, level: int):
    """
    Set the logging level for a given logger.

    :param logger: Logger instance.
    :param level: Logging level.
    """
    logger.setLevel(level)

def add_handler(logger: logging.Logger, handler: logging.Handler):
    """
    Add a handler to the logger.

    :param logger: Logger instance.
    :param handler: Handler to add.
    """
    logger.addHandler(handler)

def remove_handler(logger: logging.Logger, handler: logging.Handler):
    """
    Remove a handler from the logger.

    :param logger: Logger instance.
    :param handler: Handler to remove.
    """
    logger.removeHandler(handler)