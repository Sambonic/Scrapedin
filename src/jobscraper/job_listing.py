from src.configurations.common_imports import *
from src.jobscraper.data_preprocessing import _translate_skills


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

    def __init__(self, logger, csv_file_name, path):
        
        self._logger = logger
        self._csv_filename = csv_file_name
        self._path = path

        self.job_details = {}
    

    def _extract_details(self, details, skills) -> None:
        # NB. Check salary and skills later
        self.job_details.update({
            "id": details.get("jobPostingId"),
            "company": details.get("companyDetails", {}).get("com.linkedin.voyager.deco.jobs.web.shared.WebJobPostingCompany", {}).get("companyResolutionResult", {}).get("name"),
            "salary": details.get("salaryInsights"), 
            "employment_status": details.get("formattedEmploymentStatus"),
            "title": details.get("title"),
            "headcount": details.get("companyDetails", {}).get("com.linkedin.voyager.deco.jobs.web.shared.WebJobPostingCompany", {}).get("companyResolutionResult", {}).get("staffCountRange", {}).get("start"),
            "industry": details.get("formattedIndustries"),
            "experience": details.get("formattedExperienceLevel"),
            "applicants": details.get("applies"),
            "hiring_team": details.get("allJobHiringTeamMembersInjectionResult", {}).get("hiringTeamMembers"),
            "location": details.get("formattedLocation"),
            "workplace": details.get("workplaceTypesResolutionResults", {}).get("urn:li:fs_workplaceType:3", {}).get("localizedName"),
            "skills": self._extract_skills(skills),
            "description": details.get("description", {}).get("text"),
            "views": details.get("views"),
            "job_function": details.get("formattedJobFunctions"),
            "role": details.get("standardizedTitleResolutionResult", {}).get("localizedName"),
            "benefits": details.get("benefits"),
            "referrals_elgible": details.get("eligibleForReferrals"),
        })

    def _extract_skills(self, skills):
        try:
            insights = (
                skills.get("data", {}).get("jobsDashJobPostingHowYouFitDetailsByJobPosting", {})
                    .get("elements", [{}])[0]
                    .get("howYouFitDetailSections", [{}])[1]
                    .get("howYouFitInsights", [])
            )
            
            return [
                insight.get("displayText")
                for insight in insights
                if "displayText" in insight
            ]
        except (KeyError, IndexError):
            return []

    def _add_to_csv(self) -> None:
        """
        Adds job listing details to a CSV file. Creates necessary folders if needed, formats the data, and appends it to an appropriately named CSV file in the 'raw data' folder of the project.
        """
        file_path = os.path.join(self._path, "data")

        os.makedirs(file_path, exist_ok=True)
        os.makedirs(os.path.join(file_path, "raw_data"), exist_ok=True)
        os.makedirs(os.path.join(file_path, "clean_data"), exist_ok=True)

        csv_file_path = os.path.join(file_path, "raw_data", self._csv_filename)

        file_exists = os.path.exists(csv_file_path)

        with open(csv_file_path, mode='a', newline='', encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.job_details.keys())

            if not file_exists:
                try:
                    self._logger.info("Proceeding to create a new CSV header. . .")
                    writer.writeheader()
                except OSError as e:
                    self._logger.error("An error occurred while creating the file: %s", str(e))
            writer.writerow(self.job_details)
            self._logger.info("Data inserted into CSV file successfully.")

    def _display_details(self) -> None:
        """
        Displays details extracted in the terminal.
        """
        self._logger.info("⬛ Job Listing Details:")
        # Iterate over all instance variables dynamically
        for key, value in self.job_details.items():
            self._logger.info(f"{key.capitalize().replace('_', ' ')}: {value}")
