"""
Scrapedin Package
=================

A package for scraping job listings from LinkedIn.

This __init__.py file serves as the entry point for the Scrapedin package, making key classes and subpackages easily accessible.

Subpackages
-----------
- `configurations`: Contains configuration-related modules.
- `jobscraper`: Provides classes and functions for scraping job listings from LinkedIn.

Modules
-------
- `LinkedInLogin`: Class for handling LinkedIn login.
- `LinkedInJobScraper`: Class for scraping job listings on LinkedIn.

Note
----
To simplify access to classes and subpackages, we use the `__all__` attribute to specify what should be accessible when importing the Scrapedin package.
"""

from .configurations.linkedin_login import LinkedInLogin
from .jobscraper.linkedin_job_scraper import LinkedInJobScraper
from .jobscraper.data_preprocessing import stanadard_cleaning
from .jobscraper.data_preprocessing import combine_data
from .jobscraper.data_preprocessing import count_by_country
from .jobscraper.data_preprocessing import top_skills
from .jobscraper.data_preprocessing import job_distribution_by_expertise_level

# List of symbols and subpackages to make accessible when importing the Scrapedin package.
__all__ = ['LinkedInLogin', 'LinkedInJobScraper','stanadard_cleaning','combine_data','count_by_country','top_skills', 'job_distribution_by_expertise_level']
