from scrapedin.configurations.common_imports import *
from scrapedin.configurations.driver import Driver


class LinkedInLogin(Driver):
    """
    Initialize the LinkedInLogin instance and perform login.

    Args:
        email (str): Email address of the LinkedIn account.
        password (str, optional): Password of the LinkedIn account. Defaults to None.
    """
    def __init__(self, email: str, password: str = None):
        super().__init__()
        self.login(email, password)

    def _load_cookies(self, root_dir: str, email: str) -> None:
        """
        Load cookies from a file and use them to log in to LinkedIn.

        Args:
            root_dir (str): Path to the cookies file.
            email (str): Email address of the LinkedIn account.
        """
        try:
            with open(root_dir, 'rb') as file:
                serialized_cookies = file.read()
        except FileNotFoundError:
            self.logger.error(f"File {root_dir} not found.")
            return

        cookies = pickle.loads(serialized_cookies)
        try:
            self.driver.get("https://www.linkedin.com/")
        except TimeoutException:
            self.driver.refresh()

        # Clear existing cookies before adding the loaded cookies
        self.driver.delete_all_cookies()
        for cookie in cookies:
            self.driver.add_cookie(cookie)

        self.driver.refresh()
        self.logger.info("Logged in successfully!")
        time.sleep(5)

    def _create_cookies(self, root_dir: str, email: str, password: str) -> str:
        """
        Create new cookies for a new email and save them to a file.

        Args:
            root_dir (str): Path to save the cookies file.
            email (str): Email address of the LinkedIn account.
            password (str): Password of the LinkedIn account.

        Returns:
            str: Path to the saved cookies file.
        """
        try:
            email_field = self.wait.until(
                EC.presence_of_element_located((By.ID, 'session_key'))
            )
            pass_field = self.wait.until(
                EC.presence_of_element_located((By.ID, 'session_password'))
            )
            email_field.send_keys(email)
            pass_field.send_keys(password)
        except TimeoutException:
            email_field = self.wait.until(
                EC.presence_of_element_located((By.ID, 'email-or-phone'))
            )
            pass_field = self.wait.until(
                EC.presence_of_element_located((By.ID, 'password'))
            )
            email_field.send_keys(email)
            pass_field.send_keys(password)

        sign_in = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
        )
        sign_in.click()

        time.sleep(2)
        self.driver.get("https://www.linkedin.com/")

        # Check for login errors
        try:
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="error-for-username"]'))
            )
            self.logger.error("Your email or password is incorrect. Please try again.")
            self.driver.quit()
            sys.exit()
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            self.logger.info("Creating new user. . .")

        # Save cookies
        time.sleep(1)
        cookies = self.driver.get_cookies()
        serialized_cookies = pickle.dumps(cookies)
        try:
            with open(root_dir, 'wb') as file:
                file.write(serialized_cookies)
        except IOError:
            self.logger.exception(f"Failed to write cookies to file: {root_dir}")

        self.logger.info(f"User '{email}' created successfully.")
        return root_dir

    def login(self, email: str, password: str = None) -> None:
        """
        Log in to LinkedIn using email and password. Create and load cookies as needed.

        Args:
            email (str): Email address of the LinkedIn account.
            password (str, optional): Password of the LinkedIn account. Defaults to None.
        """
        # Create 'users' folder if it doesn't exist
        file_path = os.path.join(self.path, "users")
        os.makedirs(file_path, exist_ok=True)

        root_dir = os.path.join(file_path, f"{email}.pkl")

        self.logger.info(f"Directory: {root_dir}")
        self.driver.get("https://www.linkedin.com/")

        if not os.path.exists(root_dir):
            if password is None:
                self.logger.error("User not found. Login with both email and password")
                self.driver.quit()
                sys.exit()
            else:
                self.logger.info("First login. Proceeding to create log file for new user...")
                cookies_path = self._create_cookies(root_dir, email, password)
                self._load_cookies(cookies_path, email)
        else:
            self.logger.info(f"Email '{email}' exists. Proceeding to login...")
            self._load_cookies(root_dir, email)