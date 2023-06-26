from Scrapedin.common_imports import *


class JobListing:

    def __init__(self, driver, path):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
        self.path = path

        self.Id = self.get_id()
        self.skills = self.get_skills()
        self.position = self.get_position()
        self.time = self.get_time()
        self.country = self.get_country()
        self.city = self.get_city()
        self.workplace = self.get_workplace()
        self.company = self.get_company()
        self.title = self.get_title()
        self.expertise = self.get_expertise()

    def get_id(self):
        try:
            job_url = self.driver.current_url
            id_element = job_url[job_url.find("currentJobId=")+len("currentJobId="):]
        except NoSuchElementException:
            id_element = "N/A"
        return id_element

    def get_skills(self):
        try:
            skills_button = self.wait.until(EC.presence_of_element_located(
                (By.XPATH,
                 "//button[contains(@class,'jobs-unified-top-card__job-insight-text-button')]")
            ))

            time.sleep(0.3)
            skills_button.click()

            skills_elements = self.wait.until(EC.presence_of_all_elements_located(
                (By.XPATH,
                 "//ul[contains(@class, 'job-details-skill-match-status-list')]/li/div[1]/div[2]")
            ))
            skills = [element.text for element in skills_elements]

        except StaleElementReferenceException:
            self.driver.refresh()

        except TimeoutException:
            self.driver.refresh()

        except NoSuchElementException:
            skills = []

        
        return skills

    def get_position(self):
        try:
            # Process and return the position
            position_element = ""
        except NoSuchElementException:
            position_element = "N/A"
        return position_element

    def get_time(self):
        try:
           # Process and return the time
            time_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'mt5 mb2')]/ul/li/span")
            ))
            time_element = time_element.text

            start_index = time_element.find(" ·")

            if start_index != -1:
                time_element = time_element[:start_index]
            else:
                time_element = ""

        except NoSuchElementException:
            time_element = "N/A"

        return time_element

    def get_country(self):
        try:
            # Process and return the country
            country_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH,
                 "//span[contains(@class,'jobs-unified-top-card__bullet')]")
            ))
            country_element = country_element.text

        except NoSuchElementException:
            country_element = "N/A"
        return country_element

    def get_city(self):
        try:
            # Process and return the city
            city_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH,
                 "//span[contains(@class,'jobs-unified-top-card__bullet')]")
            ))
            city_element = city_element.text

        except NoSuchElementException:
            city_element = "N/A"
        return city_element

    def get_workplace(self):
        try:
            # Process and return the workplace
            workplace_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH,
                 "//span[contains(@class,'jobs-unified-top-card__workplace-type')]")
            ))
            workplace = workplace_element.text

        except NoSuchElementException:
            workplace = "N/A"
        return workplace

    def get_company(self):
        try:
            # Process and return the company
            company_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH,
                 "//span[contains(@class,'jobs-unified-top-card__company-name')]/a")
            ))

            company = company_element.text
 
        except NoSuchElementException:
            company = "N/A"
        return company

    def get_title(self):
        try:
            # Process and return the title
            title_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'display-flex justify-space-between')]/a/h2")
            ))
            title = title_element.text
   
        except NoSuchElementException:
            title = "N/A"
        return title

    def get_expertise(self):
        try:
            # Process and return the expertise
            expertise_element = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'mt5 mb2')]/ul/li/span")
            ))
            expertise = expertise_element.text

            start_index = expertise.find("· ")

            if start_index != -1:
                expertise = expertise[start_index+1:]
            else:
                expertise = ""
    
        except NoSuchElementException:
            expertise = "N/A"
        return expertise

    def add_to_csv(self):
        # Create needed folders if it !exists
        file_path = f"{self.path}/data"
        if not os.path.exists(file_path):
            os.makedirs(file_path)
            os.makedirs(file_path+"/raw_data")
            os.makedirs(file_path+"/clean_data")

        # File path to save the CSV file
        file_path = self.path + "/data/raw_data/datarole.csv"

        # Attributes
        attributes = ["Id", "skills", "position", "time", "country",
                      "city", "workplace", "company", "title", "expertise"]

        # Data to be written into the CSV file
        data = [self.Id, ", ".join(self.skills), self.position, self.time, self.country,
                self.city, self.workplace, self.company, self.title, self.expertise]

        # Check if the file exists
        file_exists = os.path.exists(file_path)

        # Open the CSV file in append mode
        with open(file_path, mode='a', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)  # Create a CSV writer object

            if not file_exists:
                try:
                    print(f"Proceeding to create new CSV header...")
                    writer.writerow(attributes)

                except OSError as e:
                    print(f"An error occurred while creating the file")

            # Write the data into the CSV file
            writer.writerow(data)
            print("CSV file writing complete.")

    def display_details(self):
        print("⬛ Job Listing Details:")
        print(f"ID: {self.Id}")
        print(f"Skills: {', '.join(self.skills)}")
        print(f"Position: {self.position}")
        print(f"Time: {self.time}")
        print(f"Country: {self.country}")
        print(f"City: {self.city}")
        print(f"Workplace: {self.workplace}")
        print(f"Company: {self.company}")
        print(f"Title: {self.title}")
        print(f"Expertise: {self.expertise}")
