# Import the Scrapedin class
import Scrapedin as si

# Initialize Scrapedin with the path to the data folder
scraper = si.LinkedInScraper()

# Log in to LinkedIn
email = 'your_email@example.com'
password = 'your_password'
scraper.login(email, password)

# Scrape job listings for a specific role (e.g., "Data Scientist")
scraper.scrape(role='Data Scientist', location='New York, NY')

# Combine data for the same role from multiple files
si.combine_data(role='DataScientist')

# Count the number of job listings by country
si.count_by_country()

# Get the top N skills from the scraped data
si.top_skills(n=10)

# Get the job distribution by expertise level
si.job_distribution_by_expertise_level()