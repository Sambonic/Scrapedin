from scrapedin.configurations.common_imports import *
from scrapedin.configurations.driver import Driver


class LinkedInLogin(Driver):
    def __init__(self, email, password=None):
        super().__init__()
        self.login(email, password)

    # Load cookies if email already exists
    def _load_cookies(self, root_dir, email):
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

    # Create new cookies for new emails
    def _create_cookies(self, rt_dir, email, password):
        try:
            try:
                email_field = self.wait.until(
                    EC.presence_of_element_located((By.ID, 'session_key')))
                pass_field = self.wait.until(
                    EC.presence_of_element_located((By.ID, 'session_password')))
                email_field.send_keys(email)
                pass_field.send_keys(password)
            except:
                email_field = self.wait.until(
                    EC.presence_of_element_located((By.ID, 'email-or-phone')))
                pass_field = self.wait.until(
                    EC.presence_of_element_located((By.ID, 'password')))
                email_field.send_keys(email)
                pass_field.send_keys(password)

            sign_in = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))
            sign_in.click()

        except TimeoutException:
            self.driver.refresh()

        time.sleep(2)
        self.driver.get("https://www.linkedin.com/")
        # Check email and password
        error = False
        try:
            self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="error-for-username"]')))
            self.logger.error(
                "Your email or password is incorrect. Please try again")
            error = True
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            self.logger.info("Creating new user. . .")

        if error:
            self.driver.quit()
            sys.exit()

        # Create new cookies and store in associated folder

        time.sleep(1)
        cookies = self.driver.get_cookies()
        serialized_cookies = pickle.dumps(cookies)

        try:
            with open(rt_dir, 'wb') as file:
                file.write(serialized_cookies)
        except IOError:
            self.logger.exception(f"Failed to write cookies to file: {rt_dir}")

        self.logger.info(f"User '{email}' created successfully.")
        return rt_dir

    # Login
    def login(self, email, password=None):

        # Create 'Users' folder if it doesn't exist
        file_path = os.path.join(self.path, "users")
        os.makedirs(file_path, exist_ok=True)

        root_dir = os.path.join(self.path, "users", f"{email}.pkl")

        self.logger.info(f"Directory: {root_dir}")

        self.driver.get("https://www.linkedin.com/")

        if not os.path.exists(root_dir):
            try:
                if password is None:
                    self.logger.error(
                        f"User not found. Login with both email and password")
                    self.driver.quit()
                    sys.exit()

                else:
                    self.logger.info(
                        f"First login. Proceeding to create log file for new user...")
                    cookies_path = self._create_cookies(
                        root_dir, email, password)
                    self._load_cookies(cookies_path, email)

            except OSError as e:
                self.logger.error(
                    f"An error occurred while creating folder '{user}': {e}")
        else:
            self.logger.info(f"Email '{email}' exists. Proceeding to login...")
            self._load_cookies(root_dir, email)
