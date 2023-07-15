from Scrapedin.common_imports import *
from Scrapedin.job_listing import JobListing
from Scrapedin.driver import Driver


class LinkedInScraper(Driver):
    def __init__(self):
        super().__init__()

    # Load cookies if email already exists
    def _load_cookies(self, rt_dir, email):
        try:
            with open(rt_dir, 'rb') as file:
                serialized_cookies = file.read()
        except FileNotFoundError:
            self.logger.error(f"File {rt_dir} not found.")
            return

        cookies = pickle.loads(serialized_cookies)
        try:
            self.driver.get("https://www.linkedin.com/")
        except (TimeoutException, MaxRetryError):
            self.driver.refresh()

        for cookie in cookies:
            self.driver.add_cookie(cookie)

        self.driver.refresh()
        self.logger.info("Logged in successfully!")

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

            sign_in = self.driver.find_element(
                By.XPATH, "//button[@type='submit']")
            sign_in.click()

        except TimeoutException:
            self.driver.refresh()

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

        root_dir = os.path.join(self.path, "users", f"{email}.pkl")

        self.logger.info(f"Directory: {root_dir}")

        self.driver.get("https://www.linkedin.com/?original_referer=")

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
            self.logger.info(f"email '{email}' exists. Proceeding to login...")
            self._load_cookies(root_dir, email)

    # Start measuring time and space complexities
    def _benchmarking(self, links):
        # Measure Time Complexity
        start_time = time.time()

        # Get the starting time
        current_time = datetime.now()
        starting_time = current_time.strftime("%H:%M:%S")

        # Code profiling
        profiler = cProfile.Profile()
        profiler.enable()

        # Function calls to be profiled
        self._gather_info(links)

        profiler.disable()

        end_time = time.time()
        execution_time = end_time - start_time

        # Measure Space Complexity
        process = psutil.Process()
        memory_usage = process.memory_info().rss

        # Get the finishing time
        current_time = datetime.now()
        finishing_time = current_time.strftime("%H:%M:%S")

        self.logger.info(f"Starting time: {starting_time}")
        self.logger.info(f"Finishing time: {finishing_time}")
        self.logger.info(f"Time elapsed: {execution_time} seconds")
        self.logger.info(f"Memory usage: {memory_usage} bytes")
        profiler.print_stats()

    # Begin extracting data from gathered links
    def _gather_info(self, jobs_gathered):
        for job_url in jobs_gathered:
            self.driver.get(job_url)
            time.sleep(0.3)
            try:
                job_listing = JobListing(
                    self.driver, self.wait, self.logger, self.csv_file_name, self.path)
                job_listing._add_to_csv()
                job_listing._display_details()

            except TimeoutException:
                self.logger.error("Timeout occurred. Reloading the page...")
                self.driver.refresh()

    # Scrape all links available of said job role
    def scrape(self, role, location=None, page_number=0):
        links = []
        self.wait = WebDriverWait(self.driver, 20)

        if location is None:
            role_job_listings = f"https://www.linkedin.com/jobs/search/?keywords={role}&start={page_number}"
        else:
            role_job_listings = f"https://www.linkedin.com/jobs/search/?keywords={role}&start={page_number}&location={location}"

        self.driver.get(role_job_listings)

        # Create file name where info will be stored
        role_name = role.replace(" ", "")
        self.csv_file_name = self._set_csv_file_name(role_name)

        # Find and retrieve the total number of results
        try:
            results = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'jobs-search-results-list__subtitle')]/span")))
            span_text = results.text
            total_results = int(''.join(filter(str.isdigit, span_text)))
        except NoSuchElementException:
            self.driver.refresh()

        # Loop through all the job listings
        while page_number <= total_results:
            time.sleep(1.2)

            try:
                ul_element = self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//ul[contains(@class,'scaffold-layout__list-container')]")))
            except TimeoutException:
                # No more job listings
                break

            # Gather job listing URLs
            link_elements = ul_element.find_elements(By.TAG_NAME, "li")
            time.sleep(0.2)

            for element in link_elements:
                try:
                    link_id = element.get_attribute("data-occludable-job-id")
                    if link_id is not None:
                        link = f"https://www.linkedin.com/jobs/search/?currentJobId={link_id}"
                        self.logger.info(link)
                        links.append(link)
                except StaleElementReferenceException:
                    continue

            self.logger.info(
                f"Job listings gathered: {len(links)} / {total_results}")

            # Update values
            page_number += 25
            if location is None:
                role_job_listings = f"https://www.linkedin.com/jobs/search/?keywords={role}&start={page_number}"
            else:
                role_job_listings = f"https://www.linkedin.com/jobs/search/?keywords={role}&start={page_number}&location={location}"

            self.driver.get(role_job_listings)

        for i, link in enumerate(links):
            self.logger.info(f"[{i + 1}]: {link}")

        # Print the total number of links
        self.logger.info("Total number of links: %s", len(links))

        # Send links for processing
        self._benchmarking(links)
