import os
import pyautogui

def get_next_screenshot_path():
    directory = os.path.join("C:", "Pictures")
    base_filename = "screenshot"
    extension = ".png"

    # Find the next available filename
    i = 1
    while True:
        filename = f"{base_filename}{i}{extension}"
        save_path = os.path.join(directory, filename)
        if not os.path.exists(save_path):
            return save_path
        i += 1

def take_screenshot():
    # Change the directory to C:\Users\micha
    os.chdir("C:\\Users\\micha")

    # Take screenshot
    screenshot = pyautogui.screenshot()

    # Get the next available file path
    save_path = get_next_screenshot_path()

    # Save the screenshot
    screenshot.save(save_path)

# Take the screenshot immediately without any GUI
take_screenshot()
