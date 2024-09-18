from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# GeckoDriver executable path
gecko_driver_path = r"C:\Users\micha\Downloads\geckodriver.exe"

# Initialize the GeckoDriver service
service = Service(executable_path=gecko_driver_path)
driver = webdriver.Firefox(service=service)

driver.get("https://google.com")

# Wait for the search input field to be present
WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.NAME, "q"))
)

input_element = driver.find_element(By.NAME, "q")
input_element.clear()
input_element.send_keys("@mychannel-wr8kq" + Keys.ENTER)

# Wait for the link containing "mychannel" to be present
WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "mychannel"))
)

link = driver.find_element(By.PARTIAL_LINK_TEXT, "mychannel")

# Click on the "mychannel" link using JavaScript
driver.execute_script("arguments[0].click();", link)

time.sleep(10)

driver.quit()
