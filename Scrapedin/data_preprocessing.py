from Scrapedin.common_imports import *


def _path_setter(file_name=None, path=None, logger=None):
    if path is None:
        current_file_path = os.path.abspath(__file__)
        current_directory = os.path.dirname(current_file_path)
        parent_path = os.path.dirname(current_directory)
        path = os.path.join(parent_path, "data")
    else:
        path = os.path.join(path, "data")

    raw_path = os.path.join(path, "raw_data")
    clean_path = os.path.join(path, "clean_data")

    if file_name is None:
        # Get all file names in the folder path
        entries = os.scandir(raw_path)
        files = [entry for entry in entries]

        if files:
            # Get the last added file
            file_name = os.path.basename(files[-1].path)

            if logger is None:
                print(f"File: {file_name}")
            else:
                logger.info(f"File: {file_name}")
        else:
            if logger is None:
                print("Folder is empty")
            else:
                logger.info("Folder is empty")

    raw_path = os.path.join(path, "raw_data", file_name)
    clean_path = os.path.join(path, "clean_data", file_name)

    return raw_path, clean_path

# Data cleaning and preprocessing functions
def stanadard_cleaning(file_name=None, path=None, logger=None):
    if logger is None:
        print("Proceeding to apply standard data cleaning procedure")
    else:
        logger.info("Proceeding to apply standard data cleaning procedure")

    raw_path, clean_path = _path_setter(file_name, path, logger)

    df = pd.read_csv(raw_path)
    df = _remove_empty_skills(df)
    df = _remove_dollar_rows(df)
    df = _remove_duplicates(df)
    df = _remove_corrupted_data(df)
    df = _preprocess_skills(df)
    df = _convert_date(df)
    df = _convert_salary(df)
    df.to_csv(clean_path, index=False)

    top_skills()
    df.info()
    df.describe()

def _remove_empty_skills(df):
    df = df[~(df['skills'] == "[]")]
    return df

def _remove_dollar_rows(df):
    df = df[~(df['position'].str.contains('\$') |
              df['expertise'].str.contains('\$'))]
    return df

def _remove_duplicates(df):
    column_name = 'id'
    df_no_duplicates = df.drop_duplicates(subset=column_name)
    return df_no_duplicates

def _remove_corrupted_data(df):
    df = df[~df['country'].str.contains('·')]
    return df

def _preprocess_skills(df):
    df['skills'] = df['skills'].str.lower()
    df['skills'] = df['skills'].str.title()
    return df

def _convert_date(df):
    df['date'] = pd.to_datetime(df['date'])
    return df

def _convert_salary(df):
    df['salary'] = df['salary'].str.replace(
        '/hr', '/yr').replace('$', '').replace(',', '').split(' - ')

    for i, row in df.iterrows():
        if len(row['salary']) == 2:  # If the salary range has two values
            low_salary = float(row['salary'][0]) * 40 * \
                52  # Convert low salary to yearly
            # Convert high salary to yearly
            high_salary = float(row['salary'][1]) * 40 * 52
            df.at[i, 'salary'] = f"${low_salary:,.0f} - ${high_salary:,.0f}/yr"
        else:
            # Convert single salary to yearly
            yearly_salary = float(row['salary'][0]) * 40 * 52
            df.at[i, 'salary'] = f"${yearly_salary:,.0f}/yr"
    else:  # If 'salary' is a single numeric value
        # Convert single salary to yearly
        yearly_salary = float(row['salary']) * 40 * 52
        df.at[i, 'salary'] = f"${yearly_salary:,.0f}/yr"

    return df

# Data analysis
def translate_skills(skills):
    translated_skills = ""

    options = Options()
    options.headless = True
    translate_driver = webdriver.Chrome(options)
    translate_driver.get(
        'https://translate.google.com/?sl=auto&tl=en&op=translate')
    wait = WebDriverWait(translate_driver, 10)

    time.sleep(0.2)

    input_area = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//*[@id='yDmH0d']/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[1]/span/span/div/textarea")
    ))
    output_area = wait.until(EC.presence_of_element_located(
        (By.XPATH,
            "/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[2]/div/div[9]")
    ))
    input_area.clear()
    input_area.send_keys(skills)
    input_area.send_keys(Keys.ENTER)

    time.sleep(3)

    while "..." in output_area.text:
        time.sleep(1)

    translated_skills = output_area.text

    return translated_skills

def combine_data(role, file_name=None, path=None):

    role = role.replace(" ", "")

    raw_path, clean_path = _path_setter(file_name, path)

    # Get parent directories
    raw_path = os.path.dirname(raw_path)
    clean_path = os.path.dirname(clean_path)

    entries = os.scandir(raw_path)
    files = [entry for entry in entries if role in os.path.basename(entry)]

    if files:
        combined_data = pd.DataFrame()

        for file in files:
            file_path = os.path.join(raw_path, file)
            data = pd.read_csv(file_path)
            combined_data = combined_data.append(data)

        file_name = f'{role}combined.csv'
        combined_file_path = os.path.join(raw_path, file_name)
        combined_data.to_csv(combined_file_path, index=False)

        stanadard_cleaning()

def count_by_country():
    raw_path, clean_path = _path_setter()

    df = pd.read_csv(clean_path)
    country_counts = df['country'].value_counts()

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    print(country_counts)

def top_skills(n=None):

    if n == "max" or n == None:
        n = len(skill_counts)

    raw_path, clean_path = _path_setter()
    df = pd.read_csv(clean_path)

    df['skills'] = df['skills'].str.split(', ').explode('skills')

    skill_counts = df['skills'].value_counts()
   
    top_skills = skill_counts.head(n)

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    print(top_skills)

def job_distribution_by_expertise_level():

    raw_path, clean_path = _path_setter()
    df = pd.read_csv(clean_path)
    
    exclude_list = ["Full-time", "Part-time", "Contract", "Internship"]

    filtered_df = df[~df['expertise'].isin(exclude_list)]

    job_distribution = filtered_df['expertise'].value_counts()

    print(job_distribution)


