"""
Configurations Package
======================

A subpackage within Scrapedin for handling configuration-related tasks.

This __init__.py file serves as the entry point for the Configurations subpackage, making key modules and classes easily accessible.

Modules
-------
- `common_imports`: Contains common imports used throughout the Scrapedin package.
- `driver`: Provides the WebDriver class for Selenium-based web scraping.
- `linkedin_login`: Contains a class for handling LinkedIn login.

Note
----
To simplify access to modules and classes, we use the `__all__` attribute to specify what should be accessible when importing the Configurations subpackage.
"""

from .common_imports import *
from ..managers.linkedin_login import *

# List of modules and classes to make accessible when importing the Configurations subpackage.
__all__ = ['common_imports', 'driver_manager', 'linkedin_login']
