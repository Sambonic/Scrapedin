from scrapedin.config.common_imports import logging
from scrapedin.config.path_config import path_manager

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

    def _initialize_logger(self) -> None:
        """Initializes and configures the logger instance."""
        self.logger = self._create_logger()

    def _create_logger(self) -> logging.Logger:
        """
        Creates and configures a logger instance with file and console handlers.
        """
        logger = logging.getLogger('my_logger')
        logger.setLevel(logging.DEBUG)

        # Create formatter
        formatter = logging.Formatter('[%(asctime)s] - %(levelname)s - %(message)s')

        # File handler for INFO level logs
        file_handler = logging.FileHandler(path_manager.LOG_FILE_DIR, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        # Console handler for DEBUG level logs
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    def _get_logger(self) -> logging.Logger:
        """
        Returns the configured logger instance.
        """
        return self.logger

# Initialize the global logger instance
logger = LoggerManager()._get_logger()