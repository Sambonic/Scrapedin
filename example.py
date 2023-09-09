# Import the Scrapedin class
import scrapedin as si

# Log in to LinkedIn
email = 'your_email@example.com'
password = 'your_password'
login = si.LinkedInLogin(user, password)

# Initialize and scrape job listings for a specific role (e.g., "Data Scientist")
scraper = si.LinkedInJobScraper(login, role='Data Scientist')

# Combine data for the same role from multiple files
si.combine_data(role='Data Scientist')

# Count the number of job listings by country
si.count_by_country()

# Get the top N skills from the scraped data
si.top_skills(n=10)

# Get the job distribution by expertise level
si.job_distribution_by_expertise_level()