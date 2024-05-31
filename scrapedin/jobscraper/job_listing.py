from scrapedin.configurations.common_imports import *
from scrapedin.jobscraper.data_preprocessing import _translate_skills


class JobListing:

    """
    Initializes a JobListing object with the given parameters.

    Args:
        driver: WebDriver instance used to interact with the web page.
        wait: WebDriverWait instance used to wait for elements to appear.
        logger: Logger instance for logging information.
        csv_file_name: Name of the CSV file where job listings will be saved.
        path: Path to the directory where data will be stored.
    """

    def __init__(self, driver, wait, logger, csv_file_name, path):
        
        self.driver = driver
        self.wait = wait
        self.logger = logger
        self.csv_file_name = csv_file_name
        self.path = path

        self.id = None
        self.date = None
        self.company = None
        self.salary = None
        self.job_type = None
        self.title = None
        self.headcount = None
        self.industry = None
        self.experience = None
        self.applicants = None
        self.interviewer = None
        self.location = None
        self.workplace = None
        self.skills = None
        self.description = None

    def _extract_job_details(self) -> None:
        """
        Extracts all job details by calling individual extraction methods.
        """
        self.id = self._extract_id()
        self.date = self._extract_date()
        self.company = self._extract_company()
        self.salary = self._extract_salary()
        self.job_type = self._extract_job_type()
        self.title = self._extract_title()
        self.headcount = self._extract_headcount()
        self.industry = self._extract_industry()
        self.experience = self._extract_experience()
        self.applicants = self._extract_applicants()
        self.interviewer = self._extract_interviewer()
        self.location = self._extract_location()
        self.workplace = self._extract_workplace()
        self.skills = self._extract_skills()
        self.description = self._extract_description()

    def _extract_id(self) -> str:
        """
        Extracts the unique ID of the job listing.

        Returns:
            str: The job listing ID.
        """
        job_url = self.driver.current_url
        pattern = r"(view\/|currentJobId=)(\d+)"
        match = re.search(pattern, job_url)
        if match:
            return match.group(2)
        else:
            self.logger.error("ID not found")
            return ""

    def _extract_date(self) -> str:
        """
        Extracts and formats the posted date of the job listing.

        Returns:
            str: The formatted posted date.
        """
        date_text = ""
        release_text = ""
        delta = None

        path = "//div[contains(@class,'jobs-unified-top-card__primary-description')]/div"

        try:
            date_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, path)))
            self.wait.until(EC.visibility_of(date_element))
            date_text = date_element.text
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            pass

        if date_text:
            if "ago" in date_text:
                words = date_text.split()
                if "ago" in words:
                    idx = words.index("ago")
                    if idx >= 2:
                        date_text = f"{words[idx - 2]} {words[idx - 1]} {words[idx]}"

            current_date = datetime.utcnow()

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
        else:
            self.logger.error("Date not found")

        return release_text

    def _extract_company(self) -> str:
        """
        Extracts the company name from the job listing page.

        Returns:
            str: The company name.
        """
        path = "//div[contains(@class,'job-details-jobs-unified-top-card__primary-description-container')]/div/a"
        try:
            company_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, path))
            )
            return company_element.text
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            self.logger.error("Company not found")
            return ""

    def _extract_salary(self) -> str:
        """
        Extracts the salary range per hour or per year.

        Returns:
            str: The salary range.
        """
        path = "//div[contains(@class,'mt2 mb2')]/ul/li[1]/span/span[1]"
        try:
            salary_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, path))
            )
            salary_text = salary_element.text
            if "$" not in salary_text:
                return ""
            else:
                return salary_text
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            self.logger.error("Salary not found")
            return ""

    def _extract_workplace(self) -> str:
        """
        Extracts the work location (on-site, remote, hybrid).

        Returns:
            str: The workplace type.
        """
        path = "//ul/li[contains(@class,'job-details-jobs-unified-top-card__job-insight job-details-jobs-unified-top-card__job-insight--highlight')]"
        try:
            workplace_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, path))
            )
            workplace_text = workplace_element.text
            workplace_options = ["On-site", "Remote", "Hybrid"]

            for workplace in workplace_options:
                if workplace in workplace_text:
                    return workplace
            return ""
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            self.logger.error("Workplace not found")
            return ""

    def _extract_job_type(self) -> str:
        """
        Extracts the job type (Full-time, Part-time, Contract, Temporary, Volunteer, Internship, Other).

        Returns:
            str: The job type.
        """
        path = "//ul/li[contains(@class,'job-details-jobs-unified-top-card__job-insight job-details-jobs-unified-top-card__job-insight--highlight')]"
        try:
            job_type_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, path))
            )
            job_type_text = job_type_element.text
            job_type_options = ["Full-time", "Part-time", "Contract", "Temporary", "Volunteer", "Internship", "Other"]

            for job_type in job_type_options:
                if job_type in job_type_text:
                    return job_type
            return ""
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            self.logger.error("Job type not found")
            return ""

    def _extract_experience(self) -> str:
        """
        Extracts the experience level required (Internship, Entry level, Associate, Mid-Senior level, Director, Executive).

        Returns:
            str: The experience level required.
        """
        path = "//ul/li[contains(@class,'job-details-jobs-unified-top-card__job-insight job-details-jobs-unified-top-card__job-insight--highlight')]"
        try:
            experience_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, path))
            )
            experience_text = experience_element.text
            experience_options = ["Internship", "Entry level", "Associate", "Mid-Senior level", "Director", "Executive"]

            for experience in experience_options:
                if experience in experience_text:
                    return experience
            return ""
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            self.logger.error("Experience level not found")
            return ""

    def _extract_title(self) -> str:
        """
        Extracts the title of the job posting.

        Returns:
            str: The job title.
        """
        path = "//div[contains(@class,'t-24 job-details-jobs-unified-top-card__job-title')]/h1"
        try:
            title_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, path))
            )
            return title_element.text
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            self.logger.error("Title not found")
            return ""

    def _extract_headcount(self) -> str:
        """
        Extracts the range of employees in the hiring company.

        Returns:
            str: The headcount range in the format "x,xxx-xx,xxx employees" or "x,xxx+ employees".
        """
        path = "//div[contains(@class,'mt2 mb2')]/ul"
        try:
            headcount_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, path))
            )
            headcount_text = headcount_element.text

            pattern = r"(\d+,?\d+-\d+,?\d+|\d+,?\d+\+)\s(employees)"
            match = re.search(pattern, headcount_text)
            if match:
                return match.group(1)
            else:
                return ""
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            self.logger.error("Headcount not found")
            return ""

    def _extract_industry(self) -> str:
        """
        Extracts the industry of the hiring company.

        Returns:
            str: The industry of the company.
        """
        path = "//div[contains(@class,'mt2 mb2')]/ul"
        try:
            industry_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, path))
            )
            industry_text = industry_element.text

            pattern = r"(·)\s(.+)"
            match = re.search(pattern, industry_text)
            if match:
                return match.group(2)
            else:
                return ""
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            self.logger.error("Industry not found")
            return ""

    def _extract_skills(self) -> list[str]:
        """
        Extracts the required skills of the job listing.

        Returns:
            list[str]: A list of required skills for the job.
        """
        skills_text = []

        try:
            skills_button = self.wait.until(EC.presence_of_element_located(
                (By.XPATH,
                 "//button[contains(@class,'mv5 t-16 pt1 pb1 artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--2 artdeco-button--secondary ember-view')]")
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
                self.logger.info("Non-english text detected. Proceeding to translate. . .")
            skills_text = skills_text.replace("\nLook up details", "")

        except (StaleElementReferenceException, TimeoutException, NoSuchElementException, ElementClickInterceptedException):
            self.logger.error("Skills not found")
            pass

        return skills_text

    def _extract_applicants(self) -> int:
        """
        Extracts the total number of people that applied to the job listing at the time of extraction.

        Returns:
            int: The number of applicants, or -1 if not found.
        """
        path = "//div[contains(@class,'job-details-jobs-unified-top-card__primary-description-container')]"
        try:
            parent_div = self.wait.until(
                EC.presence_of_element_located((By.XPATH, path))
            )
            child_spans = [span.text.strip() for span in parent_div.find_elements(By.XPATH, ".//span")]
            applicant_text = child_spans[-1]
            pattern = r"(\d+)\s(applicants)"
            match = re.search(pattern, applicant_text)
            if match:
                return int(match.group(1))
            else:
                return -1
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            self.logger.error("Applicants not found")
            return -1

    def _extract_interviewer(self) -> str:
        """
        Extracts the LinkedIn page of the hiring manager (if available).

        Returns:
            str: The URL of the hiring manager's LinkedIn page, or an empty string if not found.
        """
        path = "//div[contains(@class,'mh4 pt4 pb3')]/div/a"
        try:
            interviewer_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, path)))
            self.wait.until(EC.visibility_of(interviewer_element))
            return interviewer_element.get_attribute("href")
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            self.logger.error("Interviewer not found")
            return ""

    def _extract_location(self) -> str:
        """
        Extracts the general location given for the hiring company.

        Returns:
            str: The location of the job listing.
        """
        path = "//div[contains(@class,'job-details-jobs-unified-top-card__primary-description-without-tagline mb2')]"
        try:
            location_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, path))
            )
            location_text = location_element.text
            pattern = r"· (.*?) ·"
            match = re.search(pattern, location_text)
            if match:
                return match.group(1).strip()
            else:
                return ""
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            self.logger.error("Location not found")
            return ""

    def _extract_description(self) -> str:
        """
        Extracts the job description.

        Returns:
            str: The job description text.
        """
        path = "//article/div/div[1]/div"
        try:
            description_element = self.wait.until(
                EC.presence_of_element_located((By.XPATH,path))
            )
            description_text = re.sub(r'\s+', ' ', description_element.text)
            description_text = '\n'.join([line for line in description_text.splitlines() if line.strip()])
            return description_text
        except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
            self.logger.error("Description not found")
            return ""

    def _add_to_csv(self) -> None:
        """
        Adds job listing details to a CSV file. Creates necessary folders if needed, formats the data, and appends it to an appropriately named CSV file in the 'raw data' folder of the project.
        """
        file_path = os.path.join(self.path, "data")

        os.makedirs(file_path, exist_ok=True)
        os.makedirs(os.path.join(file_path, "raw_data"), exist_ok=True)
        os.makedirs(os.path.join(file_path, "clean_data"), exist_ok=True)

        csv_file_path = os.path.join(file_path, "raw_data", self.csv_file_name)

        data = {
            "id": self.id,
            "date": self.date,
            "company": self.company,
            "salary": self.salary,
            "job_type": self.job_type,
            "title": self.title,
            "headcount": self.headcount,
            "skills": self.skills,
            "industry": self.industry,
            "experience": self.experience,
            "applicants": self.applicants,
            "interviewer": self.interviewer,
            "location": self.location,
            "workplace": self.workplace,
            "description": self.description
        }

        file_exists = os.path.exists(csv_file_path)

        with open(csv_file_path, mode='a', newline='', encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())

            if not file_exists:
                try:
                    self.logger.info("Proceeding to create a new CSV header. . .")
                    writer.writeheader()
                except OSError as e:
                    self.logger.error("An error occurred while creating the file: %s", str(e))
            writer.writerow(data)
            self.logger.info("Data inserted into CSV file successfully.")

    def _display_details(self) -> None:
        """
        Displays details extracted in the terminal.
        """
        self.logger.info("⬛ Job Listing Details:")
        self.logger.info(f"ID: {self.id}")
        self.logger.info(f"Date: {self.date}")
        self.logger.info(f"Company: {self.company}")
        self.logger.info(f"Salary: {self.salary}")
        self.logger.info(f"Job Type: {self.job_type}")
        self.logger.info(f"Title: {self.title}")
        self.logger.info(f"Headcount: {self.headcount}")
        self.logger.info(f"Skills: {self.skills}")
        self.logger.info(f"Industry: {self.industry}")
        self.logger.info(f"Experience: {self.experience}")
        self.logger.info(f"Applicants: {self.applicants}")
        self.logger.info(f"Interviewer: {self.interviewer}")
        self.logger.info(f"Location: {self.location}")
        self.logger.info(f"Workplace: {self.workplace}")
        self.logger.info(f"Description: {self.description}")
