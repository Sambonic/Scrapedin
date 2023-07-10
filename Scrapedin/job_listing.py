from Scrapedin.common_imports import *


class JobListing:

    def __init__(self, driver, path):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.path = path

        # Note:- one of those functions is causing timeout
        # Reorganize and standardize variables and naming conventions
        self.headcount = self.get_headcount()
        self.industry = self.get_industry()
        self.date = self.get_date()
        self.applicants = self.get_applicants()
        self.interviewer = self.get_interviewer()

        self.id = self.get_id()
        self.skills = self.get_skills()
        self.position = self.get_position()
        self.country = self.get_country()
        self.city = self.get_city()
        self.workplace = self.get_workplace()
        self.company = self.get_company()
        self.title = self.get_title()
        self.expertise = self.get_expertise()

    def get_headcount(self):
        headcount_text = ""
        try:
            # Process and return the headcount
            headcount_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'mt5 mb2')]/ul/li[2]/span")
            ))
            headcount_text = headcount_element.text

            start_index = headcount_text.find("employees") - 1

            if start_index != -1:
                headcount_text = headcount_text[:start_index]

        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            pass

        if headcount_text.find("selenium.webdriver.remote") != -1:
            headcount_text = ""

        return headcount_text

    def get_industry(self):
        industry_text = ""
        try:
            # Process and return the industry
            industry_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'mt5 mb2')]/ul/li[2]/span")
            ))
            industry_text = industry_element.text

            start_index = industry_text.find("· ")

            if start_index != -1:
                industry_text = industry_text[start_index+2:]
            else:
                industry_text = ""

        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            pass

        return industry_text

    def get_date(self):
        release_text = ""
        try:
            # Process and return the date
            date_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH,
                "//span[contains(@class,'jobs-unified-top-card__posted-date')]")
            ))
            date_element = date_element.text

            # Get current date
            current_date = datetime.now()

            if "month" in date_element:
                month_value = int(date_element.split()[0])
                delta = relativedelta(months=month_value)
                release_date = current_date - delta
                release_text = release_date.strftime("%Y-%m-%d")
            else:
                time_value = int(date_element.split()[0])

                # Determine the time unit based on the string
                if "week" in date_element:
                    delta = timedelta(weeks=time_value)
                elif "day" in date_element:
                    delta = timedelta(days=time_value)
                elif "hour" in date_element:
                    delta = timedelta(hours=time_value)
                elif "minute" in date_element:
                    delta = timedelta(minutes=time_value)
                elif "second" in date_element:
                    delta = timedelta(seconds=time_value)

                release_date = current_date - delta
                release_text = release_date.strftime("%Y-%m-%d")

        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            pass

        return release_text


    def get_applicants(self):
        applicants_text = ""
        try:
            # Process and return the applicants
            applicants_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH,
                 "//span[contains(@class,'jobs-unified-top-card__applicant-count')]")
            ))
            applicants_text = applicants_element.text

            start_index = applicants_text.find("applicant") - 1

            applicants_text = applicants_text[:start_index]

        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            pass

        return applicants_text

    def get_interviewer(self):
        interviewer_text = ""
        try:
            # Process and return the interviewer
            interviewer_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH,
                 "//div[contains(@class,'mh4 pt4 pb3')]/div/div[2]/a")
            ))
            interviewer_text = interviewer_element.get_attribute("href")

        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            pass
        return interviewer_text

    def get_id(self):
        id_text = ""
        try:
            job_url = self.driver.current_url
            id_text = job_url[job_url.find(
                "currentJobId=")+len("currentJobId="):]

        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            pass
        return id_text

    def get_skills(self):
        skills_text = []

        try:
            skills_button = self.wait.until(EC.presence_of_element_located(
                (By.XPATH,
                 "//button[contains(@class,'jobs-unified-top-card__job-insight-text-button')]")
            ))
            skills_button.click()

            skills_elements = self.wait.until(EC.presence_of_all_elements_located(
                (By.XPATH,
                 "//ul[contains(@class, 'job-details-skill-match-status-list')]/li/div[1]/div[2]")
            ))
            skills_text = [element.text for element in skills_elements]

        except (StaleElementReferenceException, TimeoutException):
            self.driver.refresh()

        except NoSuchElementException:
            pass

        return skills_text

    def get_position(self):
        position_text = ""
        try:
           # Process and return the time
            position_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'mt5 mb2')]/ul/li/span")
            ))
            position_text = position_element.text

            start_index = position_text.find(" ·")

            if start_index != -1:
                position_text = position_text[:start_index]

        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            pass

        return position_text

    def get_country(self):
        country_text = ""
        try:
            # Process and return the country
            country_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH,
                 "//span[contains(@class,'jobs-unified-top-card__bullet')]")
            ))
            country_text = country_element.text

            start_index = country_text.rfind(", ")
            if start_index != -1:
                country_text = country_text[start_index+2:]

        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            pass
        return country_text

    def get_city(self):
        city_text = ""

        try:
            # Process and return the city
            city_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH,
                 "//span[contains(@class,'jobs-unified-top-card__bullet')]")
            ))
            city_text = city_element.text

            start_index = city_text.rfind(", ")

            if start_index != -1:
                parts = city_text.split(", ")

                if parts[0] == parts[1]:
                    city_text = parts[0]

        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            pass
        return city_text

    def get_workplace(self):
        workplace_text = ""

        try:
            # Process and return the workplace
            workplace_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH,
                 "//span[contains(@class,'jobs-unified-top-card__workplace-type')]")
            ))
            workplace_text = workplace_element.text

        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            pass
        return workplace_text

    def get_company(self):
        company_text = ""
        try:
            # Process and return the company
            company_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH,
                 "//span[contains(@class,'jobs-unified-top-card__company-name')]/a")
            ))

            company_text = company_element.text

        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            pass
        return company_text

    def get_title(self):
        title_text = ""
        try:
            # Process and return the title
            title_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH,
                 "//div[contains(@class,'display-flex justify-space-between')]/a/h2")
            ))
            title_text = title_element.text

        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            pass
        return title_text

    def get_expertise(self):
        expertise_text = ""

        try:
            # Process and return the expertise
            expertise_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'mt5 mb2')]/ul/li/span")
            ))
            expertise_text = expertise_element.text

            start_index = expertise_text.find("· ")

            if start_index != -1:
                expertise_text = expertise_text[start_index+2:]

        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            pass
        return expertise_text

    def add_to_csv(self):
        # Create needed folders if they don't exist
        file_path = os.path.join(self.path, "data")
        os.makedirs(file_path, exist_ok=True)
        os.makedirs(os.path.join(file_path, "raw_data"), exist_ok=True)
        os.makedirs(os.path.join(file_path, "clean_data"), exist_ok=True)

        # File path to save the CSV file
        csv_file_path = os.path.join(file_path, "raw_data", "datarole.csv")

        # Attributes
        attributes = ["id", "skills", "position", "country",
                      "city", "workplace", "company", "title", "expertise",
                      "headcount", "industry", "date", "applicants", "interviewer"]

        # Data to be written into the CSV file
        data = {
            "id": self.id,
            "skills": ", ".join(self.skills),
            "position": self.position,
            "country": self.country,
            "city": self.city,
            "workplace": self.workplace,
            "company": self.company,
            "title": self.title,
            "expertise": self.expertise,
            "headcount": self.headcount,
            "industry": self.industry,
            "date": self.date,
            "applicants": self.applicants,
            "interviewer": self.interviewer
        }

        # Check if the file exists
        file_exists = os.path.exists(csv_file_path)

        # Open the CSV file in append mode
        with open(csv_file_path, mode='a', newline='', encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=attributes)

            if not file_exists:
                try:
                    print("Proceeding to create a new CSV header...")
                    writer.writeheader()
                except OSError as e:
                    print("An error occurred while creating the file:", str(e))

            # Write the data into the CSV file
            writer.writerow(data)
            print("CSV file writing complete.")

    def display_details(self):
        print("⬛ Job Listing Details:")
        print(f"ID: {self.id}")
        print(f"Skills: {', '.join(self.skills)}")
        print(f"Position: {self.position}")
        print(f"Country: {self.country}")
        print(f"City: {self.city}")
        print(f"Workplace: {self.workplace}")
        print(f"Company: {self.company}")
        print(f"Title: {self.title}")
        print(f"Expertise: {self.expertise}")
        print(f"Headcount: {self.headcount}")
        print(f"Industry: {self.industry}")
        print(f"Date: {self.date}")
        print(f"Applicants: {self.applicants}")
        print(f"Interviewer: {self.interviewer}")
