import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from fake_useragent import UserAgent

def start_driver():
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={UserAgent().random}")
    options.add_argument("user-data-dir=./")
    return uc.Chrome(options=options)

def send_message(driver, message):
    try:
        chat_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "textarea"))
        )
        chat_input.send_keys(message)
        time.sleep(2)
        chat_input.send_keys(Keys.ENTER)
        print("Message sent.")
    except Exception as e:
        print(f"An error occurred while sending the message: {e}")

def monitor_chat(driver):
    last_text = ""
    message_count = 0
    while True:
        try:
            # Wait for a new message
            messages = driver.find_elements(By.XPATH, "//div[contains(@class, 'message')]")
            if messages:
                last_message = messages[-1].text
                if last_message != last_text:
                    last_text = last_message
                else:
                    send_message(driver, "next")
                    message_count += 1
                    if message_count >= 10:  # Reload the page after 10 messages
                        print("Reloading the page to avoid session issues...")
                        driver.refresh()
                        message_count = 0
                    time.sleep(10)  # Wait to ensure message is sent before checking again
            else:
                send_message(driver, "next")
        except Exception as e:
            print(f"An error occurred while monitoring the chat: {e}")
            try:
                driver.quit()
            except:
                pass
            driver = start_driver()
            driver.get('https://chat.openai.com/chat')
            input("Press Enter after you are logged in and inside the chat...")

if __name__ == "__main__":
    driver = start_driver()
    driver.get('https://chat.openai.com/chat')
    print("Page loaded: ", driver.title)
    input("Press Enter after you are logged in and inside the chat...")
    monitor_chat(driver)