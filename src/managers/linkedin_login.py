from src.config.common_imports import *
from src.config.config import LINKEDIN_LOGIN, WAIT
from src.managers.driver_manager import DriverManager
from src.utils.file_operations import *
from src.config.path_config import path_manager
from src.managers.logger_manager import logger

class LinkedInLogin:
    """Handles LinkedIn login using email and password. Manages cookies for persistent sessions."""

    def __init__(self, email: str, password: str = None):
        self.session = requests.Session()
        self.driver = DriverManager()._get_driver()
        self.email = email
        self.password = password
        self._login()

    def _update_session(self, cookies) -> None:
        """Update session details once cookies are acquired."""

        for cookie in cookies:
            self.session.cookies.set(cookie['name'], cookie['value'])

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'X-Restli-Protocol-Version': '2.0.0',
            'Csrf-Token': self.session.cookies.get('JSESSIONID').strip('"'),
        }
        self.session.headers.update(headers)


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
            logger.error("Timeout during login.")
            return

        time.sleep(WAIT)
        cookies = self.driver.get_cookies()
        self._update_session(cookies=cookies)

        write_cookies(cookies)
        logger.info(f"User '{self.email}' created successfully.")

    def _load_cookies(self) -> None:
        """Load cookies from a file to log in."""
        cookies = read_cookies()
        if not cookies:
            logger.error(f"File for user '{self.email}' not found.")
            return

        self._update_session(cookies=cookies)

        logger.info("Logged in successfully!")
        time.sleep(WAIT)

    def _login(self) -> None:
        """Log in to LinkedIn. Load or create cookies as needed."""

        self.driver.get(LINKEDIN_LOGIN)
        exists, _ = path_manager.check_path_exists(path_manager.USERS_DIR, self.email, ".pkl")
        path_manager.create_user_file(self.email)

        if not exists:
            if self.password is None:
                logger.error("User not found. Login requires both email and password.")
            else:
                logger.info("First login. Creating a log file for the new user...")
                self._create_cookies()
        else:
            logger.info(f"Email '{self.email}' exists. Proceeding to login...")
            self._load_cookies()

        self.driver.quit()