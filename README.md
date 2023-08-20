# Scrapedin Documentation

This is the documentation for the Scrapedin Python module, which is designed to scrape and gather job listings from LinkedIn using Selenium. The module contains various functions and utilities for extracting job data, cleaning and preprocessing the data, and performing data analysis. Below, you'll find the details of each function and how to use them.
#### Last Updated: August 20th, 2023
## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Functions](#functions)
   - [Login](#login)
   - [Scrape](#scrape)
   - [Data Analysis](#data-analysis)
5. [Legality](#legality)
  

<a name="introduction"></a>
## Introduction 

The Scrapedin module provides a convenient way to scrape job listings from LinkedIn, clean and preprocess the data, and perform data analysis. It uses Selenium to interact with the LinkedIn website and gather relevant information about job listings.

**Key Features:**

- **Effortless Job Listing Scraping**: Scrapedin provides an intuitive and simple way to log in to LinkedIn and scrape job listings for a specific role and location. By automating the data collection process, users can quickly gather valuable job data without manual effort.

- **Data Cleaning and Preprocessing**: The module includes various functions for data cleaning and preprocessing, ensuring that the scraped data is of high quality and ready for analysis. Functions remove duplicates, handle corrupt data, preprocess text fields and more.

- **Data Analysis and Insights**: Scrapedin goes beyond scraping by offering essential data analysis functions. Users can count job listings by country, discover the most in-demand skills, and examine the job distribution by expertise level to gain valuable insights from the scraped data.


<a name="installation"></a>
## Installation

Make sure you have [python](https://www.python.org/downloads/) downloaded if you haven't already.
Follow these steps to set up the environment and run the application:

1. Clone the Repository:
   
```bash
git clone https://github.com/Sambonic/Scrapedin
```

```bash
cd Scrapedin
```

2. Create a Python Virtual Environment:
```bash
python -m venv env
```

3. Activate the Virtual Environment:
- On Windows:
  ```
  env\Scripts\activate
  ```

- On macOS and Linux:
  ```
  source env/bin/activate
  ```
4. Ensure Pip is Up-to-Date:
  ```
  python.exe -m pip install --upgrade pip
  ```
5. Install Dependencies:

   ```bash
   pip install .
   ```

6. Import Scrapedin as shown below.


<a name="usage"></a>
## Usage

Here's an example of how to use the Scrapedin module to scrape job listings, and perform data analysis:

```python
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
```


<a name="functions"></a>
## Functions
The following are functions that can be called directly by the user in order to achieve the tasks of logging in, scraping data and analyzing it.

**Note:** Functions starting with "_" found in project files perform the data cleaning process automatically and are not meant to be called directly by the user.

<br></br>
<a name="login"></a>
## Login

**Function: `login(email, password=None)`**

Logs in to LinkedIn using the provided email and password. After logging in the first time, cookies file is established on your local machine from which you can can login using email after.

- Parameters:
    - `email` (str): The email address associated with the LinkedIn account.
    - `password` (str, optional): The password for the LinkedIn account. If not provided and it's first time loggin in, the login process may require additional information and terminate if unsuccessful.

Example Usage:
```python
# Log in to LinkedIn (first time)
email = 'your_email@example.com'
password = 'your_password'
scraper.login(email, password)

# Log in to LinkedIn (cookies exist)
email = 'your_email@example.com'
scraper.login(email)
```

**Note:** Since cookies of your login credentials will be stored on your local machine during the login process, it is important to be aware of the potential security risks. Ensure that you are the only user with access to your computer or hide the project folder appropriately.


<a name="scrape"></a>
## Scrape

**Function: `scrape(role, location=None, page_number=0)`**

Scrapes job listings for a specific role and location from LinkedIn. The scraped data will be saved to a CSV file in the 'raw_data' folder.

Parameters:

- `role`: The job role or title to search for (e.g., "Data Scientist").
- `location` (optional): The location where job listings should be searched (e.g., "United States"). If not provided, it will assume local location of your linkedin account.
- `page_number` (optional): The page number of the job listings to start scraping. The default value is 0.


Example Usage:

```python
# Scrape job listings for "Data Scientist" roles in "United States"
scraper.scrape(role='Data Scientist', location='United States')

# In case of internet interruption, you can continue where you left of by setting the page number
# accordingly and later use the combine_data() function to gather and clean all data in one place.
scraper.scrape(role='Data Scientist', location='United States', page_number=400)
```


<a name="data-analysis"></a>
## Data Analysis

**Function:**
- **`stanadard_cleaning(file_name=None, path=None, logger=None)`**: Clean files automatically and get the output in 'clean_data' folder. It can be performed manually as you see fit.
- **`top_skills(file_name=None, n=None)`**: Gets the top N most frequently occurring skills from the scraped data.
- **`combine_data(role)`**: Combines data for a specific role from multiple CSV files.
- **`count_by_country(file_name=None)`**: Counts the number of job listings by country.
- **`job_distribution_by_expertise_level(file_name=None)`**: Gets the job distribution by expertise level.

<br></br>
### Stanadard_cleaning(file_name=None, path=None, logger=None)
The stanadard_cleaning() function is responsible for standard data cleaning and preprocessing procedures. It applies various cleaning steps to the provided dataset in 'raw_data' folder.

Parameters:

- `file_name` (str, optional): The name of the raw data file. If not provided, then by default the latest file in the "raw_data" folder will be used.
- `path` (str, optional): The path to where data is stored. If not provided, the default "data" folder in the project directory will be used to search for the data.
- `logger` (Logger, optional): A logger object to document the cleaning process. If not provided, the cleaning process will print messages to the console.

Example Usage:
```python
# Default cleaning (clean last scraped file)
si.standard_cleaning()

# Clean specific file by name
si.standard_cleaning("datascientist202307192207.csv")
```
---

### Top_skills(file_name=None, n=None)
The top_skills() function identifies the most frequently mentioned skills in the cleaned dataset and prints the top N skills to the console (or all skills if used on default).

Parameters:

- `file_name` (str, optional): The name of a specific file to apply said function to. If left empty, it will analyze the lastest data added to the folder.
- `n` (int, optional): The number of top skills to display. If not provided, all unique skills will be displayed. Default is None.

Example Usage:
```python
# Get the top N skills from the scraped data
si.top_skills(n=10)

# Get all skills from the scraped data
si.top_skills()
```
---

### Combine_data(role)
The combine_data() function combines all raw data regarding a certain job role and saves into one clean, new file to be analyzed later.

Parameters:
- `role` (str): The job role for which the raw data will be combined.

Example Usage:
```python
# Combine data for the same role from multiple files
si.combine_data(role='DataScientist')
```
---

### Count_by_country(file_name=None)
The count_by_country() function counts the number of job listings for each country in the cleaned dataset and prints the results to the console.

Parameters:
- `file_name` (str, optional): The name of a specific file to apply said function to. If left empty, it will analyze the lastest data added to the folder.

Example Usage:
```python
# Count the number of job listings by country (default)
si.count_by_country()

# Count the number of job listings by country (specific file)
si.count_by_country("datascientist202307192207.csv")
```

---

### Job_distribution_by_expertise_level(file_name=None)
The job_distribution_by_expertise_level() function analyzes the distribution of job listings based on expertise level and prints the results to the console.

Parameters:
- `file_name` (str, optional): The name of a specific file to apply said function to. If left empty, it will analyze the lastest data added to the folder.

Example Usage:
```python
# Get the job distribution by expertise level (default)
si.job_distribution_by_expertise_level()


# Get the job distribution by expertise level (specific file)
si.job_distribution_by_expertise_level("datascientist202307192207.csv")
```

<br></br>
<a name="legality"></a>
# Legality
This project was done for educational purposes and to better understand the intricacies behind data extraction, cleaning and analysis.
It is crucial to understand that any web scraping or data extraction activities you undertake, including using the Scrapedin module, does not comply with all applicable laws of linkedin and can result in legal consequences.
It is your responsibility to understand and comply with the legal requirements related to web scraping and data usage. Creator of Scrapedin module is not responsible for any misuse or illegal use of the module.
<br></br>
For more information read more [here](https://www.linkedin.com/help/linkedin/answer/a1340567/automated-activity-on-linkedin?lang=en)
