import logging
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def test_facebook_account(username, password):
    logger = logging.getLogger('test_facebook_account')
    try:
        # Initialize the Chrome webdriver
        driver = webdriver.Chrome()

        # Open Facebook login page
        driver.get("https://www.facebook.com/")

        # Handle cookies popup if it appears
        try:
            decline_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Decline optional cookies"]')))
            decline_button.click()
        except TimeoutException:
            logger.info("No cookies popup, proceeding with login.")

        # Find and fill in the username and password fields
        driver.find_element(By.NAME, "email").send_keys(username)
        driver.find_element(By.NAME, "pass").send_keys(password)

        # Click the login button
        driver.find_element(By.NAME, "login").click()

        # Wait for the page to load and check for an element that indicates a successful login
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Create a post"]')))
            logger.info(f"Login successful for {username}")
        except TimeoutException:
            logger.error(f"Login failed for {username}")

    except (WebDriverException, NoSuchElementException) as e:
        logger.error(f"Error occurred during login for {username}: {str(e)}")
    finally:
        # Close the browser
        driver.quit()


def read_accounts_from_file(filename):
    accounts = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        current_account = {}
        for line in lines:
            line = line.strip()
            if line.startswith('username='):
                current_account['username'] = line.split('=')[1]
            elif line.startswith('password='):
                current_account['password'] = line.split('=')[1]
                accounts.append(current_account.copy())
                current_account.clear()
    return accounts


def main():
    # Prompt user for the file directory
    while True:
        file_directory = input("Please enter the directory of the file containing Facebook accounts: ")
        if os.path.exists(file_directory):
            break
        else:
            print("Invalid directory. Please enter a valid directory.")

    # Example of how the file should be formatted
    print("\nExample of how the file should be formatted:")
    print("username=example@gmail.com")
    print("password=example_password\n")

    # Read accounts from the file
    try:
        accounts = read_accounts_from_file(file_directory)
        if not accounts:
            print("No accounts found in the file.")
        else:
            for account in accounts:
                test_facebook_account(account['username'], account['password'])
    except FileNotFoundError:
        print("File not found. Please make sure you enter the correct file directory.")


if __name__ == "__main__":
    main()
