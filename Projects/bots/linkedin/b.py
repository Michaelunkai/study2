import os
import time
import psutil
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def close_chrome():
    # Close all instances of Google Chrome
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].lower() == 'chrome.exe':
            print(f"Terminating Chrome with PID: {proc.info['pid']}")
            proc.terminate()  # Gracefully terminate Chrome processes

def launch_chrome():
    # Setup Chrome to run with minimized options and avoid detection
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode to avoid detection
    chrome_options.add_argument("--disable-extensions")  # Disable extensions to reduce risk
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-gpu")  # Disabling GPU rendering
    chrome_options.add_argument("--disable-software-rasterizer")  # Force software rendering
    chrome_options.add_argument("--log-level=3")  # Suppress unnecessary logs

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver

def run_linkedin():
    while True:
        print("Closing any existing Chrome browser instances...")
        close_chrome()  # Make sure to close any running Chrome instances

        print("Launching Chrome to navigate to LinkedIn...")
        driver = launch_chrome()

        try:
            driver.get("https://www.linkedin.com/login")  # Navigates to LinkedIn login page
            time.sleep(120)  # Wait for 2 minutes (or customize duration) before closing browser
        finally:
            driver.quit()  # Ensure that Chrome is closed after use

        print("Waiting for the next cycle...")
        time.sleep(30)  # Optional delay before restarting the cycle

if __name__ == "__main__":
    run_linkedin()

