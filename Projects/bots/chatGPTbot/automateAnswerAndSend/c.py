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
    options.binary_location = "/usr/bin/google-chrome-stable"  # Path to the Chrome binary
    return uc.Chrome(options=options)

def send_message(driver, message):
    try:
        # Wait for the textarea to be present and interactable
        chat_input = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.TAG_NAME, "textarea"))
        )
        chat_input.send_keys(message)
        time.sleep(2)

        # Wait for the send button to be present and clickable
        send_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#__next > div > div.relative.flex.h-full.max-w-full.flex-1.flex-col.overflow-hidden > main > div.flex.h-full.flex-col.focus-visible\\:outline-0 > div.md\\:pt-0.dark\\:border-white\\/20.md\\:border-transparent.md\\:dark\\:border-transparent.w-full > div.text-base.px-3.md\\:px-4.m-auto.md\\:px-5.lg\\:px-1.xl\\:px-5 > div > form > div > div.flex.w-full.items-center > div > div > button > svg"))
        )
        send_button.click()

        print("Message sent.")
    except Exception as e:
        print(f"An error occurred while sending the message: {e}")

def wait_for_chat_to_finish(driver, timeout=30):
    start_time = time.time()
    last_message_count = 0

    while time.time() - start_time < timeout:
        messages = driver.find_elements(By.XPATH, "//div[contains(@class, 'message')]")
        current_message_count = len(messages)

        if current_message_count == last_message_count:
            time.sleep(2)  # Wait for a short period to ensure no new messages are coming
            messages = driver.find_elements(By.XPATH, "//div[contains(@class, 'message')]")
            if len(messages) == current_message_count:
                break  # Chat has finished responding
        else:
            last_message_count = current_message_count
            time.sleep(2)  # Wait before checking again

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
                    wait_for_chat_to_finish(driver)
                    send_message(driver, "next")
                    message_count += 1
                    if message_count >= 10:  # Reload the page after 10 messages
                        print("Reloading the page to avoid session issues...")
                        driver.refresh()
                        message_count = 0
                    time.sleep(20)  # Wait 20 seconds before sending the next message
            else:
                send_message(driver, "next")
                time.sleep(20)  # Wait 20 seconds before sending the next message
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

    # Send "next" immediately after pressing Enter
    send_message(driver, "next")

    # Start monitoring the chat
    monitor_chat(driver)
