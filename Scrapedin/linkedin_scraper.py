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
        wait = WebDriverWait(self.driver, 30)
        user_field = wait.until(
            EC.presence_of_element_located((By.ID, 'session_key')))
        pass_field = wait.until(
            EC.presence_of_element_located((By.ID, 'session_password')))
        user_field.send_keys(user)
        pass_field.send_keys(password)

        sign_in = self.driver.find_element(
            By.XPATH, "//button[@type='submit']")
        sign_in.click()

        cookies = self.driver.get_cookies()
        serialized_cookies = pickle.dumps(cookies)

        # Create new cookies and store in associated folder
        with open(rt_dir, 'wb') as file:
            file.write(serialized_cookies)

        self.driver.quit()

        print(f"New user detected, user '{user}' created successfully.")
        return rt_dir  # Return the path to the cookies file

    def login(self, user, password, root_dir):
        self.driver.get(
            "https://www.linkedin.com/?trk=seo-authwall-base_nav-header-logo")
        self.path = root_dir

        if root_dir[-1] != '/':
            rt_dir = root_dir + '/users/'
        else:
            rt_dir = root_dir + 'users/'

        # Check if 'users' folder exists
        if not os.path.exists(rt_dir):
            os.makedirs(rt_dir)

        rt_dir = rt_dir + user + '.pkl'

        if not os.path.exists(rt_dir):
            try:
                print(f"First login. Proceeding to create log file for new user...")
                cookies_path = self.create_cookies(rt_dir, user, password)
                # Load cookies separately after creating them
                self.load_cookies(cookies_path, user)

            except OSError as e:
                print(f"An error occurred while creating folder '{user}': {e}")
        else:
            print(f"User '{user}' exists. Proceeding to login...")
            self.load_cookies(rt_dir, user)

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
                self.driver.refresh()
        self.driver.quit()

    def scrape(self, role):
        page_number = 0
        links = []
        wait = WebDriverWait(self.driver, 30)

        role_job_listings = f"https://www.linkedin.com/jobs/search/?keywords={role}&start={page_number}"
        self.driver.get(role_job_listings)

        try:
            # Find and get the total number of results
            results = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'jobs-search-results-list__subtitle')]/span")))
            span_text = results.text
            total_results = int(''.join(filter(str.isdigit, span_text)))
        except NoSuchElementException:
            self.driver.refresh()

        # Loop over all the job listings
        while page_number < total_results:
            ul_element = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//ul[contains(@class,'scaffold-layout__list-container')]")))
            content = self.driver.find_element(
                By.CLASS_NAME, 'jobs-search-results-list')

            time.sleep(1)
            scroll_distance = 300
            for i in range(1, 10):
                self.driver.execute_script(
                    "arguments[0].scrollTop = arguments[1];", content, scroll_distance)
                scroll_distance = scroll_distance+400
                time.sleep(0.5)

            time.sleep(1)

            link_elements = ul_element.find_elements(By.TAG_NAME, "a")

            for element in link_elements:
                links.append(element.get_attribute("href"))

            print(f"Job listings gathered: {len(links)} / {total_results}")

            page_number = page_number + 25

            role_job_listings = f"https://www.linkedin.com/jobs/search/?keywords={role}&start={page_number}"
            self.driver.get(role_job_listings)

        for i in range(0, len(links)):
            print(f"[{i+1}]: {links[i]}")

        # Print the total number of links
        print("Total number of links:", len(links))

        # Send links to be processed
        self.gather_info(links)
