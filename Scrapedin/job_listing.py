from Scrapedin.common_imports import *
from Scrapedin.data_preprocessing import _translate_skills


class JobListing:
    def __init__(self, driver, wait, logger, csv_file_name, path):
        self.driver = driver
        self.wait = wait
        self.logger = logger
        self.csv_file_name = csv_file_name
        self.path = path

        time.sleep(1.5)
        self.id = self._get_id()
        self.date = self._get_date()
        self.company = self._get_company()
        self.salary = self._get_salary()
        self.position = self._get_position()
        self.title = self._get_title()
        self.headcount = self._get_headcount()
        self.skills = self._get_skills()
        self.industry = self._get_industry()
        self.expertise = self._get_expertise()
        self.applicants = self._get_applicants()
        self.interviewer = self._get_interviewer()
        self.country = self._get_country()
        self.city = self._get_city()
        self.workplace = self._get_workplace()

    # Extract said elements as present on the webpage
    def _get_id(self):
        id_text = ""
        try:
            job_url = self.driver.current_url
            id_text = job_url[job_url.find(
                "currentJobId=")+len("currentJobId="):]

        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            self.logger.error(
                f"ID not found")
            pass

        return id_text

    def _get_date(self):
        date_text = ""
        release_text = ""
        delta = None

        try:
            date_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH,
                 "/html/body/div[5]/div[3]/div[4]/div/div/main/div/div[2]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/div[2]/div/span[3]")
            ))
            self.wait.until(EC.visibility_of(date_element))
            date_text = date_element.text

        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):

            try:
                date_element = self.wait.until(EC.presence_of_element_located(
                    (By.XPATH,
                     "//span[contains(@class,'jobs-unified-top-card__posted-date')]")
                ))
                self.wait.until(EC.visibility_of(date_element))
                date_text = date_element.text

            except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
                self.logger.error("Date not found")
                pass

        if date_text:
            start_index = ""
            for num in range(10):
                start_index = date_text.find(str(num))
                if start_index != -1:
                    break

            end_index = date_text.find("ago")
            date_text = date_text[:end_index]
            date_text = date_text[start_index:]

            current_date = datetime.now()

            if "week" in date_text:
                time_value = int(date_text.split()[0])
                delta = timedelta(weeks=time_value)
            elif "day" in date_text:
                time_value = int(date_text.split()[0])
                delta = timedelta(days=time_value)
            elif "hour" in date_text:
                time_value = int(date_text.split()[0])
                delta = timedelta(hours=time_value)
            elif "minute" in date_text:
                time_value = int(date_text.split()[0])
                delta = timedelta(minutes=time_value)
            elif "second" in date_text:
                time_value = int(date_text.split()[0])
                delta = timedelta(seconds=time_value)
            elif "month" in date_text:
                month_value = int(date_text.split()[0])
                delta = relativedelta(months=month_value)

            if delta is not None:
                release_date = current_date - delta
                release_text = release_date.strftime("%Y-%m-%d")

        return release_text

    def _get_company(self):
        company_text = ""
        try:
            company_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH,
                 "//div[contains(@class,'jobs-unified-top-card__primary-description')]/div/a")
            ))
            self.wait.until(EC.visibility_of(company_element))
            company_text = company_element.text

        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            try:
                company_element = self.wait.until(EC.presence_of_element_located(
                    (By.XPATH,
                     "//span[contains(@class,'jobs-unified-top-card__company-name')]")
                ))
                self.wait.until(EC.visibility_of(company_element))
                company_text = company_element.text

            except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
                self.logger.error(f"Company not found")
                pass

        return company_text

    def _get_salary(self):
        salary_text = ""
        try:
            salary_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'mt5 mb2')]/ul/li/span")
            ))
            self.wait.until(EC.visibility_of(salary_element))
            salary_text = salary_element.text

            if "$" in salary_text:
                end_index = salary_text.find("(")
                if end_index != -1:
                    salary_text = salary_text[:end_index]

                end_index = salary_text.find("·")
                if end_index != -1:
                    salary_text = salary_text[:end_index]

            else:
                salary_text = ""

        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            self.logger.error(
                f"Salary not found")
            pass

        return salary_text

    def _get_position(self):
        position_text = ""
        try:
            position_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'mt5 mb2')]/ul/li/span")
            ))
            self.wait.until(EC.visibility_of(position_element))
            position_text = position_element.text

            div = position_text.count("·")

            if div == 2:
                start_index = position_text.find("·")
                if start_index != -1:
                    position_text = position_text[start_index+2:]

                end_index = position_text.find("·")
                if end_index != -1:
                    position_text = position_text[:end_index]

            if div == 1:
                positions_list = ["Full-time", "Part-time", "Contract","Internship"]
                if any(position in position_text for position in positions_list):
                    end_index = position_text.find("·")
                    if end_index != -1:
                        position_text = position_text[:end_index]
                else:
                    position_text = ""

            position_text.replace(" ", "")

        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            self.logger.error(
                f"Position not found")
            pass

        return position_text

    def _get_title(self):
        title_text = ""
        try:
            title_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH,
                 "//div[contains(@class,'display-flex justify-space-between')]/a/h2")
            ))
            self.wait.until(EC.visibility_of(title_element))
            title_text = title_element.text

        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            self.logger.error(
                f"Title not found")
            pass

        return title_text

    def _get_headcount(self):
        headcount_text = ""
        try:
            headcount_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'mt5 mb2')]/ul/li[2]/span")
            ))
            self.wait.until(EC.visibility_of(headcount_element))
            headcount_text = headcount_element.text

            start_index = headcount_text.find("employees") - 1

            if start_index != -1:
                headcount_text = headcount_text[:start_index]

        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            self.logger.error(
                f"Headcount not found")
            pass

        return headcount_text

    def _get_skills(self):
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
            skills_text = ", ".join(skills_text)
            ascii_text = unidecode(skills_text)
            if skills_text != ascii_text:
                skills_text = _translate_skills(skills_text)
                self.logger.info(
                    "Non-english text detected. Proceeding to translate. . .")
            skills_text = skills_text.replace("\nLook up details", "")

        except (StaleElementReferenceException, TimeoutException, NoSuchElementException, ElementClickInterceptedException):
            self.logger.error("Skills not found")
            pass

        return skills_text

    def _get_industry(self):
        industry_text = ""
        try:
            industry_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'mt5 mb2')]/ul/li[2]/span")
            ))
            self.wait.until(EC.visibility_of(industry_element))
            industry_text = industry_element.text

            start_index = industry_text.find("· ")

            if start_index != -1:
                industry_text = industry_text[start_index+2:]
            else:
                industry_text = ""

        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            self.logger.error(
                f"Industry not found")
            pass

        return industry_text

    def _get_expertise(self):
        expertise_text = ""
        try:
            expertise_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'mt5 mb2')]/ul/li/span")
            ))
            self.wait.until(EC.visibility_of(expertise_element))
            expertise_text = expertise_element.text

            start_index = expertise_text.rfind("·")

            if start_index != -1:
                expertise_text = expertise_text[start_index+2:]

            positions_list = ["Full-time", "Part-time", "Contract", "Internship"]
            if any(position in expertise_text for position in positions_list):
                expertise_text = ""

            expertise_text.replace(" ", "")

        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            self.logger.error(
                f"Expertise not found")
            pass

        return expertise_text

    def _get_applicants(self):
        applicants_text = ""
        try:
            applicants_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH,
                 "//div[contains(@class,'jobs-unified-top-card__primary-description')]/div/span[5]")
            ))
            self.wait.until(EC.visibility_of(applicants_element))
            applicants_text = applicants_element.text

        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):

            try:
                applicants_element = self.wait.until(EC.presence_of_element_located(
                    (By.XPATH,
                     "//span[contains(@class,'jobs-unified-top-card__subtitle-secondary-grouping t-black--light')]/span[contains(@class,'jobs-unified-top-card__bullet')]")
                ))
                self.wait.until(EC.visibility_of(applicants_element))
                applicants_text = applicants_element.text

            except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
                self.logger.error(
                    f"Applicants not found")
                pass

        if applicants_text:
            end_index = applicants_text.find("applicant") - 1
            applicants_text = applicants_text[:end_index]

            if "Over" in applicants_text:
                start_index = applicants_text.find(" ") + 1
                applicants_text = applicants_text[start_index:]

            applicants_text.replace(" ", "")

        return applicants_text

    def _get_interviewer(self):
        interviewer_text = ""
        try:
            interviewer_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH,
                 "//div[contains(@class,'mh4 pt4 pb3')]/div/div[2]/a")
            ))
            self.wait.until(EC.visibility_of(interviewer_element))
            interviewer_text = interviewer_element.get_attribute("href")

        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            self.logger.error(
                f"Interviewer not found")
            pass

        return interviewer_text

    def _get_country(self):

        country_text = ""
        try:
            country_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH,
                 "//div[contains(@class,'jobs-unified-top-card__primary-description')]/div")
            ))
            self.wait.until(EC.visibility_of(country_element))
            country_text = country_element.text

        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            try:
                country_element = self.wait.until(EC.presence_of_element_located(
                    (By.XPATH,
                     "//span[contains(@class,'jobs-unified-top-card__subtitle-primary-grouping t-black')]/span[contains(@class,'jobs-unified-top-card__bullet')]")
                ))
                self.wait.until(EC.visibility_of(country_element))
                country_text = country_element.text
            except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
                self.logger.error(
                    f"Country not found")
                pass

        if country_text:
            start_index = country_text.rfind(", ")
            if start_index != -1:
                country_text = country_text[start_index + 2:]
                end_index = country_text.find(" ")
                if end_index != -1:
                    country_text = country_text[:end_index]

            end_index = country_text.rfind("(")
            if end_index != -1:
                country_text = country_text[:end_index-1]
                start_index = country_text.rfind(" ")
                if start_index != -1:
                    country_text = country_text[start_index + 1:]

            end_index = country_text.rfind("Reposted")
            if end_index != -1:
                country_text = country_text[:end_index-1]
                start_index = country_text.rfind(" ")
                if start_index != -1:
                    country_text = country_text[start_index + 1:]


        return country_text

    def _get_city(self):

        city_text = ""
        try:
            city_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH,
                 "//div[contains(@class,'jobs-unified-top-card__primary-description')]/div")
            ))
            self.wait.until(EC.visibility_of(city_element))
            city_text = city_element.text

        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            try:
                city_element = self.wait.until(EC.presence_of_element_located(
                    (By.XPATH,
                     "//span[contains(@class,'jobs-unified-top-card__subtitle-primary-grouping t-black')]/span[contains(@class,'jobs-unified-top-card__bullet')]")
                ))
                self.wait.until(EC.visibility_of(city_element))
                city_text = city_element.text

            except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
                self.logger.error(
                    f"City not found")
                pass

        if city_text:
            country_position = city_text.rfind(self.country)
            if country_position != -1:
                city_text = city_text[:country_position - 2]

            start_index = city_text.rfind(",")
            if start_index != -1:
                city_text = city_text[start_index + 2:]

            start_index = city_text.rfind("·")
            if start_index != -1:
                city_text = city_text[start_index + 2:]

        return city_text

    def _get_workplace(self):
        workplace_text = ""
        try:
            workplace_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH,
                 "//div[contains(@class,'jobs-unified-top-card__primary-description')]/div")
            ))
            self.wait.until(EC.visibility_of(workplace_element))
            workplace_text = workplace_element.text

        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            try:
                workplace_element = self.wait.until(EC.presence_of_element_located(
                    (By.XPATH,
                     "//span[contains(@class,'jobs-unified-top-card__workplace-type')]")
                ))
                self.wait.until(EC.visibility_of(workplace_element))
                workplace_text = workplace_element.text

            except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
                self.logger.error(f"Workplace not found")
                pass

        if workplace_text:
            start_index = workplace_text.rfind("(")
            end_index = workplace_text.rfind(")")

            if start_index != -1 and end_index != -1:
                workplace_text = workplace_text[start_index:end_index + 1]
        else:
            workplace_text = ""

        return workplace_text

    # Add info in the CSV file with appropriate format
    def _add_to_csv(self):
        # Create needed folders if they don't exist
        file_path = os.path.join(self.path, "data")
        os.makedirs(file_path, exist_ok=True)
        os.makedirs(os.path.join(file_path, "raw_data"), exist_ok=True)
        os.makedirs(os.path.join(file_path, "clean_data"), exist_ok=True)

        # File path to save the CSV file
        csv_file_path = os.path.join(file_path, "raw_data", self.csv_file_name)

        # Attributes
        attributes = ["id", "date", "company", "salary", "position", "title", "headcount", "skills", "industry", "expertise", "applicants",
                      "interviewer", "country", "city", "workplace"]

        data = {
            "id": self.id,
            "date": self.date,
            "company": self.company,
            "salary": self.salary,
            "position": self.position,
            "title": self.title,
            "headcount": self.headcount,
            "skills": self.skills,
            "industry": self.industry,
            "expertise": self.expertise,
            "applicants": self.applicants,
            "interviewer": self.interviewer,
            "country": self.country,
            "city": self.city,
            "workplace": self.workplace
        }

        # Check if the file exists
        file_exists = os.path.exists(csv_file_path)

        # Open the CSV file in append mode
        with open(csv_file_path, mode='a', newline='', encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=attributes)

            if not file_exists:
                try:
                    self.logger.info(
                        "Proceeding to create a new CSV header. . .")
                    writer.writeheader()
                except OSError as e:
                    self.logger.error(
                        "An error occurred while creating the file: %s", str(e))

            # Write the data into the CSV file
            writer.writerow(data)
            self.logger.info("Data inserted into CSV file successfully.")

    # Display details gathered in terminal
    def _display_details(self):
        self.logger.info("⬛ Job Listing Details:")
        self.logger.info(f"ID: {self.id}")
        self.logger.info(f"Date: {self.date}")
        self.logger.info(f"Company: {self.company}")
        self.logger.info(f"Salary: {self.salary}")
        self.logger.info(f"Position: {self.position}")
        self.logger.info(f"Title: {self.title}")
        self.logger.info(f"Headcount: {self.headcount}")
        self.logger.info(f"Skills: {self.skills}")
        self.logger.info(f"Industry: {self.industry}")
        self.logger.info(f"Expertise: {self.expertise}")
        self.logger.info(f"Applicants: {self.applicants}")
        self.logger.info(f"Interviewer: {self.interviewer}")
        self.logger.info(f"Country: {self.country}")
        self.logger.info(f"City: {self.city}")
        self.logger.info(f"Workplace: {self.workplace}")
