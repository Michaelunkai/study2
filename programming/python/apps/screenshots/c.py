import os
import pyautogui
import tkinter as tk
from tkinter import messagebox, Canvas
from PIL import ImageGrab, Image
import threading
import time

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

    # Change the directory to C:\
    os.chdir("C:\\Users\\micha")

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

def take_screenshot_with_delay():
    # Wait for 5 seconds before taking the screenshot
    time.sleep(5)
    
    # Call the screenshot function
    take_screenshot()

def start_delay_thread():
    # Create and start a new thread to handle the delayed screenshot
    delay_thread = threading.Thread(target=take_screenshot_with_delay)
    delay_thread.start()

def take_freeform_screenshot():
    def on_mouse_down(event):
        nonlocal start_x, start_y
        start_x, start_y = event.x, event.y
        canvas.create_rectangle(start_x, start_y, start_x, start_y, outline='red', width=2, tag="rect")

    def on_mouse_drag(event):
        nonlocal start_x, start_y
        canvas.coords("rect", start_x, start_y, event.x, event.y)

    def on_mouse_up(event):
        nonlocal start_x, start_y
        end_x, end_y = event.x, event.y

        # Hide the canvas window
        canvas_window.withdraw()

        # Capture the screenshot of the selected region
        x1 = min(start_x, end_x)
        y1 = min(start_y, end_y)
        x2 = max(start_x, end_x)
        y2 = max(start_y, end_y)

        # Adjust for the canvas window offset
        x1 += canvas_window.winfo_rootx()
        y1 += canvas_window.winfo_rooty()
        x2 += canvas_window.winfo_rootx()
        y2 += canvas_window.winfo_rooty()

        # Take the screenshot of the region
        region = ImageGrab.grab(bbox=(x1, y1, x2, y2))

        # Change the directory to C:\
        os.chdir("C:\\Users\\micha")

        # Get the next available file path
        save_path = get_next_screenshot_path()

        # Save the screenshot
        region.save(save_path)

        # Show a message box indicating success
        messagebox.showinfo("Screenshot Taken", f"Screenshot saved as {save_path}")

        # Destroy the tkinter window
        root.destroy()

    # Hide the main window to avoid capturing it
    root.withdraw()

    # Create a full-screen window with a transparent canvas to capture the region
    canvas_window = tk.Toplevel(root)
    canvas_window.attributes('-fullscreen', True)
    canvas_window.attributes('-alpha', 0.3)
    canvas_window.attributes('-topmost', True)
    canvas = Canvas(canvas_window, cursor="cross")
    canvas.pack(fill=tk.BOTH, expand=True)

    start_x = start_y = 0
    canvas.bind("<ButtonPress-1>", on_mouse_down)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_up)

# Create tkinter window
root = tk.Tk()
root.title("Screenshot Taker")
root.attributes('-topmost', True)

# Create button to take screenshot
screenshot_button = tk.Button(root, text="Take Screenshot", command=take_screenshot)
screenshot_button.pack(pady=10)

# Create button to take freeform screenshot
freeform_button = tk.Button(root, text="Freeform Screenshot", command=take_freeform_screenshot)
freeform_button.pack(pady=10)

# Create button to take screenshot with delay
delay_button = tk.Button(root, text="Delay Screenshot (5s)", command=start_delay_thread)
delay_button.pack(pady=10)

# Run tkinter event loop
root.mainloop()
