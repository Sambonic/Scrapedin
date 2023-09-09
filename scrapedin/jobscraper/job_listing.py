from scrapedin.configurations.common_imports import *
from scrapedin.jobscraper.data_preprocessing import _translate_skills


class JobListing:
    def __init__(self, driver, wait, logger, csv_file_name, path):
        self.driver = driver
        self.wait = wait
        self.logger = logger
        self.csv_file_name = csv_file_name
        self.path = path

        time.sleep(2)
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
        substrings_to_find = ["view", "currentJobId="]

        for substring in substrings_to_find:
            try:
                job_url = self.driver.current_url
                id_text = job_url[job_url.find(substring) + len(substring):]
                if id_text:
                    break  # Exit the loop if a substring is found

            except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
                continue  # Continue to the next substring if an exception occurs

        if not id_text:
            self.logger.error("ID not found")

        return id_text

    def _get_date(self):
        date_text = ""
        release_text = ""
        delta = None

        xpaths_to_try = [
            "//div[contains(@class,'jobs-unified-top-card__primary-description')]/div"
        ]

        for xpath in xpaths_to_try:
            try:
                date_element = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
                self.wait.until(EC.visibility_of(date_element))
                date_text = date_element.text
                break

            except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
                continue

        if date_text:
            if "ago" in date_text:
                words = date_text.split()
                if "ago" in words:
                    idx = words.index("ago")
                    if idx >= 2:
                        date_text = f"{words[idx - 2]} {words[idx - 1]} {words[idx]}"

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
        else:
            self.logger.error("Date not found")

        return release_text

    def _get_company(self):
        company_text = ""
        xpaths_to_try = [
            "//div[contains(@class,'jobs-unified-top-card__primary-description')]/div/a",
            "//span[contains(@class,'jobs-unified-top-card__company-name')]"
        ]

        for xpath in xpaths_to_try:
            try:
                company_element = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
                self.wait.until(EC.visibility_of(company_element))
                company_text = company_element.text
                break

            except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
                continue

        if not company_text:
            self.logger.error("Company not found")

        return company_text

    def _get_salary(self):
        salary_text = ""
        xpaths_to_try = [
            "//div[contains(@class,'mt5 mb2')]/ul/li/span",
        ]

        for xpath in xpaths_to_try:
            try:
                salary_element = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
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
                break

            except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
                continue

        if not salary_text:
            self.logger.error("Salary not found")

        return salary_text

    def _get_position(self):
        position_text = ""
        xpaths_to_try = [
            "//div[contains(@class,'mt5 mb2')]/ul/li/span",
        ]

        for xpath in xpaths_to_try:
            try:
                position_element = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
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
                    positions_list = ["Full-time",
                                      "Part-time", "Contract", "Internship"]
                    if any(position in position_text for position in positions_list):
                        end_index = position_text.find("·")
                        if end_index != -1:
                            position_text = position_text[:end_index]
                    else:
                        position_text = ""

                position_text = position_text.replace(" ", "")

                if "from job description" in position_text:
                    position_text = ""
                break

            except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
                continue

        if not position_text:
            self.logger.error("Position not found")

        return position_text

    def _get_title(self):
        title_text = ""
        xpaths_to_try = [
            "//div[contains(@class,'display-flex justify-space-between')]/a/h2",
            "//h1[contains(@class,'t-24 t-bold jobs-unified-top-card__job-title')]"
        ]

        for xpath in xpaths_to_try:
            try:
                title_element = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
                self.wait.until(EC.visibility_of(title_element))
                title_text = title_element.text
                break

            except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
                continue

        if not title_text:
            self.logger.error("Title not found")

        return title_text

    def _get_headcount(self):
        headcount_text = ""
        xpaths_to_try = [
            "//div[contains(@class,'mt5 mb2')]/ul/li[2]/span",
        ]

        for xpath in xpaths_to_try:
            try:
                headcount_element = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
                self.wait.until(EC.visibility_of(headcount_element))
                headcount_text = headcount_element.text

                start_index = headcount_text.find("employees") - 1

                if start_index != -1:
                    headcount_text = headcount_text[:start_index]
                break

            except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
                continue

        if not headcount_text:
            self.logger.error("Headcount not found")

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
        xpaths_to_try = [
            "//div[contains(@class,'mt5 mb2')]/ul/li[2]/span",
        ]

        for xpath in xpaths_to_try:
            try:
                industry_element = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
                self.wait.until(EC.visibility_of(industry_element))
                industry_text = industry_element.text

                start_index = industry_text.find("· ")

                if start_index != -1:
                    industry_text = industry_text[start_index+2:]
                    break

            except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
                continue

        if not industry_text:
            self.logger.error("Industry not found")

        return industry_text

    def _get_expertise(self):
        expertise_text = ""
        xpaths_to_try = [
            "//div[contains(@class,'mt5 mb2')]/ul/li/span",
        ]

        for xpath in xpaths_to_try:
            try:
                expertise_element = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
                self.wait.until(EC.visibility_of(expertise_element))
                expertise_text = expertise_element.text

                start_index = expertise_text.rfind("·")

                if start_index != -1:
                    expertise_text = expertise_text[start_index+2:]

                positions_list = ["Full-time",
                                  "Part-time", "Contract", "Internship"]
                if any(position in expertise_text for position in positions_list):
                    expertise_text = ""
                else:
                    expertise_text = expertise_text.replace(" ", "")
                    break

            except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
                continue

        if not expertise_text:
            self.logger.error("Expertise not found")

        return expertise_text

    def _get_applicants(self):
        applicants_text = ""
        xpaths_to_try = [
            "//div[contains(@class,'jobs-unified-top-card__primary-description')]/div/span[5]",
            "//span[contains(@class,'jobs-unified-top-card__subtitle-secondary-grouping t-black--light')]/span[contains(@class,'jobs-unified-top-card__bullet')]"
        ]

        for xpath in xpaths_to_try:
            try:
                applicants_element = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
                self.wait.until(EC.visibility_of(applicants_element))
                applicants_text = applicants_element.text
                break

            except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
                continue

        if applicants_text:
            end_index = applicants_text.find("applicant") - 1
            applicants_text = applicants_text[:end_index]

            if "Over" in applicants_text:
                start_index = applicants_text.find(" ") + 1
                applicants_text = applicants_text[start_index:]

            applicants_text = applicants_text.replace(" ", "")
        else:
            self.logger.error("Applicants not found")

        return applicants_text

    def _get_interviewer(self):
        interviewer_text = ""
        xpaths_to_try = [
            "//div[contains(@class,'mh4 pt4 pb3')]/div/div[2]/a",
        ]

        for xpath in xpaths_to_try:
            try:
                interviewer_element = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
                self.wait.until(EC.visibility_of(interviewer_element))
                interviewer_text = interviewer_element.get_attribute("href")
                break

            except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
                continue

        if not interviewer_text:
            self.logger.error("Interviewer not found")

        return interviewer_text

    def _get_country(self):
        country_text = ""
        xpaths_to_try = [
            "//div[contains(@class,'jobs-unified-top-card__primary-description')]/div",
            "//span[contains(@class,'jobs-unified-top-card__subtitle-primary-grouping t-black')]/span[contains(@class,'jobs-unified-top-card__bullet')]"
        ]

        for xpath in xpaths_to_try:
            try:
                country_element = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
                self.wait.until(EC.visibility_of(country_element))
                country_text = country_element.text
                break

            except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
                continue

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
        else:
            self.logger.error("Country not found")

        return country_text

    def _get_city(self):
        city_text = ""
        xpaths_to_try = [
            "//div[contains(@class,'jobs-unified-top-card__primary-description')]/div",
            "//span[contains(@class,'jobs-unified-top-card__subtitle-primary-grouping t-black')]/span[contains(@class,'jobs-unified-top-card__bullet')]"
        ]

        for xpath in xpaths_to_try:
            try:
                city_element = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
                self.wait.until(EC.visibility_of(city_element))
                city_text = city_element.text
                break

            except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
                continue

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
        else:
            self.logger.error("City not found")

        return city_text

    def _get_workplace(self):
        workplace_text = ""
        xpaths_to_try = [
            "//div[contains(@class,'jobs-unified-top-card__primary-description')]/div",
            "//span[contains(@class,'jobs-unified-top-card__workplace-type')]"
        ]

        for xpath in xpaths_to_try:
            try:
                workplace_element = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
                self.wait.until(EC.visibility_of(workplace_element))
                workplace_text = workplace_element.text
                break

            except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
                continue

        start_index = workplace_text.rfind("(")
        end_index = workplace_text.rfind(")")

        if start_index != -1 and end_index != -1:
            workplace_text = workplace_text[start_index:end_index + 1]
        else:
            workplace_text = ""
            self.logger.error("Workplace not found")

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
