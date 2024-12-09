import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    WebDriverException
)
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Hardcoded URL and credentials
TARGET_URL = "https://192.168.1.222:8006/"
CREDENTIALS = {
    "username": "root",
    "password": "123456",
}

# Flexible CSS Selectors for form fields
FIELD_SELECTORS = {
    "username": [
        "input[name='username']", 
        "input[id='username']", 
        "input[placeholder='Username']",
        "input[type='text']"
    ],
    "password": [
        "input[name='password']", 
        "input[id='password']", 
        "input[placeholder='Password']",
        "input[type='password']"
    ]
}

def setup_driver():
    """Set up and configure the Selenium WebDriver."""
    try:
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--ignore-certificate-errors")
        
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except Exception as e:
        logger.error(f"Failed to set up WebDriver: {e}")
        raise

def find_element_with_multiple_selectors(driver, field_name):
    """
    Try multiple CSS selectors to find an element.
    
    Args:
        driver: Selenium WebDriver instance
        field_name: Name of the field to find (username or password)
    
    Returns:
        WebElement if found, None otherwise
    """
    selectors = FIELD_SELECTORS.get(field_name, [])
    
    for selector in selectors:
        try:
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            if element.is_displayed() and element.is_enabled():
                return element
        except (TimeoutException, NoSuchElementException):
            continue
    
    logger.warning(f"Could not find {field_name} field with any provided selector")
    return None

def login_to_site(driver, url, credentials):
    """
    Attempt to log in to the specified site.
    
    Args:
        driver: Selenium WebDriver instance
        url: Target URL to log in
        credentials: Dictionary with username and password
    
    Returns:
        bool: True if login successful, False otherwise
    """
    try:
        # Navigate to the URL
        driver.get(url)
        logger.info(f"Navigating to {url}")
        
        # Wait for potential page load or overlay
        time.sleep(3)
        
        # Find and fill username
        username_element = find_element_with_multiple_selectors(driver, "username")
        if username_element:
            username_element.clear()
            username_element.send_keys(credentials["username"])
            logger.info("Username field filled")
        else:
            logger.error("Could not find username field")
            return False
        
        # Find and fill password
        password_element = find_element_with_multiple_selectors(driver, "password")
        if password_element:
            password_element.clear()
            password_element.send_keys(credentials["password"])
            logger.info("Password field filled")
        else:
            logger.error("Could not find password field")
            return False
        
        # Find and click login button
        login_button_selectors = [
            "button[type='submit']", 
            "input[type='submit']", 
            "button.login-button",
            "button#login-button"
        ]
        
        for selector in login_button_selectors:
            try:
                login_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )
                login_button.click()
                logger.info("Login button clicked")
                return True
            except (TimeoutException, NoSuchElementException):
                continue
        
        logger.error("Could not find login button")
        return False
    
    except Exception as e:
        logger.error(f"Login process failed: {e}")
        return False

def main():
    """Main function to execute the login process and keep browser open."""
    driver = None
    try:
        driver = setup_driver()
        
        # Attempt login
        login_success = login_to_site(driver, TARGET_URL, CREDENTIALS)
        
        if login_success:
            logger.info("Login successful!")
            
            # Keep the browser open indefinitely
            while True:
                # Optional: Add a small delay to prevent high CPU usage
                time.sleep(60)
        else:
            logger.error("Login attempt failed. Please check credentials and site.")
    
    except WebDriverException as wde:
        logger.error(f"WebDriver error: {wde}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        # If you want to keep the browser open on failure, comment out the next line
        # if driver:
        #     driver.quit()
        pass

if __name__ == "__main__":
    main()
