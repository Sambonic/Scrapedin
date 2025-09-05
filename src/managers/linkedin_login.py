from src.config.common_imports import *
from src.config.config import LINKEDIN_LOGIN, HOMEPAGE_URL, HEADERS, WAIT
from src.utils.cookies import *
from src.config.path_config import path_manager
from src.managers.logger_manager import logger

class LinkedInLogin:
    """Handles LinkedIn login using email and password. Manages cookies for persistent sessions."""

    def __init__(self, email: str, password: str = None):
        self.session = requests.Session()
        self.email = email
        self.password = password
        self._login()

    def _update_session(self, cookies) -> None:
        """Update session details once cookies are acquired."""
        if isinstance(cookies, list) and all(isinstance(c, dict) for c in cookies):
            cookies = {c['name']: c['value'] for c in cookies} 
        self.session.cookies.update(cookies)
        HEADERS.update({'Csrf-Token': self.session.cookies.get('JSESSIONID').strip('"')})
        self.session.headers.update(HEADERS)

    def _set_driver(self):
        driver = webdriver.Firefox()
        driver.get(LINKEDIN_LOGIN)
        return driver

    def _login_request(self) -> None:
        """Login and save cookies."""
        try:
            html = self.session.get(HOMEPAGE_URL, headers=HEADERS).content
            soup = BeautifulSoup(html, "html.parser")
            csrf = soup.find("input", {"name": "loginCsrfParam"})["value"]

            login_information = {
                'session_key': self.email,
                'session_password': self.password,
                'loginCsrfParam': csrf,
            }

            response = self.session.post(LINKEDIN_LOGIN, data=login_information, headers=HEADERS)
            response_url = response.url

            if '/feed' not in response_url:
                raise ValueError("Not expected URL response")
            
            self._save_and_update_cookies(self.session.cookies)
            logger.info(f"User '{self.email}' logged in successfully via requests.")

        except (requests.RequestException, ValueError) as e:
            logger.error(f"Error during requests-based login: {e}. Falling back to Selenium.")
            self._login_selenium()

    def _login_selenium(self) -> None:
        """Login using Selenium to handle CAPTCHA and other challenges."""
        driver = self._set_driver()

        try:
            email_field = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.ID, 'session_key')))
            pass_field = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.ID, 'session_password')))
            email_field.send_keys(self.email)
            pass_field.send_keys(self.password)
            pass_field.submit()

            WebDriverWait(driver, 10).until(EC.url_contains('/feed'))
            
            cookies = driver.get_cookies()
            self._save_and_update_cookies(cookies)
            logger.info(f"User '{self.email}' logged in successfully via Selenium.")

        except TimeoutException:
            logger.error("Selenium login failed. User input may be required for a challenge.")
            logger.info("Please complete the login manually in the browser and then re-run the script.")
        
        finally:
            driver.quit()

    def _save_and_update_cookies(self, cookies):
        """Saves cookies and updates the session."""
        path_manager.create_user_file(self.email)
        write_cookies(cookies)
        self._update_session(cookies=cookies)
        logger.info(f"User '{self.email}' created successfully.")


    def _load_cookies(self) -> None:
        """Load cookies from a file to log in."""
        path_manager.create_user_file(self.email)
        cookies = read_cookies()
        if not cookies:
            logger.error(f"File for user '{self.email}' not found.")
            return

        self._update_session(cookies=cookies)

        logger.info("Logged in successfully!")
        time.sleep(WAIT)

    def _login(self) -> None:
        """Log in to LinkedIn. Load or create cookies as needed."""
        exists, _ = path_manager.check_path_exists(path_manager.USERS_DIR, self.email, ".pkl")
        if not exists:
            if self.password is None:
                logger.error("User not found. Login requires both email and password.")
            else:
                logger.info("First login detected.")
                self._login_request()
        else:
            logger.info(f"Email '{self.email}' exists. Proceeding to login...")
            self._load_cookies()