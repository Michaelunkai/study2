# Opening and Reading Files in Python with Tkinter

import tkinter as tk
from tkinter import filedialog

# Create a function to open and read files
def open_file():
    initial_dir = r"C:\path\to\your\project\folder"  # Set your initial directory
    file_path = filedialog.askopenfilename(initialdir=initial_dir, title="Open File", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

    if file_path:
        file = open(file_path, "rt")
        file_content = file.read()
        print(f"File Content:\n{file_content}")
        file.close()

# Create the Tkinter window
window = tk.Tk()

# Create a button to trigger file dialog
open_button = tk.Button(window, text="Open", command=open_file)
open_button.pack(pady=20)

# Display the GUI
window.mainloop()
