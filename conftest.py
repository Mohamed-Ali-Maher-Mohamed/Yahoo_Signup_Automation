# conftest.py
import pytest
from utils.selenium_utils import init_driver

@pytest.fixture(scope="module")
def get_driver():
    def _get_driver(headless=True, user_data_dir=None):
        driver = init_driver(headless=headless, user_data_dir=user_data_dir)
        yield driver
        driver.quit()
    return _get_driver



"""""""""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    yield driver
    driver.quit()


"""""""""
