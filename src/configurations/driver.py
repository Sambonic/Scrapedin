from src.configurations.common_imports import *


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
        self.driver = self._set_driver()
        self.wait = WebDriverWait(self.driver, 1)
        self.path = self._set_path()
        self.logger = self._set_logger()
        self.session = requests.Session()

    def _set_driver(self) -> WebDriver:
        """
        Creates and configures a Chrome WebDriver instance with desired options.

        Returns:
            WebDriver: The initialized Chrome WebDriver object.
        """
        chrome_options = Options()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--no-sandbox")
        
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def _set_logger(self) -> Logger:
        """
        Configures a logger object with file and console handlers.

        Returns:
            Logger: The configured logger object.
        """
        current_time = datetime.now()
        file_date = current_time.strftime("%Y%m%d%H%M")

        # Create a logger
        logger = logging.getLogger('my_logger')
        logger.setLevel(DEBUG)

        # Set up file handler
        file_path = os.path.join(self.path, "logs")
        os.makedirs(file_path, exist_ok=True)
        file_path = os.path.join(file_path, f"log{file_date}.txt")
        file_handler = logging.FileHandler(file_path, encoding='utf-8')
        file_handler.setLevel(INFO)

        # Set up console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(DEBUG)

        # Create a formatter and add it to the handlers
        formatter = logging.Formatter('[%(asctime)s] - %(levelname)s - %(message)s')
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
        current_file_path = os.path.abspath(__file__)
        current_directory = os.path.dirname(current_file_path)
        parent_directory = os.path.dirname(current_directory)
        super_directory = os.path.dirname(parent_directory)
        return super_directory