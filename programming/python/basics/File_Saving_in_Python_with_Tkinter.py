# File Saving in Python with Tkinter
from tkinter import filedialog
import tkinter as tk

# Define the Save File Function
def save_file():
    # Open the file dialog for saving
    file = filedialog.asksaveasfile(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("HTML files", "*.html"), ("All files", "*.*")],
        initialdir="C:\\your\\project\\folder"
    )

# Check if the user canceled the file dialog
    if file is None:
        return

    # Get text from the Text area
    file_text = text.get("1.0", "end-1c")

    # Write the text to the selected file
    file.write(file_text)

    # Close the file
    file.close()

# Create the main window
window = tk.Tk()

# Create a Save button
button = tk.Button(window, text="Save", command=save_file)
button.pack()

# Create a Text area
text = tk.Text(window)
text.pack()

# Start the Tkinter main loop
window.mainloop()