import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

def test_web_application():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")
    service = Service('/usr/bin/chromedriver')  # Path to chromedriver

    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get('https://www.example.com')

        # Example check: Verify title of the web page
        assert driver.title == 'Example Domain'

    except WebDriverException as e:
        pytest.fail(f"WebDriver exception: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()  # Ensure that the browser is closed
