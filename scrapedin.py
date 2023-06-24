import os
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def loadcookies(directory, username):
    driver = webdriver.Chrome()
    # Load the serialized cookies from the file
    with open(directory+username+'.pkl', 'rb') as file:
        serialized_cookies = file.read()

    cookies = pickle.loads(serialized_cookies)
    driver.get("https://www.linkedin.com/")

    for cookie in cookies:
        driver.add_cookie(cookie)

    driver.refresh()
    print("Logged in successfully!")


def createcookies(directory, username, password):
    driver = webdriver.Chrome()
    driver.get("https://www.linkedin.com/")

    wait = WebDriverWait(driver, 10)
    user_field = wait.until(EC.presence_of_element_located((By.ID, 'session_key')))
    pass_field = wait.until(EC.presence_of_element_located((By.ID, 'session_password')))
    user_field.send_keys(username)
    pass_field.send_keys(password)

    sign_in = driver.find_element(By.XPATH, "//button[@type='submit']") 
    sign_in.click()

    cookies = driver.get_cookies()
    serialized_cookies = pickle.dumps(cookies)

    # Create new folder for user
    os.makedirs(directory)
    # Create new cookies and store in associated folder
    with open(directory+username+'.pkl', 'wb') as file:
        file.write(serialized_cookies)

    driver.quit()
    
    print( f"New user detected, user '{username}' created successfully.")
    loadcookies(directory, user)


def search_user(root_dir, folder_name, password):
    directory = root_dir+folder_name
    if not os.path.exists(directory):
        try:
            print( f"First login. Proceeding to create log file for new user. . . ")
            createcookies(directory, folder_name, password)

        except OSError as e:
            print(
                f"An error occurred while creating folder '{folder_name}': {e}")
    else:
        print(f"User '{folder_name}' exists. Proceeding to login. . .")
        loadcookies(directory, folder_name)


def login(username, password, root_dir):
    search_user(root_dir, username, password)


root_dir = "directory where you want the project to be in"
username = "email@gmail.com"
password = "password"
login(username, password, root_dir)
