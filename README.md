# Yahoo_Signup_Automation
Software Automation Testing of signing up Yahoo email using the verification from Whatsapp Web  and verifiying the creation of the Yahoo email
# Yahoo Signup Automation

## Overview
This project automates the process of signing up for a Yahoo email account using verification from WhatsApp Web. It includes Selenium-based automation scripts, and tests implemented using pytest.

## Prerequisites
Before running the automation script, ensure you meet the following prerequisites:

1. **WhatsApp Web Login:**
   - Ensure you are logged into your WhatsApp Web on Google Chrome.

2. **Edit the User Directory:**
   - Edit the `user_data_dir` line in `tests/test_yahoo_signup.py` to match your Chrome user data directory.
     ```python
     user_data_dir = r'C:\Users\YourUsername\AppData\Local\Google\Chrome\User Data'
     ```

3. **WhatsApp Number:**
   - Update the Excel file (`Mohamed_data.xlsx`) under the `phone` column with your own WhatsApp number.

## Steps to Run the Script

1. **Open WhatsApp Web:**
   - Open WhatsApp Web and ensure it is correctly loaded and you are logged in.

2. **Run the Script:**
   - Execute the test script which will perform the following actions:
     1. Open the Yahoo signup page.
     2. Fill in the signup form details from the Excel file.
     3. When prompted, enter your WhatsApp number for verification.
     4. Switch to WhatsApp Web, read the verification code, copy it, and delete the message.
     5. Refresh WhatsApp Web to ensure the message is deleted and verify by checking the absence of the copied code.
     6. Complete the Yahoo signup process by entering the verification code.
     7. Confirm that the Yahoo email is created by checking the presence of the user's name instead of the 'sign up' button.

## Learning Points

This project involves several key learning points:

1. **Web Scraping and Automation:**
   - Using Selenium for web scraping and automating web interactions.
   - Techniques to wait for elements, find elements by various locators, and perform mouse operations.

2. **Headless Browser Operation:**
   - Running browser automation in headless mode for efficiency and bypassing detection.

3. **Session Management:**
   - Leveraging Chrome's user data directory to maintain login sessions, particularly for WhatsApp Web.
     ```python
     if user_data_dir:
         profile_dir = 'Default'
         options.add_argument(f"user-data-dir={user_data_dir}")
         options.add_argument(f"profile-directory={profile_dir}")
     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
     ```

4. **Excel Integration:**
   - Reading from and writing to Excel files to handle test data and results.
   - Using utilities to manipulate Excel sheets within the script.

5. **Error Handling and Alerts:**
   - Implementing robust error handling and showing custom alerts during the test execution.

6. **Using pytest:**
   - Structuring tests using pytest framework.
   - Yielding the driver fixture to ensure proper setup and teardown.

7. **Randomization and Human-Like Interactions:**
   - Adding random delays and clicks to mimic human interactions and avoid detection.

## Running the Tests

To run the tests, execute the following command in your terminal:

```bash
pytest
