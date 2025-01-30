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
role='Software Engineer'

# Initialize and scrape job listings for the role
scraper = si.LinkedInJobScraper(login, role=role)
scraper.scrape()