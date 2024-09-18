# # Creating a Custom Menu Bar in Tkinter
import tkinter as tk

# Define functions
def open_file():
    print("File has been opened")

def save_file():
    print("File has been saved")

def cut():
    print("Text has been cut")

def copy():
    print("Text has been copied")

def paste():
    print("Text has been pasted")

# Create the main window
window = tk.Tk()
window.title("Custom Menu Bar Tutorial")

# Create a menu bar
menu_bar = tk.Menu(window)

# Set the menu bar for the window
window.config(menu=menu_bar)

# Create a File menu
file_menu = tk.Menu(menu_bar, tearoff=0)

# Add a label to the File menu
menu_bar.add_cascade(label="File", menu=file_menu)

# Add commands to the File menu
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=window.quit)

# Create an Edit menu
edit_menu = tk.Menu(menu_bar, tearoff=0)

# Add a label to the Edit menu
menu_bar.add_cascade(label="Edit", menu=edit_menu)

# Add commands to the Edit menu
edit_menu.add_command(label="Cut", command=cut)
edit_menu.add_command(label="Copy", command=copy)
edit_menu.add_command(label="Paste", command=paste)

# Change font for both menus
file_menu['font'] = ('Arial', 12)
edit_menu['font'] = ('Arial', 12)

# Add images to File menu commands
open_image = tk.PhotoImage(file="open.png")  # Replace "open.png" with your actual image file
save_image = tk.PhotoImage(file="save.png")  # Replace "save.png" with your actual image file
exit_image = tk.PhotoImage(file="exit.png")  # Replace "exit.png" with your actual image file

file_menu.add_command(label="Open", command=open_file, image=open_image, compound=tk.LEFT)
file_menu.add_command(label="Save", command=save_file, image=save_image, compound=tk.LEFT)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=window.quit, image=exit_image, compound=tk.LEFT)

# Run the main loop
window.mainloop()
