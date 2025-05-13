import os
import pyautogui
import keyboard
from datetime import datetime

save_directory = r'C:\Users\micha\Pictures'

if not os.path.exists(save_directory):
    os.makedirs(save_directory)

def take_screenshot():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'screenshot_{timestamp}.png'
    filepath = os.path.join(save_directory, filename)
    screenshot = pyautogui.screenshot()
    screenshot.save(filepath)

keyboard.add_hotkey('f9', take_screenshot)

print('Press F9 to take a screenshot. Press Ctrl+C to exit.')

keyboard.wait('ctrl+c')
