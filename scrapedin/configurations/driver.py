from scrapedin.configurations.common_imports import *


class Driver:
    def __init__(self):
        self.driver = self._set_driver()
        self.wait = WebDriverWait(self.driver, 2.5)
        self.path = self._set_path()
        self.logger = self._set_logger()

    # Create and initialise driver according to preference

    def _set_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
        chrome_options.add_argument("--disable-dev-shm-usage")  # Disable /dev/shm usage
        chrome_options.add_argument("--no-sandbox")  # Disable sandboxing for better compatibility
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    # Instantiate file and console loggers to track during runtime
    def _set_logger(self):
        current_time = datetime.now()
        file_date = current_time.strftime("%Y%m%d%H%M")

        # Create a logger
        logger = logging.getLogger('my_logger')
        logger.setLevel(logging.DEBUG)

        file_path = os.path.join(self.path, "logs")
        os.makedirs(file_path, exist_ok=True)
        file_path = os.path.join(file_path, f"log{file_date}.txt")

        # Create a file handler and set its log level
        file_handler = logging.FileHandler(file_path, encoding='utf-8')
        file_handler.setLevel(logging.INFO)

        # Create a console handler and set its log level
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # Create a formatter and add it to the handlers
        formatter = logging.Formatter(
            '[%(asctime)s] - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add the handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    def _set_path(self):
        current_file_path = os.path.abspath(__file__)
        current_directory = os.path.dirname(current_file_path)
        parent_directory = os.path.dirname(current_directory)
        super_directory = os.path.dirname(parent_directory)
        return super_directory
