"""
Jobscraper Package
=================

A subpackage within Scrapedin for handling job scraping from LinkedIn.

This __init__.py file serves as the entry point for the Jobscraper subpackage, making key modules and classes easily accessible.

Modules
-------
- `job_listing`: Provides classes and functions for job listing data extraction and processing.
- `linkedin_job_scraper`: Contains a class for logging into LinkedIn and scraping job listings.
- `data_preprocessing`: Contains functions for data cleaning and preprocessing.

Note
----
To simplify access to modules, we use the `__all__` attribute to specify what should be accessible when importing the Jobscraper subpackage.
"""

from .job_listing import *
from .linkedin_job_scraper import *

# List of modules to make accessible when importing the Jobscraper subpackage.
__all__ = ['job_listing', 'linkedin_job_scraper', 'data_preprocessing']
