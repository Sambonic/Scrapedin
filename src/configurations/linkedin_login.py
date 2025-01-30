from src.configurations.common_imports import *
from src.configurations.config import (LINKEDIN_LOGIN, WAIT)
from src.configurations.driver_manager import DriverManager
from src.configurations.logger_manager import LoggerManager
from src.configurations.path_manager import PathManager
from src.configurations.file_manager import FileManager

class LinkedInLogin:
    """Handles LinkedIn login using email and password. Manages cookies for persistent sessions."""

    def __init__(self, email: str, password: str = None):
        self.path = PathManager()
        self.session = requests.Session()
        self.logger = LoggerManager().get_logger()
        
        self.file_manager = FileManager(self.path)
        self.driver = DriverManager().get_driver()
        
        self.email = email
        self.password = password
        self.login()

    def _create_cookies(self) -> None:
        """Create and save cookies for a new login."""
        try:
            email_field = WebDriverWait(self.driver, WAIT).until(
                EC.presence_of_element_located((By.ID, 'username'))
            )
            pass_field = WebDriverWait(self.driver, WAIT).until(
                EC.presence_of_element_located((By.ID, 'password'))
            )
            email_field.send_keys(self.email)
            pass_field.send_keys(self.password)
            pass_field.submit()
        except TimeoutException:
            self.logger.error("Timeout during login.")
            return

        time.sleep(WAIT)
        cookies = self.driver.get_cookies()
        self.file_manager.write_cookies(self.email, cookies)
        self.logger.info(f"User '{self.email}' created successfully.")

    def _load_cookies(self) -> None:
        """Load cookies from a file to log in."""
        cookies = self.file_manager.read_cookies(self.email)
        if not cookies:
            self.logger.error(f"File for user '{self.email}' not found.")
            return

        for cookie in cookies:
            self.session.cookies.set(cookie['name'], cookie['value'])

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'X-Restli-Protocol-Version': '2.0.0',
            'Csrf-Token': self.session.cookies.get('JSESSIONID').strip('"'),
        }
        self.session.headers.update(headers)

        self.logger.info("Logged in successfully!")
        time.sleep(WAIT)

    def login(self) -> None:
        """Log in to LinkedIn. Load or create cookies as needed."""
        cookie_path = self.path.get_user_cookie_path(self.email)
        self.logger.info(f"Directory: {cookie_path}")
        self.driver.get(LINKEDIN_LOGIN)

        if not self.path.file_exists(self.email):
            if self.password is None:
                self.logger.error("User not found. Login requires both email and password.")
            else:
                self.logger.info("First login. Creating a log file for the new user...")
                self._create_cookies(self.email, self.password)
        else:
            self.logger.info(f"Email '{self.email}' exists. Proceeding to login...")
            self._load_cookies()

        self.driver.quit()