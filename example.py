# Import the Scrapedin class
import src as si
from dotenv import load_dotenv
import os 

load_dotenv()

# Input your email and password
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

# Log in to LinkedIn
login = si.LinkedInLogin(email, password)

# Define a specific role (e.g., "Data Scientist")
role='Data Scientist'

# Initialize and scrape job listings for the role
scraper = si.LinkedInJobScraper(login, role=role)
scraper.scrape()

# Combine data for the same role from multiple files
si.combine_data(role=role)

# Count the number of job listings by country
si.count_by_country()

# Get the top N skills from the scraped data
si.top_skills(n=10)

# Get the job distribution by expertise level
si.job_distribution_by_expertise_level()