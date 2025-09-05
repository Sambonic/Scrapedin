from src.config.common_imports import *
from src.jobscraper.job_listing import JobListing
from src.decorators.benchmarking import benchmark
from src.decorators.logging import log_function_call
from src.config.config import *
from src.managers.csv_handler import CSVHandler
from src.managers.logger_manager import logger
from src.managers.linkedin_login import LinkedInLogin

class LinkedInJobScraper:
    def __init__(self, login: LinkedInLogin, role: str, location: str = None, job_number: int = 0):
        self.session = login.session
        self.role = role
        self.location = location
        self.job_number = job_number
        self.links = set()

    @log_function_call
    def _fetch_api_data(self, url: str) -> dict:
        """
        Handles API requests and returns JSON data and status code.
        """
        response = self.session.get(url)
        if response.status_code != 200:
            logger.warning(f"Non-200 status code received from {url}: {response.status_code}")
        return response.json() if response.status_code == 200 else None, response.status_code

    @log_function_call
    def _fetch_job_details(self, job_number: str) -> dict:
        """
        Fetch job listing details from API.
        """
        job_listing_api = JOB_DETAILS_API.format(job_number=job_number)
        return self._fetch_api_data(job_listing_api)

    @log_function_call
    def _fetch_skills(self, job_number: str) -> dict:
        """
        Fetch skills details for a job from API.
        """
        skills_api = SKILLS_API.format(job_number=job_number)
        return self._fetch_api_data(skills_api)

    @log_function_call
    def _fetch_job_listings(self, job_number: int) -> dict:
        """
        Fetch job listings from API.
        """
        job_listings_api = JOB_LISTINGS_API.format(role=self.role.replace(' ', '%20'), job_number=job_number)
        return self._fetch_api_data(job_listings_api)

    @benchmark
    @log_function_call
    def _gather_info(self) -> None:
        """
        Gather job details and skills from APIs and save the data.
        """
        csv_instance = CSVHandler(self.role)

        for index, job_url in enumerate(self.links):
            logger.info(f"=== Scraping job listing {index + 1}/{len(self.links)}: {job_url} ===")
            
            job_details, _ = self._fetch_job_details(job_url)
            skills_details, _ = self._fetch_skills(job_url)
            
            time.sleep(REQUEST_DELAY)
            
            job_listing = JobListing()
            job_listing._extract_details(details=job_details, skills=skills_details)
            job_listing._display_details()

            csv_instance._add_to_csv(job_listing.job_details)

    @log_function_call
    def _process_page(self, job_number: int) -> Tuple[List[str], int]:
        """
        Fetch job listings from API and extract job IDs.
        """
        data, status_code = self._fetch_job_listings(job_number)
        
        if data:
            jobs = str(data.get("metadata", {}).get("jobCardPrefetchQueries", [{}])[0].get("prefetchJobPostingCardUrns", []))
            job_ids = re.findall(r"urn:li:fsd_jobPostingCard:\((\d+),", jobs)
            return job_ids, status_code
        
        return [], status_code

    @benchmark
    @log_function_call
    def scrape(self) -> None:
        """
        Scrape job listings from LinkedIn.
        """
        JOBS_URL.format(role=self.role, job_number=self.job_number) + (f"&location={self.location}" if self.location else "")
        self.session.get(JOBS_URL)

        for job_number in range(self.job_number, LINKEDIN_LIMIT, 25):
            jobs, status_code = self._process_page(job_number)
            if status_code != 200:
                logger.error(f"Received {status_code} status code at job_number {job_number}. Stopping execution.")
                break

            self.links.update(jobs)

        logger.info(f"Total number of links: {len(self.links)}")
        self._gather_info()