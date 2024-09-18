import os
import pyautogui
import tkinter as tk
from tkinter import messagebox

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
    # Hide the main window to avoid capturing it
    root.withdraw()
    
    # Take screenshot
    screenshot = pyautogui.screenshot()
    
    # Get the next available file path
    save_path = get_next_screenshot_path()
    
    # Save the screenshot
    screenshot.save(save_path)
    
    # Show a message box indicating success
    messagebox.showinfo("Screenshot Taken", f"Screenshot saved as {save_path}")
    
    # Destroy the tkinter window
    root.destroy()

# Create tkinter window
root = tk.Tk()
root.title("Screenshot Taker")

# Create button to take screenshot
screenshot_button = tk.Button(root, text="Take Screenshot", command=take_screenshot)
screenshot_button.pack(pady=10)

# Run tkinter event loop
root.mainloop()
