from src.config.common_imports import logging, datetime, os
from src.config.path_config import path_manager

class LoggerManager:
    """
    Manages the logger instance and provides access to it.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggerManager, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self):
        """Initializes the logger and sets it up."""
        self.logger = self._set_logger()

    def _get_logger(self) -> logging.Logger:
        """Returns the logger instance."""
        return self.logger

    def _set_logger(self) -> logging.Logger:
        """Configures and returns a logger instance."""
        logger = logging.getLogger('my_logger')
        logger.setLevel(logging.DEBUG)

        # Set up file handler
        file_handler = logging.FileHandler(path_manager.LOG_FILE_DIR, encoding='utf-8')
        file_handler.setLevel(logging.INFO)

        # Set up console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # Create a formatter and add it to the handlers
        formatter = logging.Formatter('[%(asctime)s] - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

# Initialize the global logger instance
logger = LoggerManager()._get_logger()
