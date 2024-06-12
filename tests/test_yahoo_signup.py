# tests/test_yahoo_signup.py
from tkinter import messagebox
import tkinter as tk
import win32api
import pickle
import random
import pytest
import time
import os
import datetime
import re
import calendar
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from utils.excel_utils import read_excel, write_excel
from selenium.webdriver.support.select import Select
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)



def random_click(driver):
    actions = ActionChains(driver)
    window_size = driver.get_window_size()
    width = window_size['width']
    height = window_size['height']

    # Choose a random point within the window's bounds
    x_offset = random.randint(0, width // 2)  # half the width to avoid out of bounds
    y_offset = random.randint(0, height // 2)  # half the height to avoid out of bounds

    # Move to a guaranteed visible element first, then offset from there
    body = driver.find_element(By.TAG_NAME, 'body')
    actions.move_to_element_with_offset(body, x_offset, y_offset).click().perform()


def random_delay():
    time.sleep(random.uniform(0.1, 0.3))


def show_alert(driver, message, duration=5):
    # Inject JavaScript to create an alert
    alert_script = f"alert('{message}');"
    driver.execute_script(alert_script)

    # Wait for the specified duration
    time.sleep(duration)

    # Switch to the alert and accept it (close it)
    alert = driver.switch_to.alert
    alert.accept()


def perform_help_operation(driver, wait): # funnction to go to help page and perfom basic search (mimic human interactions)
    # Store the main window handle
    main_window_handle = driver.current_window_handle
    time.sleep(2)

    # Locate and click on the help link
    help_link = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='login-body']/div[1]/div/a[1]")))
    #help_link.click()
    # Open the help link in a new tab
    ActionChains(driver) \
        .key_down(Keys.CONTROL) \
        .click(help_link) \
        .key_up(Keys.CONTROL) \
        .perform()

    # Wait for the new window and switch to it
    wait.until(lambda driver: len(driver.window_handles) > 1)
    new_window_handle = [handle for handle in driver.window_handles if handle != main_window_handle][0]
    driver.switch_to.window(new_window_handle)

    try:
        # Wait for and click the reject button if it appears
        reject_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@value='reject']")))
        driver.execute_script("arguments[0].scrollIntoView(true);", reject_button)
        reject_button.click()
        time.sleep(2)
    except:
        # If the reject button doesn't appear, just continue with the next steps
        pass

    # Perform search in the new window
    searchitem = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='searchInput']")))
    searchitem.send_keys('how to create email')

    searchbutton = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='search-submit']")))
    searchbutton.click()

    # Save cookies
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

    time.sleep(3)

    # Close the new window and switch back to the original window
    driver.close()
    driver.switch_to.window(main_window_handle)



def perform_yahoo_signup_test(driver):
    wait = WebDriverWait(driver, 10)
    data = read_excel("yahoo_signup")

    for record in data:
        # Example of using data from the Excel sheet
        first_name = record['First name']
        surname = record['Surname']
        day = record['Day']
        month = record['Month']
        month_index = list(calendar.month_name).index(month.capitalize())
        year = str(record['Year'])  # Convert year to string
        telephone_number = str(record['phone'])
        password = record['Password']
        signup_url = record['signup_url']
        whatsapp_url = record['whatsapp_url']
        login_url = record['login_url']
        break

    overall_status = "Passed"  # Initialize overall status

    driver.get(whatsapp_url)

    time.sleep(3)

    try:
        whatsapp_web = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[normalize-space(text())='WhatsApp Web']")))
        whatsapp_web.click()
        time.sleep(3)
    except:
        print('continuing with the test')
        # Scroll down if the button is not found

    all_msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='side']/div[2]/button[1]")))
    all_msg.click()

    time.sleep(3)

    driver.get(signup_url)
    # Example steps to fill in the signup form
    login_first_name: WebElement = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@id,'firstName')]")))
    for char in first_name:
        login_first_name.send_keys(char)
        random_delay()

    #perform_help_operation(driver, wait)



    login_surname: WebElement = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@id,'lastName')]")))
    for char in surname:
        login_surname.send_keys(char)
        random_delay()
    #login_surname.send_keys(surname)

    random_delay()

    now = datetime.datetime.now()
    # Format the date and time
    date_str = now.strftime("%Y%m%d.%H%M")
    # Create the unique username
    unique_user_name = f"{first_name}{surname}{date_str}"

    Email_address: WebElement = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@id,'userId')]")))
    Email_address.clear()

    for char in unique_user_name:
        Email_address.send_keys(char)
        random_delay()

    created_email = unique_user_name + "@yahoo.com"
    print('created_email', created_email)

    record['created_email'] = created_email

    password_input: WebElement = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@id,'password')]")))
    for char in password:
        password_input.send_keys(char)
        random_delay()

    birth_day: WebElement = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@id,'day')]")))
    birth_day.send_keys(day)

    random_delay()

    drp_down_month_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//select[contains(@id,'month')]")))
    drpc_down_month = Select(drp_down_month_element)
    drpc_down_month.select_by_index(month_index)

    random_delay()

    birth_year: WebElement = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@id,'year')]")))
    for char in year:
        birth_year.send_keys(char)
        random_delay()

    next_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[contains(@id,'submit-button')]")))
    next_button.click()

    time.sleep(2)

    try:
        Telephone: WebElement = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@id,'phone')]")))

        # Check if the element is displayed
        if Telephone.is_displayed():
            Result = "The Telephone_element is displayed."
            print(Result)
            record['Status'] = "Passed"
        else:
            Result = "The Telephone_element is not displayed."
            print(Result)
            record['Reason'] = Result
            record['Status'] = "Failed"
            overall_status = "Failed"  # Set overall status to Failed
            os.startfile(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Mohamed_data.xlsx'))
            pytest.fail(Result)  # This will cause the test to fail
    except Exception as e:
        print(f"Error: {e}")
        record['Reason'] = str(e)
        record['Status'] = "Failed"
        overall_status = "Failed"  # Set overall status to Failed
        os.startfile(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Mohamed_data.xlsx'))
        pytest.fail(str(e))  # This will cause the test to fail

    write_excel("yahoo_signup", data)

    Telephone: WebElement = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@id,'phone')]")))
    for char in telephone_number:
        Telephone.send_keys(char)
        random_delay()
    random_delay()

    whatsapp_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[contains(@id,'whatsapp')]")))
    whatsapp_button.click()

    main_window_handle = driver.current_window_handle
    time.sleep(2)

    # Open a new tab by simulating the Ctrl + t shortcut
    driver.execute_script("window.open('');")
    time.sleep(2)  # Allow the new tab to open

    # Get the handles of all open windows
    window_handles = driver.window_handles

    # Switch to the new tab (it will be the last in the list)
    driver.switch_to.window(window_handles[-1])

    # Navigate to the desired URL in the new tab
    driver.get(whatsapp_url)

    try:
        whatsapp_web = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[normalize-space(text())='WhatsApp Web']")))
        whatsapp_web.click()
        time.sleep(3)
    except:
        print('continuing with the test')
        # Scroll down if the button is not found


    yahoo_whats_msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Yahoo')]")))
    yahoo_whats_msg.click()

    elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//strong[@class='_ao3e selectable-text copyable-text']")))

    verification_code = None
    for element in elements:
        element.click()
        text = element.text
        # if re.match(r'^\d{6}$', text):  # Check if the text is exactly 6 digits
        if text:
            verification_code = text
            break
    print('verification_code', verification_code)

    def delete_yahoo_message():
        try:
            dropdown_xpath = "//span[contains(@data-icon,'down-context')]"
            delete_drpdown = driver.find_element(By.XPATH, dropdown_xpath)
            delete_drpdown.click()

            time.sleep(5)

            delete_option_xpath = "//div[@role='button' and @aria-label='Delete']"
            delete_option = wait.until(EC.visibility_of_element_located((By.XPATH, delete_option_xpath)))
            delete_option.click()

            time.sleep(2)

            confirm_xpath = "//*[@id='app']/div/span[2]/div/span/div/div/div/div/div/div[2]/div/button[2]/div/div"
            confirm_button = wait.until(EC.visibility_of_element_located((By.XPATH, confirm_xpath)))
            confirm_button.click()

            time.sleep(5)

            driver.refresh()

            time.sleep(2)
        except Exception as e:
            print("Error while deleting the message:", str(e))

    # Delete message loop
    message_deleted = False
    while not message_deleted:
        delete_yahoo_message()
        try:
            yahoo_whats_msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Yahoo')]")))
            yahoo_whats_msg.click()

            elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//strong[@class='_ao3e selectable-text copyable-text']")))
            message_deleted = all(not el.text for el in elements)

        except:
            message_deleted = True

    time.sleep(2)

    # Close the new window and switch back to the original window
    driver.close()
    driver.switch_to.window(main_window_handle)

    verification: WebElement = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='verification-code-field']")))
    verification_code = str(verification_code)
    for char in verification_code:
        verification.send_keys(char)
        random_delay()
    #verification.send_keys(day)

    time.sleep(3)


    verification_button: WebElement = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='verification-code-field']")))
    verification_button.click()

    time.sleep(3)

    following_confirmation: WebElement = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='verify-code-button']")))
    following_confirmation.click()

    time.sleep(3)


    success_button: WebElement = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='account-attributes-challenge-success']/form/button")))
    success_button.click()

    time.sleep(3)


    try:
        reject_cookies = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='consent-page']/div/div/div/form/div[2]/div[2]/button[2]")))
        reject_cookies.click()
    except:
        # Scroll down if the button is not found
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            # Try to find and click the button again after scrolling
            reject_cookies = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='consent-page']/div/div/div/form/div[2]/div[2]/button[2]")))
            reject_cookies.click()
        except:
            print("Reject Cookies button did not appear, proceeding with the script.")

    time.sleep(3)


    try:
        yahoo_email_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@id='ybarAccountMenu']")))
        yahoo_email_button.click()

        # Check if the element is displayed
        if yahoo_email_button.is_displayed():
            Result = "The yahoo email is created."
            print(Result)
            record['Status'] = "Passed"
            record['Reason'] = "No failures were detected"
        else:
            Result = "The yahoo email is not created."
            print(Result)
            record['Reason'] = Result
            record['Status'] = "Failed"
            overall_status = "Failed"  # Set overall status to Failed
            print('data 6', data)
    except Exception as e:
        print(f"Error: {e}")
        record['Reason'] = str(e)
        record['Status'] = "Failed"
        overall_status = "Failed"  # Set overall status to Failed

    # Check if detected as robot
    try:
        robot_checking = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Confirm you’re not a robot') or contains(text(), 'Error')]")))
        if robot_checking.is_displayed():
            print("Detected as robot, re-running the test in headless mode")
            show_alert(driver, "Detected as robot, re-running the test in headless mode", duration=2)
            overall_status = "Failed"  # Set overall status to Failed due to robot detection
            record['Status'] = "Failed"
            record['Reason'] = "Detected as robot"
    except:
        print("No robot detection, proceeding with the test")

        # Write the results to Excel
    write_excel("yahoo_signup", data)

    # Open the Excel file at the end
    os.startfile(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Mohamed_data.xlsx'))

    return overall_status  # Indicates overall status of the test


def test_yahoo_signup(get_driver):
    # Define user data directory
    user_data_dir = r'C:\Users\dida_\AppData\Local\Google\Chrome\User Data'

    # First run in non-headless mode with user data directory
    driver = next(get_driver(headless=False, user_data_dir=user_data_dir)) # without user_data_dir driver = next(get_driver(headless=....))

    test_passed = perform_yahoo_signup_test(driver)

    if test_passed == "Failed":
        # Rerun the test in headless mode if it failed due to robot detection
        print("++++++++++++++++++++++++++++++++++++++")
        print("Re-running the test in headless mode")
        driver = next(get_driver(headless=True, user_data_dir=user_data_dir))
        test_passed = perform_yahoo_signup_test(driver)


















































"""
# Not used function

import random
from selenium.webdriver.common.action_chains import ActionChains

def random_delay(min_delay=0.5, max_delay=2.0):
    time.sleep(random.uniform(min_delay, max_delay))

# Function to perform a random click
def random_click(driver):
    actions = ActionChains(driver)
    window_size = driver.get_window_size()
    width = window_size['width']
    height = window_size['height']

    # Choose a random point within the window's bounds
    x_offset = random.randint(0, width // 2)  # half the width to avoid out of bounds
    y_offset = random.randint(0, height // 2)  # half the height to avoid out of bounds

    # Move to a guaranteed visible element first, then offset from there
    body = driver.find_element(By.TAG_NAME, 'body')
    actions.move_to_element_with_offset(body, x_offset, y_offset).click().perform()

random_click(driver)

"""