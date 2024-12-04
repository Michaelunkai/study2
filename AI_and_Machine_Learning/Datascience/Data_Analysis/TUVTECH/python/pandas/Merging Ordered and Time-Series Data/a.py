import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager

# Form data with hardcoded username and password
form_fields = {
    "email": "michaelovsky5@gmail.com",
    "first_name": "Michael",
    "last_name": "Fedorovsky",
    "password": "123456",
    "confirm_password": "123456",
    "phone": "0547632418",
    "country_code": "+972",
    "master_password_hint": "69",
    "company": "YourCompanyName",
    "zip_code": "5965121",
    "username": "root",
    "job_title": "Student",
    "city": "bat yam",
    "postal_code": "5965121",
    "address": "daliya23",
}

# Extended field selectors
field_selectors = {
    "email": "input[type='email'], input[name*='email' i], input[id*='email' i], input[placeholder*='email' i]",
    "first_name": "input[name*='first' i], input[id*='first' i], input[placeholder*='first' i], input[name*='fname' i], input[id*='fname' i]",
    "last_name": "input[name*='last' i], input[id*='last' i], input[placeholder*='last' i], input[name*='lname' i], input[id*='lname' i]",
    "password": "input[type='password']:not([name*='master' i]):not([name*='retype' i]):not([name*='confirm' i])",
    "confirm_password": "input[type='password'][name*='confirm' i], input[type='password'][id*='confirm' i], input[type='password'][placeholder*='confirm' i], input[type='password'][name*='retype' i]",
    "phone": "input[type='tel'], input[name*='phone' i], input[id*='phone' i], input[placeholder*='phone' i], input[name*='mobile' i], input[id*='mobile' i]",
    "country_code": "select[name*='country' i], select[id*='country' i], select[placeholder*='country' i], select[name*='phone' i], select[id*='phone' i]",
    "master_password": "input[name*='master' i]:not([name*='retype' i]):not([name*='confirm' i])",
    "retype_master_password": "input[name*='retype' i], input[name*='confirm' i]",
    "master_password_hint": "input[name*='hint' i], input[id*='hint' i], input[placeholder*='hint' i]",
    "company": "input[name*='company' i], input[id*='company' i], input[placeholder*='company' i], input[name*='organization' i], input[id*='organization' i]",
    "zip_code": "input[name*='zip' i], input[id*='zip' i], input[placeholder*='zip' i], input[name*='postal' i], input[id*='postal' i], input[placeholder*='postal' i]",
    "username": "input[name*='username' i], input[id*='username' i], input[placeholder*='username' i], input[name*='user' i], input[id*='user' i]",
    "job_title": "input[name*='job' i], input[id*='job' i], input[placeholder*='job' i], input[name*='title' i], input[id*='title' i], input[name*='occupation' i], input[id*='occupation' i]"
}

def setup_driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    return webdriver.Chrome(service=service, options=options)

def wait_for_element(driver, selector, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )

def find_and_fill_field(driver, field_name, value):
    selector = field_selectors.get(field_name)
    if not selector:
        print(f"No selector defined for field: {field_name}")
        return False

    try:
        elements = driver.find_elements(By.CSS_SELECTOR, selector)
        for element in elements:
            if element.is_displayed() and element.is_enabled():
                if element.tag_name.lower() == "select":
                    Select(element).select_by_visible_text(value)
                else:
                    element.clear()
                    element.send_keys(value)
                print(f"Filled '{field_name}' field with '{value}'")
                return True
        print(f"No fillable element found for '{field_name}'")
        return False
    except Exception as e:
        print(f"An error occurred while filling '{field_name}': {e}")
        return False

def click_agreement_checkbox(driver):
    checkbox_selectors = [
        "input[type='checkbox'][name*='agree' i]",
        "input[type='checkbox'][id*='agree' i]",
        "input[type='checkbox'][name*='terms' i]",
        "input[type='checkbox'][id*='terms' i]",
        "label:contains('I agree to the Main Services Agreement')",
        "label:contains('I agree to the Terms of Service')",
        "label:contains('I accept the Terms and Conditions')"
    ]

    for selector in checkbox_selectors:
        try:
            checkbox = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            if not checkbox.is_selected():
                checkbox.click()
            print("Clicked agreement checkbox")
            return True
        except (TimeoutException, ElementClickInterceptedException):
            continue
        except Exception as e:
            print(f"An error occurred while trying to click the agreement checkbox: {e}")

    print("Could not find or click agreement checkbox")
    return False

def submit_form(driver):
    submit_button_selectors = [
        "button[type='submit']",
        "input[type='submit']",
        "button:contains('Submit')",
        "input[value='Submit']",
        "button:contains('Register')",
        "input[value='Register']",
        "button:contains('Sign Up')",
        "input[value='Sign Up']",
        "button:contains('Create Account')",
        "input[value='Create Account']"
    ]

    for selector in submit_button_selectors:
        try:
            submit = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            submit.click()
            print("Form submitted")
            return True
        except (TimeoutException, ElementClickInterceptedException):
            continue
        except Exception as e:
            print(f"An error occurred while trying to submit the form: {e}")

    print("Could not find or click submit button")
    return False

def fill_form(driver, url):
    driver.get(url)
    time.sleep(5)  # Wait for the page to load

    for field, value in form_fields.items():
        if not find_and_fill_field(driver, field, value):
            print(f"Failed to fill '{field}' field. Continuing with the next field.")

    if not find_and_fill_field(driver, "master_password", form_fields["password"]):
        print("No 'master password' field found or could not fill it.")
    if not find_and_fill_field(driver, "retype_master_password", form_fields["password"]):
        print("No 'retype master password' field found or could not fill it.")

    if not click_agreement_checkbox(driver):
        print("Failed to click agreement checkbox. You may need to do this manually.")

    if not submit_form(driver):
        print("Form submission failed. You may need to submit manually.")

def main():
    driver = setup_driver()

    try:
        while True:
            url = input("Enter the website URL (or 'quit' to exit): ")
            if url.lower() == 'quit':
                break
            fill_form(driver, url)

            choice = input("Continue to next form? (y/n): ")
            if choice.lower() != 'y':
                break
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

