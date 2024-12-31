import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import undetected_chromedriver as uc
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chatgpt_bot.log'),
        logging.StreamHandler()
    ]
)

class ChatGPTBot:
    def __init__(self):
        self.driver = None
        self.message_count = 0
        self.retry_count = 0
        self.max_retries = 3

    def start_driver(self):
        try:
            options = uc.ChromeOptions()
            options.add_argument(f'user-agent={UserAgent().random}')
            options.add_argument('user-data-dir=./')
            
            self.driver = uc.Chrome(
                driver_executable_path=ChromeDriverManager().install(),
                options=options
            )
            logging.info("Browser started successfully")
            return True
        except Exception as e:
            logging.error(f"Failed to start browser: {str(e)}")
            return False

    def wait_for_element(self, by, selector, timeout=20, clickable=False):
        try:
            wait = WebDriverWait(self.driver, timeout)
            condition = (
                EC.element_to_be_clickable((by, selector))
                if clickable
                else EC.presence_of_element_located((by, selector))
            )
            return wait.until(condition)
        except TimeoutException:
            logging.warning(f"Timeout waiting for element: {selector}")
            return None
        except Exception as e:
            logging.error(f"Error waiting for element {selector}: {str(e)}")
            return None

    def send_message(self, message):
        try:
            # Try to find the main textarea first
            textarea = self.wait_for_element(
                By.ID,
                "prompt-textarea",
                clickable=True
            )
            
            if not textarea:
                # Fallback to finding by class if ID doesn't work
                textarea = self.wait_for_element(
                    By.CSS_SELECTOR,
                    "div[contenteditable='true'].ProseMirror",
                    clickable=True
                )
            
            if not textarea:
                return False
                
            # Clear the textarea
            textarea.clear()
            
            # Type the message
            textarea.send_keys(message)
            time.sleep(1)
            
            # Send with Enter key
            textarea.send_keys(Keys.RETURN)
            
            logging.info(f"Message sent: {message}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to send message: {str(e)}")
            return False

    def wait_for_response(self, timeout=60):
        start_time = time.time()
        
        try:
            # Wait for the response to complete
            while time.time() - start_time < timeout:
                # Check if the message input is enabled (indicating response is complete)
                textarea = self.driver.find_element(By.ID, "prompt-textarea")
                if textarea.is_enabled():
                    return True
                time.sleep(1)
                
            logging.warning("Response timeout reached")
            return False
            
        except Exception as e:
            logging.error(f"Error waiting for response: {str(e)}")
            return False

    def monitor_chat(self):
        while True:
            try:
                # Send "next" message
                if not self.send_message("next"):
                    self.handle_error()
                    continue

                # Wait for response
                if not self.wait_for_response():
                    self.handle_error()
                    continue

                # Wait 35 seconds before next message
                time.sleep(35)

                # Increment message counter
                self.message_count += 1
                
                # Refresh page every 10 messages
                if self.message_count >= 10:
                    logging.info("Refreshing page...")
                    self.driver.refresh()
                    time.sleep(5)
                    self.message_count = 0

            except Exception as e:
                logging.error(f"Error in monitor_chat: {str(e)}")
                self.handle_error()

    def handle_error(self):
        self.retry_count += 1
        if self.retry_count >= self.max_retries:
            logging.error("Max retries reached. Restarting browser...")
            self.restart_browser()
            self.retry_count = 0
        else:
            logging.warning(f"Retry attempt {self.retry_count}/{self.max_retries}")
            time.sleep(5)

    def restart_browser(self):
        try:
            if self.driver:
                self.driver.quit()
        except:
            pass
            
        if self.start_driver():
            self.driver.get('https://chat.openai.com/chat')
            logging.info("Browser restarted. Waiting for login...")
            input("Press Enter after logging in...")
        else:
            logging.error("Failed to restart browser. Exiting...")
            exit(1)

    def run(self):
        if not self.start_driver():
            logging.error("Failed to start browser. Exiting...")
            return

        self.driver.get('https://chat.openai.com/chat')
        logging.info(f"Page loaded: {self.driver.title}")
        input("Press Enter after logging in...")
        
        # Send initial "next" message
        self.send_message("next")
        
        # Start monitoring
        self.monitor_chat()

if __name__ == "__main__":
    bot = ChatGPTBot()
    bot.run()
