from src.configurations.common_imports import *
from src.configurations.driver import Driver

LINKEDIN_LOGIN = "https://www.linkedin.com/login"
WAIT = 1

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

    def _load_cookies(self, root_dir: str) -> None:
        """
        Load cookies from a file and use them to log in to LinkedIn.

        Args:
            root_dir (str): Path to the cookies file.
        """
        try:
            with open(root_dir, 'rb') as file:
                serialized_cookies = file.read()
        except FileNotFoundError:
            self.logger.error(f"File {root_dir} not found.")
            return

        cookies = pickle.loads(serialized_cookies)


        #=========================================================================
        #=========================================================================
        # Add the cookies to the session
        for cookie in cookies:
            self.session.cookies.set(cookie['name'], cookie['value'])

        # Set headers (mimic a real browser)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'X-Restli-Protocol-Version': '2.0.0',
            'Csrf-Token': self.session.cookies.get('JSESSIONID').strip('"'),
        }

        self.session.headers.update(headers)
        #=========================================================================
        #=========================================================================


        # Clear existing cookies before adding the loaded cookies
        self.driver.delete_all_cookies()
        for cookie in cookies:
            self.driver.add_cookie(cookie)

        self.driver.refresh()
        self.logger.info("Logged in successfully!")
        time.sleep(WAIT)

    def _create_cookies(self, root_dir: str, email: str, password: str) -> None:
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
                EC.presence_of_element_located((By.ID, 'username'))
            )
            pass_field = self.wait.until(
                EC.presence_of_element_located((By.ID, 'password'))
            )
            email_field.send_keys(email)
            pass_field.send_keys(password)

            pass_field.submit()
        except TimeoutException:
            pass
            # Revise the logic here

        # Save cookies
        time.sleep(WAIT)
        cookies = self.driver.get_cookies()
        serialized_cookies = pickle.dumps(cookies)
        try:
            with open(root_dir, 'wb') as file:
                file.write(serialized_cookies)
        except IOError:
            self.logger.exception(f"Failed to write cookies to file: {root_dir}")

        self.logger.info(f"User '{email}' created successfully.")

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

        # Get the the cookie file directory associated with email
        root_dir = os.path.join(file_path, f"{email}.pkl")

        self.logger.info(f"Directory: {root_dir}")
        self.driver.get(LINKEDIN_LOGIN)

        if not os.path.exists(root_dir):
            if password is None:
                self.logger.error("User not found. Login with both email and password")
                self.driver.quit()
                sys.exit()
            else:
                self.logger.info("First login. Creating a log file for the new user...")
                self._create_cookies(root_dir, email, password)

        else:
            self.logger.info(f"Email '{email}' exists. Proceeding to login...")
            self._load_cookies(root_dir)

    # NB. Add cookie validation function here