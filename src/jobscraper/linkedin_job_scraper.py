from src.configurations.common_imports import *
from src.configurations.driver import Driver
from src.configurations.linkedin_login import LinkedInLogin
from src.jobscraper.job_listing import JobListing
from src.jobscraper.data_preprocessing import stanadard_cleaning



class LinkedInJobScraper:
    def __init__(self, login, role, location=None, job_number=0):
        self.session = login.session
        self.driver = login.driver
        self.wait = login.wait
        self.path = login.path
        self.logger = login.logger
        self.csv_file_name = self._set_csv_file_name(role)
        self.role = role
        self.location = location
        self.job_number = job_number

        self.links = set()

        self._scrape()

    # Create appropriate filename to store the data
    def _set_csv_file_name(self, role):
        # Create csv file name
        current_time = datetime.now()
        file_date = current_time.strftime("%Y%m%d%H%M")
        role = role.lower().replace(' ','_')
        file_name = f"{role}{file_date}.csv"
        return file_name

    # Start measuring time and space complexities
    def _benchmarking(self):
        # Measure Time Complexity
        start_time = time.time()

        current_time = datetime.now()
        starting_time = current_time.strftime("%H:%M:%S")

        # Function calls to be profiled
        self._gather_info()

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

        #profiler.print_stats()

    # Begin extracting data from gathered links
    def _gather_info(self):
        self.logger.info("Initiating Data Extraction...")

        for index, job_url in enumerate(self.links):
            self.logger.info(
                f"Scraping job listings {index}/{len(self.links)}: {job_url}")

            try:
                job_listing_api = f"https://www.linkedin.com/voyager/api/jobs/jobPostings/{job_url}?decorationId=com.linkedin.voyager.deco.jobs.web.shared.WebFullJobPosting-65&topN=1&topNRequestedFlavors=List(TOP_APPLICANT,IN_NETWORK,COMPANY_RECRUIT,SCHOOL_RECRUIT,HIDDEN_GEM,ACTIVELY_HIRING_COMPANY)"
                job_listing_response = self.session.get(job_listing_api)

                # Check the response
                if job_listing_response.status_code == 200:
                    print("API Response successfully fetched.")
                    with open('response.txt', 'w', encoding='utf-8') as file:
                        json.dump(job_listing_response.json(), file, indent=4)
                else:
                    print("Failed to access API. Status Code:", job_listing_response.status_code)
                    print("Response Content:", job_listing_response.text)
            except requests.exceptions.RequestException as e:
                print(f"An error occurred while making the API request: {e}")

            try:
                skills_api = f"https://www.linkedin.com/voyager/api/graphql?includeWebMetadata=true&variables=(jobPostingUrn:urn%3Ali%3Afsd_jobPosting%3A{job_url})&queryId=voyagerJobsDashJobPostingHowYouFitDetails.bb4a0f9a189c19cfb8b2fe0acbddd62a"
                skills_response = self.session.get(skills_api)

                # Check the response
                if skills_response.status_code == 200:
                    print("API Response successfully fetched.")
                    with open('skills.txt', 'w', encoding='utf-8') as file:
                        json.dump(skills_response.json(), file, indent=4)
                else:
                    print("Failed to access API. Status Code:", skills_response.status_code)
                    print("Response Content:", skills_response.text)
            except requests.exceptions.RequestException as e:
                print(f"An error occurred while making the API request: {e}")

            time.sleep(0.3)

            job_listing = JobListing(self.logger, self.csv_file_name, self.path)
            job_listing._extract_details(details=job_listing_response.json(),skills=skills_response.json())
            job_listing._display_details()
            job_listing._add_to_csv()
        

        stanadard_cleaning(logger=self.logger)

    # Create URL based on given data
    def _build_job_listing_url(self, job_number = 0):
        base_url = f"https://www.linkedin.com/jobs/search/?keywords={self.role}&start={job_number}"
        if self.location is None:
            return base_url
        else:
            return f"{base_url}&location={self.location}"

    # Get total job listings available for searched role
    def _get_total_results(self):
        current_url = self.driver.current_url
        # Regex pattern
        pattern = r"currentJobId=(\d+)"
        # Search for the pattern
        match = re.search(pattern, current_url)
        job_id = match.group(1)


        results_api = (
            f"https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards"
            f"?decorationId=com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollectionLite-84"
            f"&count=7&q=jobSearch&query=(currentJobId:{job_id},origin:JOB_SEARCH_PAGE_LOCATION_AUTOCOMPLETE,keywords:{self.role.replace(' ','%20')},"
            f"locationUnion:(geoId:103644278),selectedFilters:(distance:List(25.0)),"
            f"spellCorrectionEnabled:true)&servedEventEnabled=false&start={self.job_number}"
        )

        try:
            response = self.session.get(results_api)

            # Check the response
            if response.status_code == 200:
                print("API Response successfully fetched.")
                return int(response.json()["paging"]["total"])
            else:
                print("Failed to access API. Status Code:", response.status_code)
                print("Response Content:", response.text)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while making the API request: {e}")

    # Extract job listings per page
    def _process_page(self, job_number):
   
        job_listings_api = (
            f"https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards"
            f"?decorationId=com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollection-216&count=25"
            f"&q=jobSearch&query=(origin:HISTORY,keywords:{self.role.replace(' ','%20')},locationUnion:(geoId:103644278),"
            f"selectedFilters:(distance:List(2000.0)),spellCorrectionEnabled:true)&start={job_number}"
        )
        try:
            response = self.session.get(job_listings_api)

            # Check the response
            if response.status_code == 200:
                print("API Response successfully fetched.")
                jobs = str(response.json().get("metadata", {}).get("jobCardPrefetchQueries", [{}])[0].get("prefetchJobPostingCardUrns", []))
                # Regex pattern
                pattern = r"urn:li:fsd_jobPostingCard:\((\d+),"
                # Find all matches
                job_ids = re.findall(pattern, jobs)
                return job_ids

            else:
                print("Failed to access API. Status Code:", response.status_code)
                print("Response Content:", response.text)
                return []
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while making the API request: {e}")
            return []

    # Scrape all links available of said job role
    def _scrape(self):
        # Find and retrieve the total number of results
        role_job_listings = self._build_job_listing_url()
        self.driver.get(role_job_listings)

        total_results = self._get_total_results()

        start_time = time.time()
        # Save pages for when job listings will be extracted
        for job_number in range(self.job_number, min(900, total_results), 25):
            self.session.get(self._build_job_listing_url(job_number))
            jobs = self._process_page(job_number)
            self.links.update(jobs)
            
        print(len(self.links))
        end_time = time.time()
        print("Execution Time:", end_time - start_time, "seconds")

        self.logger.info(f"Total number of links: {len(self.links)}")
        self._benchmarking()
