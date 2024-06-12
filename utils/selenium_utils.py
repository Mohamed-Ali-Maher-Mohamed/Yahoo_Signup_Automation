# utils/selenium_utils.py
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service  # Import the Service class
from selenium_stealth import stealth
import random

# Randomization functions for various attributes
def get_random_language():
    #languages = ["en-US", "en-GB", "fr-FR", "de-DE", "es-ES", "ja-JP", "ru-RU", "zh-CN"]
    languages = ["en-US", "en-GB"]
    return random.choice(languages)

def get_random_platform():
    platforms = ["Win32", "Linux", "Macintosh", "Android", "iOS"]
    return random.choice(platforms)

def get_random_vendor():
    vendors = ["Google Inc.", "Mozilla Foundation", "Apple Inc.", "Microsoft Corporation"]
    return random.choice(vendors)

def get_random_webgl_vendor():
    webgl_vendors = ["Intel Inc.", "NVIDIA Corporation", "AMD", "Broadcom", "ARM"]
    return random.choice(webgl_vendors)

def get_random_renderer():
    renderers = [
        "Intel Iris OpenGL Engine", "NVIDIA GeForce GTX 1080", "AMD Radeon HD 6700",
        "Google SwiftShader", "Microsoft Basic Render Driver"
    ]
    return random.choice(renderers)

def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1"
    ]
    return random.choice(user_agents)

def init_driver(headless=True, user_data_dir=None):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("start-maximized")
    options.add_argument("enable-automation")
    options.add_argument("--disable-infobars")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(f"user-agent={get_random_user_agent()}")

    if user_data_dir:
        profile_dir = 'Default'  # or 'Profile 1', 'Profile 2', etc.
        options.add_argument(f"user-data-dir={user_data_dir}")
        options.add_argument(f"profile-directory={profile_dir}")


    # Initialize the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Apply stealth settings with random attributes
    stealth(driver,
            languages=[get_random_language()],
            vendor=get_random_vendor(),
            platform=get_random_platform(),
            webgl_vendor=get_random_webgl_vendor(),
            renderer=get_random_renderer(),
            fix_hairline=True)

    return driver


"""""""""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os

def init_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("start-maximized")
    options.add_argument("enable-automation")
    options.add_argument("--disable-infobars")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
          Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
          })
        '''
    })
    return driver

"""""""""
