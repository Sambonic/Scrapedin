from src.configurations.common_imports import (logging,datetime,os)

class LoggerManager:
    """
    Manages the logger instance and provides access to it.
    """
    def __init__(self):
        self.logger = self._set_logger()

    def get_logger(self) -> logging.Logger:
        """Returns the logger instance."""
        return self.logger

    def _set_logger(self) -> logging.Logger:
        """Configures and returns a logger instance."""
        current_time = datetime.now()
        file_date = current_time.strftime("%Y%m%d%H%M")

        logger = logging.getLogger('my_logger')
        logger.setLevel(logging.DEBUG)

        # Set up file handler
        file_path = os.path.join(self.get_path(), "logs")
        os.makedirs(file_path, exist_ok=True)
        file_path = os.path.join(file_path, f"log{file_date}.txt")
        file_handler = logging.FileHandler(file_path, encoding='utf-8')
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
    
    def get_path(self) -> str:
        """Returns the base project directory path."""
        current_file_path = os.path.abspath(__file__)
        current_directory = os.path.dirname(current_file_path)
        parent_directory = os.path.dirname(current_directory)
        super_directory = os.path.dirname(parent_directory)
        return super_directory
