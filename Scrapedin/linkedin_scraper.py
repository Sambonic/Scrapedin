from Scrapedin.common_imports import *
from Scrapedin.job_listing import JobListing


class LinkedInScraper:
    def __init__(self):
        self.driver = self.initiate_driver()

    def initiate_driver(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome()
        self.path = ""
        return self.driver

    def set_driver(self, driver):
        if driver is not None:
            self.driver = driver
        else:
            raise ValueError("Driver cannot be None.")

    def get_driver(self):
        return self.driver

    def load_cookies(self, rt_dir, user):
        # Load the serialized cookies from the file
        with open(rt_dir, 'rb') as file:
            serialized_cookies = file.read()

        cookies = pickle.loads(serialized_cookies)
        self.driver.get("https://www.linkedin.com/")

        for cookie in cookies:
            self.driver.add_cookie(cookie)

        self.driver.refresh()
        print("Logged in successfully!")

    def create_cookies(self, rt_dir, user, password):
        wait = WebDriverWait(self.driver, 10)
        try:
            user_field = wait.until(
                EC.presence_of_element_located((By.ID, 'session_key')))
            pass_field = wait.until(
                EC.presence_of_element_located((By.ID, 'session_password')))
            user_field.send_keys(user)
            pass_field.send_keys(password)

            sign_in = self.driver.find_element(
                By.XPATH, "//button[@type='submit']")
            sign_in.click()

        except:
            user_field = wait.until(
                EC.presence_of_element_located((By.ID, 'email-or-phone')))
            pass_field = wait.until(
                EC.presence_of_element_located((By.ID, 'password')))
            user_field.send_keys(user)
            pass_field.send_keys(password)

            sign_in = self.driver.find_element(
                By.XPATH, "//button[@type='submit']")
            sign_in.click()

        # Check username and password
        incorrect_fields = wait.until(
            EC.presence_of_element_located((By.XPATH, '//div/div/p[@role="alert"]')))
        if incorrect_fields:
            print("Your username or password is incorrect. Please try again")
            self.driver.quit()
            sys.exit()

        else:

            # Create new cookies and store in associated folder
            cookies = self.driver.get_cookies()
            serialized_cookies = pickle.dumps(cookies)

            with open(rt_dir, 'wb') as file:
                file.write(serialized_cookies)

            self.driver.quit()

            print(f"New user detected, user '{user}' created successfully.")
            return rt_dir

    def login(self, user, password, root_dir):
        self.driver.get(
            "https://www.linkedin.com/")
        self.path = root_dir

        if root_dir[-1] != '/':
            root_dir = root_dir + '/users/'
        else:
            root_dir = root_dir + 'users/'

        # Check if 'users' folder exists
        if not os.path.exists(root_dir):
            os.makedirs(root_dir)

        root_dir = root_dir + user + '.pkl'

        if not os.path.exists(root_dir):
            try:
                print(f"First login. Proceeding to create log file for new user...")
                cookies_path = self.create_cookies(root_dir, user, password)
                # Load cookies separately after creating them
                self.load_cookies(cookies_path, user)

            except OSError as e:
                print(f"An error occurred while creating folder '{user}': {e}")
        else:
            print(f"User '{user}' exists. Proceeding to login...")
            self.load_cookies(root_dir, user)

    def gather_info(self, jobs_gathered):
        length = len(jobs_gathered)

        for i in range(0, length):
            time.sleep(0.5)
            self.driver.get(jobs_gathered[i])
            try:
                obj1 = JobListing(self.driver, self.path)
                obj1.add_to_csv()
                obj1.display_details()
            except TimeoutException:
                print("Timeout occurred. Reloading the page...")
                i = i-2
        self.driver.quit()

    def scrape(self, role):
        page_number = 0
        links = []
        wait = WebDriverWait(self.driver, 20)

        role_job_listings = f"https://www.linkedin.com/jobs/search/?keywords={role}&start={page_number}"
        self.driver.get(role_job_listings)

        # Find and get the total number of results
        try:
            results = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'jobs-search-results-list__subtitle')]/span")))
            span_text = results.text
            total_results = int(''.join(filter(str.isdigit, span_text)))
        except NoSuchElementException:
            self.driver.refresh()

        # Loop over all the job listings
        while page_number <= total_results:

            try:
                ul_element = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//ul[contains(@class,'scaffold-layout__list-container')]")))
            except TimeoutException:
                # No more job listings
                break

            time.sleep(1.5)
            # Gather job listing URLs
            link_elements = ul_element.find_elements(By.TAG_NAME, "li")
            for element in link_elements:

                try:
                    link_id = element.get_attribute("data-occludable-job-id")
                    if link_id != None:
                        link = f"https://www.linkedin.com/jobs/search/?currentJobId={link_id}"
                        print(link)
                        links.append(link)
                except StaleElementReferenceException:
                    continue

            print(f"Job listings gathered: {len(links)} / {total_results}")

            # Update values
            page_number = page_number + 100
            role_job_listings = f"https://www.linkedin.com/jobs/search/?keywords={role}&start={page_number}"

            self.driver.get(role_job_listings)

        for i in range(0, len(links)):
            print(f"[{i+1}]: {links[i]}")

        # Print the total number of links
        print("Total number of links:", len(links))

        # Send links to be processed
        self.gather_info(links)
