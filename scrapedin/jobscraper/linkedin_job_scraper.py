from scrapedin.configurations.common_imports import *
from scrapedin.configurations.driver import Driver
from scrapedin.configurations.linkedin_login import LinkedInLogin
from scrapedin.jobscraper.job_listing import JobListing
from scrapedin.jobscraper.data_preprocessing import stanadard_cleaning



class LinkedInJobScraper:
    def __init__(self, login, role, location=None, job_number=0, batch_size = 1):
        self.driver = login.driver
        self.wait = login.wait
        self.path = login.path
        self.logger = login.logger
        self.csv_file_name = self._set_csv_file_name(role)
        self.role = role
        self.location = location
        self.job_number = job_number
        self.batch_size = batch_size

        self.links = set()

        asyncio.run(self._scrape())

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

            self.driver.get(job_url)
            time.sleep(0.3)

            job_listing = JobListing(
                self.driver, self.wait, self.logger, self.csv_file_name, self.path)
            job_listing._extract_job_details()
            job_listing._display_details()
            job_listing._add_to_csv()

        stanadard_cleaning(logger=self.logger)

    # Create URL based on given data
    def _build_job_listing_url(self, role, location, job_number):
        if location is None:
            return f"https://www.linkedin.com/jobs/search/?keywords={role}&start={job_number}"
        else:
            return f"https://www.linkedin.com/jobs/search/?keywords={role}&start={job_number}&location={location}"

    # Get total job listings available for searched role
    def _get_total_results(self):
        try:
            results = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'jobs-search-results-list__subtitle')]/span")))
            total_results = int(''.join(filter(str.isdigit, results.text)))
            total_results = min(total_results, 1000)
            print(f'Total results to gather: {total_results}')
            return total_results
        except (NoSuchElementException, TimeoutException):
            return 0

    # Extract job listings per page
    async def _process_page(self, url):

        self.driver.get(url)
        await asyncio.sleep(3)

        try:
            link_elements = self.wait.until(EC.presence_of_all_elements_located(
                (By.XPATH, "//ul[contains(@class,'scaffold-layout__list-container')]//li")))
        except TimeoutException:
            # No more job listings
            return 0

        for element in link_elements:
            try:
                link_id = element.get_attribute("data-occludable-job-id")
                if link_id is not None:
                    link = f"https://www.linkedin.com/jobs/view/{link_id}"
                    async with asyncio.Lock():
                        self.links.add(link)
            except StaleElementReferenceException:
                continue   

    # Scrape links in batches 
    async def _process_links_batch(self, links):
        tasks = []
        for url in links:
            tasks.append(self._process_page(url))

        await asyncio.gather(*tasks)

    # Asynchronously scrape all links available of said job role
    async def _scrape(self):
        urls = []

        # Find and retrieve the total number of results
        role_job_listings = self._build_job_listing_url(
            self.role, self.location, self.job_number)
        self.driver.get(role_job_listings)

        total_results = self._get_total_results()

        # Save pages for when job listings will be extracted
        for job_number in range(self.job_number, total_results, 25):
            url = self._build_job_listing_url(
                self.role, self.location, job_number)
            urls.append(url)

        start_time = time.time()
        # Number of links to process in each batch
        for i in range(0, len(urls), self.batch_size):
            batch = urls[i:i + self.batch_size]
            await self._process_links_batch(batch)
            self.logger.info(
            f"Job listings gathered: {len(self.links)} / {total_results}")
        
        end_time = time.time()
        print("Async Execution Time:", end_time - start_time, "seconds")

        self.logger.info(f"Total number of links: {len(self.links)}")
        self._benchmarking()
