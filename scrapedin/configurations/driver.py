from scrapedin.configurations.common_imports import *


class Driver:
    """
    Initializes a WebDriver instance with desired options and configures logging.

    Attributes:
        driver (WebDriver): The instantiated WebDriver object.
        wait (WebDriverWait): A WebDriverWait object for handling asynchronous operations.
        path (str): The base path of the project directory.
        logger (Logger): A configured logger object for logging messages.
    """

    def __init__(self) -> None:
        self.driver: WebDriver = self._set_driver()
        self.wait: WebDriverWait = WebDriverWait(self.driver, 1)
        self.path: str = self._set_path()
        self.logger: Logger = self._set_logger()

    def _set_driver(self) -> WebDriver:
        """
        Creates and configures a Chrome WebDriver instance with desired options.

        Returns:
            WebDriver: The initialized Chrome WebDriver object.
        """
        chrome_options: Options = Options()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--no-sandbox")
        
        driver: WebDriver = webdriver.Chrome(options=chrome_options)
        return driver

    def _set_logger(self) -> Logger:
        """
        Configures a logger object with file and console handlers.

        Returns:
            Logger: The configured logger object.
        """
        current_time: datetime = datetime.now()
        file_date: str = current_time.strftime("%Y%m%d%H%M")

        # Create a logger
        logger: Logger = logging.getLogger('my_logger')
        logger.setLevel(DEBUG)

        # Set up file handler
        file_path: str = os.path.join(self.path, "logs")
        os.makedirs(file_path, exist_ok=True)
        file_path = os.path.join(file_path, f"log{file_date}.txt")
        file_handler: FileHandler = logging.FileHandler(file_path, encoding='utf-8')
        file_handler.setLevel(INFO)

        # Set up console handler
        console_handler: StreamHandler = logging.StreamHandler()
        console_handler.setLevel(DEBUG)

        # Create a formatter and add it to the handlers
        formatter: Formatter = logging.Formatter('[%(asctime)s] - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    def _set_path(self) -> str:
        """
        Retrieves the base path of the project directory.

        Returns:
            str: The base path of the project directory.
        """
        current_file_path: str = os.path.abspath(__file__)
        current_directory: str = os.path.dirname(current_file_path)
        parent_directory: str = os.path.dirname(current_directory)
        super_directory: str = os.path.dirname(parent_directory)
        return super_directory